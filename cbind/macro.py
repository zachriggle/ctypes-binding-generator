'''Generate Python codes from macro constants.'''

import logging
import os
import re
import subprocess
import tempfile
from collections import OrderedDict, namedtuple
from cStringIO import StringIO
from clang.cindex import Index, CursorKind
from cbind.util import walk_astree


class MacroException(Exception):
    '''Exception raised by MacroGenerator class.'''
    pass


class MacroGenerator:
    '''Generate Python code from macro constants.'''

    MAGIC = '__macro_symbol_magic'

    def __init__(self, macro_include=None, macro_exclude=None, macro_int=None):
        '''Initialize object.'''
        self.symbol_table = OrderedDict()
        self.parser = Parser()
        match_nothing = lambda s: False
        if macro_include:
            self.macro_include = re.compile(macro_include).match
        else:
            self.macro_include = match_nothing
        if macro_exclude:
            self.macro_exclude = re.compile(macro_exclude).match
        else:
            self.macro_exclude = match_nothing
        if macro_int:
            self.macro_int = re.compile(macro_int).match
        else:
            self.macro_int = match_nothing

    def parse(self, c_path, args):
        '''Parse the source files.'''
        int_symbols = []
        candidates = MacroSymbol.enumerate_candidates(c_path)
        for symbol in MacroSymbol.process(c_path, args):
            if not symbol.body:
                # Ignore empty macros
                continue
            if symbol.name not in candidates:
                if not self.macro_include(symbol.name):
                    continue
            else:
                if self.macro_exclude(symbol.name):
                    continue
            if self._parse_symbol(symbol):
                pass
            elif symbol.args is None and self.macro_int(symbol.name):
                # We could not parse this symbol, but since user assures us
                # that it is a constant integer, let us give it another try...
                self.symbol_table[symbol.name] = None
                int_symbols.append(symbol)
            else:
                logging.info('Could not parse macro: %s', symbol.macro)
        if int_symbols:
            for symbol in self._translate_const_int(c_path, args, int_symbols):
                self.symbol_table[symbol.name] = symbol
        self._check_bound_name()

    def _parse_symbol(self, symbol):
        '''Parse macro symbol body.'''
        try:
            expr = self.parser.parse(symbol.body)
        except CSyntaxError:
            return False
        new_symbol = MacroSymbol.set_expr(symbol, expr)
        # pylint: disable=E1101
        self.symbol_table[new_symbol.name] = new_symbol
        return True

    @classmethod
    def _translate_const_int(cls, c_path, args, symbols):
        '''Translate constant integers with libclang.'''
        enums = cls._clang_const_int(c_path, args, symbols)
        regex_name = re.compile('^%s_(\w+)$' % cls.MAGIC)
        symbol_map = dict((symbol.name, symbol) for symbol in symbols)
        for enum in enums:
            match = regex_name.match(enum.spelling)
            if match:
                yield cls._make_int_literal(symbol_map[match.group(1)],
                        enum.enum_value)

    @staticmethod
    def _make_int_literal(symbol, value):
        '''Make a new symbol for integer literal expression.'''
        int_literal = Token(kind=Token.INT_LITERAL, spelling=str(value))
        expr = Expression(this=int_literal, children=())
        return MacroSymbol.set_expr(symbol, expr)

    @classmethod
    def _clang_const_int(cls, c_path, args, symbols):
        '''Run clang on constant integers.'''
        tmp_src_fd, tmp_src_path = tempfile.mkstemp(suffix='.c')
        try:
            with os.fdopen(tmp_src_fd, 'w') as tmp_src:
                c_abs_path = os.path.abspath(c_path)
                tmp_src.write('#include "%s"\n' % c_abs_path)
                tmp_src.write('enum {\n')
                for symbol in symbols:
                    tmp_src.write('%s_%s = %s,\n' %
                            (cls.MAGIC, symbol.name, symbol.body))
                tmp_src.write('};\n')
            index = Index.create()
            tunit = index.parse(tmp_src_path, args=args)
            if not tunit:
                msg = 'Could not parse generated C source'
                raise MacroException(msg)
        finally:
            os.remove(tmp_src_path)
        return cls._find_enums(tunit)

    @staticmethod
    def _find_enums(tunit):
        '''Find enums of translation unit.'''
        nodes = []
        def search_enum_def(cursor):
            '''Test if the cursor is an enum definition.'''
            if cursor.kind is CursorKind.ENUM_DECL and cursor.is_definition():
                nodes.append(cursor)
        walk_astree(tunit.cursor, search_enum_def)
        if not nodes:
            msg = 'Could not find enum in generated C source'
            raise MacroException(msg)
        enum_nodes = []
        for node in nodes:
            enum_nodes.extend(node.get_children())
        return enum_nodes

    def _check_bound_name(self):
        '''Check if there are references to undefined symbols.'''
        bound_names = frozenset(name for name in self.symbol_table
                if self.symbol_table[name])
        for name in bound_names:
            symbol = self.symbol_table[name]
            if symbol.args:
                env = bound_names.union(symbol.args)
            else:
                env = bound_names
            def check_symbol_name(token):
                '''Check if token name is defined.'''
                if token.kind is not Token.SYMBOL:
                    return
                if token.spelling in env:
                    return
                raise CSyntaxError(token.spelling)
            try:
                symbol.expr.traverse(check_symbol_name)
            except CSyntaxError as err:
                logging.info('Could not resolve reference to "%s" in %s',
                        err.args[0], symbol.macro)
                self.symbol_table[name] = None

    def generate(self, output):
        '''Generate macro constants.'''
        for symbol in self.symbol_table.itervalues():
            if not symbol:
                continue
            output.write('%s = ' % symbol.name)
            if symbol.args is not None:
                output.write('lambda %s: ' % ', '.join(symbol.args))
            symbol.expr.translate(output)
            output.write('\n')


