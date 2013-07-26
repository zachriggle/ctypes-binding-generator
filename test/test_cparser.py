'''Unit tests of C expression tokenizer.'''

import unittest
from cStringIO import StringIO

from cbind.macro_const import Token, Expression, Parser


class TestToken(unittest.TestCase):

    def run_test(self, c_expr, *answer_tokens):
        output_tokens = tuple(Token.get_tokens(c_expr))
        msg = ('%d != %d:\n%s\n%s\n' %
                (len(output_tokens), len(answer_tokens),
                    output_tokens, answer_tokens))
        self.assertEqual(len(output_tokens), len(answer_tokens), msg)
        for output, answer in zip(output_tokens, answer_tokens):
            msg = '%s != %s' % (output, answer)
            self.assertEqual(output, answer, msg)

    def test_tokenizer(self):
        self.run_test('''
                __file__
                "\\"hello world\\""
                '\\''
                3.14
                + - * /
                1ul
                () [] {}
                ''',
                Token(Token.SYMBOL, '__file__'),
                Token(Token.STR_LITERAL, '"\\"hello world\\""'),
                Token(Token.CHAR_LITERAL, '\'\\\'\''),
                Token(Token.FP_LITERAL, '3.14'),
                Token(Token.BINOP, '+'),
                Token(Token.BINOP, '-'),
                Token(Token.BINOP, '*'),
                Token(Token.BINOP, '/'),
                Token(Token.INT_LITERAL, '1ul'),
                Token(Token.PARENTHESES, '('), Token(Token.PARENTHESES, ')'),
                Token(Token.PARENTHESES, '['), Token(Token.PARENTHESES, ']'),
                Token(Token.PARENTHESES, '{'), Token(Token.PARENTHESES, '}'),
                Token(Token.END, None),
                )


class TestExpression(unittest.TestCase):

    def compare_expr(self, output, answer):
        if isinstance(answer, str):
            self.assertEqual(output.this.spelling, answer)
        else:
            self.assertEqual(output.this.spelling, answer[0])
        if isinstance(answer, str) or len(answer) == 1:
            self.assertIsNone(output.left)
            self.assertIsNone(output.right)
            return
        self.compare_expr(output.left, answer[1])
        self.compare_expr(output.right, answer[2])

    def run_test(self, c_expr, answer, py_expr=None):
        parser = Parser()
        expr = parser.parse(c_expr)
        self.compare_expr(expr, answer)
        output = StringIO()
        expr.translate(output)
        self.assertEqual(output.getvalue(), py_expr or c_expr)

    def test_simple_expr(self):
        self.run_test('xx + yy * zz - (1 - 3.14) / a',
                ('+',
                    'xx',
                    ('-',
                        ('*', 'yy', 'zz'),
                        ('/',
                            ('-', '1', '3.14'),
                            'a'
                            )
                        )
                    )
                )