class MacroSymbol(namedtuple('MacroSymbol', 'name args body expr')):
    '''C macro.'''

    # pylint: disable=W0232,E1101

    REGEX_DEFINE = re.compile(r'\s*#\s*define\s+(\w+)')
    REGEX_ARGUMENTS = re.compile(r'''
            \(
                \s*
                (
                    \w+
                    (?:
                        \s*,\s*\w+
                    )*
                )?
                \s*
            \)''', re.VERBOSE)

    @classmethod
    def enumerate_candidates(cls, c_path):
        '''Get locally-defined macro names.'''
        candidates = set()
        with open(c_path) as c_src:
            for c_src_line in c_src:
                match = cls.REGEX_DEFINE.match(c_src_line)
                if match:
                    candidates.add(match.group(1))
        return candidates

    @classmethod
    def process(cls, c_path, args):
        '''Run GCC preprocessor and return an iterator MacroSymbol.'''
        gcc = ['gcc', '-E', '-dM', c_path]
        gcc.extend(args or ())
        macros = StringIO(subprocess.check_output(gcc))
        for define_line in macros:
            match = cls.REGEX_DEFINE.match(define_line)
            if not match:
                continue
            name = match.group(1)
            args, body = cls._parse_value(define_line[match.end():])
            yield cls(name=name, args=args, body=body, expr=None)

    @classmethod
    def _parse_value(cls, value):
        '''Parse macro value.'''
        match = cls.REGEX_ARGUMENTS.match(value)
        if not match:
            return None, value.strip()
        args_str = match.group(1)
        if args_str:
            args = tuple(arg.strip() for arg in args_str.split(','))
        else:
            args = ()
        body = value[match.end():].strip()
        return args, body

    @classmethod
    def set_expr(cls, symbol, expr):
        '''Add expr to a MacroSymbol.'''
        return cls(name=symbol.name, args=symbol.args, body=symbol.body,
                expr=expr)

    @property
    def macro(self):
        '''Return C marco.'''
        if self.args is None:
            return '#define %s %s' % (self.name, self.body)
        args_list = ', '.join(self.args)
        return '#define %s(%s) %s' % (self.name, args_list, self.body)


# A parser of a subset of C syntax is implemented for translating macro
# functions.  This should be good enough for the common cases.


class CSyntaxError(Exception):
    '''Raised when C syntax error.'''
    pass


class Parser:
    '''A parser of a subset of C expression syntax.'''

    # pylint: disable=R0903

    BINARY_OPERATOR_PRECEDENCE = (
            '||',
            '&&',
            '|',
            '^',
            '&',
            ('==', '!='),
            ('<', '>', '<=', '>='),
            ('<<', '>>'),
            ('+', '-'),
            ('*', '/', '%'),
            )

    def __init__(self):
        '''Initialize the object.'''
        self._tokens = None
        self._prev_token = None

    def parse(self, c_expr):
        '''Parse C expression.'''
        self._tokens = Token.get_tokens(c_expr)
        self._prev_token = None
        return self._expr_stmt()

    def _next(self):
        '''Return next token.'''
        if self._prev_token:
            token = self._prev_token
            self._prev_token = None
        else:
            try:
                token = self._tokens.next()
            except StopIteration:
                raise CSyntaxError('End of token sequence')
        return token

    def _putback(self, token):
        '''Put back this token.'''
        if self._prev_token is not None:
            raise CSyntaxError('Previous is not empty: %s' %
                    str(self._prev_token))
        self._prev_token = token

    def _may_match(self, *matches):
        '''Match an optional token.'''
        token = self._next()
        for match in matches:
            kind, spellings = match[0], match[1:]
            if kind and token.kind is not kind:
                continue
            if spellings and token.spelling not in spellings:
                continue
            return token
        # Not match, put the token back...
        self._putback(token)
        return None

    def _match(self, *matches):
        '''Match this token.'''
        token = self._may_match(*matches)
        if not token:
            raise CSyntaxError('Could not match %s' % str(matches))
        return token

    def _lookahead(self, *matches):
        '''Look ahead of token sequence.'''
        token = self._may_match(*matches)
        if token:
            # Put token back if it is matched...
            self._putback(token)
        return token

    def _expr_stmt(self):
        '''Parse expression statement.'''
        # Spacial case for string literal...
        this = self._may_match((Token.STR_LITERAL,))
        if this:
            parts = [this]
            while True:
                this = self._may_match((Token.STR_LITERAL,))
                if not this:
                    break
                parts.append(this)
            self._match((Token.END,))
            cat = Token(kind=Token.CAT, spelling=parts)
            return Expression(this=cat, children=())
        # It is quite common that a macro ends without semicolon...
        expr = self._cond_expr()
        semicolon = self._match((Token.MISC, ';'), (Token.END,))
        if semicolon.kind is not Token.END:
            self._match((Token.END,))
        return expr

    def _cond_expr(self):
        '''Parse conditional expression.'''
        cond = self._binop_expr(self.BINARY_OPERATOR_PRECEDENCE)
        qmark = self._may_match((Token.MISC, '?'))
        if not qmark:
            return cond
        true = self._cond_expr()
        self._match((Token.MISC, ':'))
        false = self._cond_expr()
        this = Token(kind=Token.TRIOP, spelling='?:')
        return Expression(this=this, children=(cond, true, false))

    def _binop_expr(self, binops):
        '''Parse binary operator expression.'''
        if not binops:
            return self._uniop_expr()
        left = self._binop_expr(binops[1:])
        if isinstance(binops[0], tuple):
            match_op = (Token.BINOP,) + binops[0]
        else:
            match_op = (Token.BINOP, binops[0])
        this = self._may_match(match_op)
        if not this:
            return left
        right = self._binop_expr(binops)
        return Expression(this=this, children=(left, right))

    def _uniop_expr(self):
        '''Parse uniary operator expression.'''
        operator = self._may_match((None, '+', '-', '~', '!'))
        if not operator:
            return self._postfix_expr()
        operand = self._uniop_expr()
        this = Token(kind=Token.UNIOP, spelling=operator.spelling)
        return Expression(this=this, children=(operand,))

    def _postfix_expr(self):
        '''Parse postfix expression.'''
        primary = self._primary_expr()
        if not self._may_match((Token.PARENTHESES, '(')):
            return primary
        args = self._arg_expr_list()
        self._match((Token.PARENTHESES, ')'))
        this = Token(kind=Token.FUNCTION, spelling='()')
        return Expression(this=this, children=(primary,) + args)

    def _arg_expr_list(self):
        '''Parse argument list.'''
        if self._lookahead((Token.PARENTHESES, ')')):
            # Empty argument list
            return ()
        args = []
        while True:
            args.append(self._cond_expr())
            if not self._may_match((Token.MISC, ',')):
                break
        return tuple(args)

    def _primary_expr(self):
        '''Parse primary expression.'''
        this = self._match((Token.PARENTHESES, '('),
                (Token.SYMBOL,),
                (Token.CHAR_LITERAL,),
                (Token.INT_LITERAL,),
                (Token.FP_LITERAL,))
        if this.kind is Token.PARENTHESES:
            expr = self._cond_expr()
            self._match((Token.PARENTHESES, ')'))
            par = Token(kind=Token.PARENTHESES, spelling='()')
            return Expression(this=par, children=(expr,))
        return Expression(this=this, children=())


class Expression(namedtuple('Expression', 'this children')):
    '''C expression.'''

    # pylint: disable=W0232,E1101

    def traverse(self, func):
        '''Traverse syntax tree.'''
        for child in self.children:
            child.traverse(func)
        func(self.this)

    def translate(self, output):
        '''Translate C expression to Python codes.'''
        if self.this.kind is Token.FUNCTION:
            self.children[0].translate(output)
            output.write('(')
            first = True
            for child in self.children[1:]:
                if not first:
                    output.write(', ')
                child.translate(output)
                first = False
            output.write(')')
        elif self.this.kind is Token.PARENTHESES:
            output.write('(')
            self.children[0].translate(output)
            output.write(')')
        elif self.this.kind is Token.TRIOP:
            self.children[1].translate(output)
            output.write(' if ')
            self.children[0].translate(output)
            output.write(' else ')
            self.children[2].translate(output)
        elif self.this.kind is Token.BINOP:
            self.children[0].translate(output)
            output.write(' ')
            self.this.translate(output)
            output.write(' ')
            self.children[1].translate(output)
        elif self.this.kind is Token.UNIOP:
            if self.this.spelling == '!':
                output.write('not ')
            else:
                output.write(self.this.spelling)
            self.children[0].translate(output)
        else:
            self.this.translate(output)


class Token(namedtuple('Token', 'kind spelling')):
    '''C token.'''

    # pylint: disable=W0232,E1101

    REGEX_TOKEN = re.compile(r'''
            (?P<symbol>[a-zA-Z_]\w*) |
            (?P<string_literal>
                \w?"(?:\\"|[^"])*"
            ) |
            (?P<char_literal>\w?'(?:[^']|\')+') |
            # Floating-point literal must be listed before integer literal...
            (?P<floating_point_literal>
                \d*\.\d+(?:[eE][+\-]?\d+)?[fFlL]? |
                \d+\.\d*(?:[eE][+\-]?\d+)?[fFlL]?
            ) |
            (?P<integer_literal>
                0[xX][a-fA-F0-9]+[uUlL]* |
                0\d+[uUlL]* |
                \d+[uUlL]* |
                \d+[eE][+\-]?\d+[fFlL]?
            ) |
            (?P<binary_operator>
                # &&, ||, and -> has to be placed first...
                && | \|\| | -> |
                (?:>>|<<|[+\-*/%&\^|<>=!])=?
            ) |
            (?P<parentheses>
                [()\[\]{}]
            ) |
            (?P<misc>
                [,;:?]
            ) |
            # Ignore the following kinds of tokens for now...
            \+\+ | -- |
            ~ | <% | %> | <: | :> |
            \.\.\. |
            \s+
            ''', re.VERBOSE)

    FUNCTION        = 'FUNCTION'
    SYMBOL          = 'SYMBOL'
    TRIOP           = 'TRIOP'
    BINOP           = 'BINOP'
    UNIOP           = 'UNIOP'
    CHAR_LITERAL    = 'CHAR_LITERAL'
    STR_LITERAL     = 'STR_LITERAL'
    INT_LITERAL     = 'INT_LITERAL'
    FP_LITERAL      = 'FP_LITERAL'
    PARENTHESES     = 'PARENTHESES'
    MISC            = 'MISC'
    CAT             = 'CAT'
    END             = 'END'

    @classmethod
    def get_tokens(cls, c_expr):
        '''Make token list from C expression.'''
        pos = 0
        while True:
            match = cls.REGEX_TOKEN.match(c_expr, pos)
            if not match:
                break
            pos = match.end()
            for gname, kind in (
                    ('symbol',                  cls.SYMBOL),
                    ('char_literal',            cls.CHAR_LITERAL),
                    ('string_literal',          cls.STR_LITERAL),
                    ('integer_literal',         cls.INT_LITERAL),
                    ('floating_point_literal',  cls.FP_LITERAL),
                    ('binary_operator',         cls.BINOP),
                    ('parentheses',             cls.PARENTHESES),
                    ('misc',                    cls.MISC),
                    ):
                spelling = match.group(gname)
                if spelling:
                    yield cls(kind=kind, spelling=spelling)
                    break
        yield cls(kind=cls.END, spelling=None)

    def translate(self, output):
        '''Translate this token to Python codes.'''
        if self.kind is self.CHAR_LITERAL:
            output.write('ord(%s)' % self.spelling)
        elif self.kind is self.BINOP and self.spelling == '&&':
            output.write('and')
        elif self.kind is self.BINOP and self.spelling == '||':
            output.write('or')
        elif self.kind is self.INT_LITERAL or self.kind is self.FP_LITERAL:
            output.write(self.spelling.rstrip('fFuUlL'))
        elif self.kind is self.CAT:
            self.spelling[0].translate(output)
            for part in self.spelling[1:]:
                output.write(' ')
                part.translate(output)
        else:
            output.write(self.spelling)
