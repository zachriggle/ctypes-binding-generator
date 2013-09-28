# This is generated by cbind and should not be edited.

import sys as _python_sys
from ctypes import *

# pylint: disable-all
from cbind.compatibility import decode_str
from cbind.min_cindex_helper import (check_cursor,
                                     ref_translation_unit,
                                     Index,
                                     CursorMixin,
                                     SourceLocationMixin,
                                     TypeMixin,
                                     EnumerateKindMixin)

if _python_sys.platform == 'darwin':
    _lib = cdll.LoadLibrary('libclang.dylib')
elif _python_sys.platform == 'win32' or _python_sys.platform == 'cygwin':
    _lib = cdll.LoadLibrary('libclang.dll')
else:
    _lib = cdll.LoadLibrary('libclang.so')


import types as _python_types

class _CtypesFunctor(object):
    def __init__(self, functor):
        self.functor = functor

    if _python_sys.version_info.major == 3:
        def __get__(self, obj, objtype=None):
            if obj is None:
                return self.functor
            else:
                return _python_types.MethodType(self.functor, obj)

    else:
        def __get__(self, obj, objtype=None):
            return _python_types.MethodType(self.functor, obj, objtype)

class String(Structure):
    pass
String._fields_ = [('data', c_void_p),
                   ('private_flags', c_uint)]

clang_getCString = _lib.clang_getCString
clang_getCString.argtypes = [String]
clang_getCString.restype = c_char_p

clang_disposeString = _lib.clang_disposeString
clang_disposeString.argtypes = [String]
String.__del__ = _CtypesFunctor(clang_disposeString)

class TranslationUnitImpl(Structure):
    pass

class UnsavedFile(Structure):
    pass
UnsavedFile._fields_ = [('Filename', c_char_p),
                        ('Contents', c_char_p),
                        ('Length', c_ulong)]

clang_createIndex = _lib.clang_createIndex
clang_createIndex.argtypes = [c_int, c_int]
clang_createIndex.restype = c_void_p

clang_disposeIndex = _lib.clang_disposeIndex
clang_disposeIndex.argtypes = [c_void_p]

clang_getFileName = _lib.clang_getFileName
clang_getFileName.argtypes = [c_void_p]
clang_getFileName.restype = String
clang_getFileName.errcheck = lambda result, *_: decode_str(clang_getCString(result))

class SourceLocation(SourceLocationMixin, Structure):
    pass
SourceLocation._fields_ = [('ptr_data', (c_void_p * 2)),
                           ('int_data', c_uint)]

clang_getInstantiationLocation = _lib.clang_getInstantiationLocation
clang_getInstantiationLocation.argtypes = [SourceLocation, POINTER(c_void_p), POINTER(c_uint), POINTER(c_uint), POINTER(c_uint)]

class DiagnosticSeverity(c_uint):
    pass

clang_getNumDiagnostics = _lib.clang_getNumDiagnostics
clang_getNumDiagnostics.argtypes = [POINTER(TranslationUnitImpl)]
clang_getNumDiagnostics.restype = c_uint

clang_getDiagnostic = _lib.clang_getDiagnostic
clang_getDiagnostic.argtypes = [POINTER(TranslationUnitImpl), c_uint]
clang_getDiagnostic.restype = c_void_p

clang_disposeDiagnostic = _lib.clang_disposeDiagnostic
clang_disposeDiagnostic.argtypes = [c_void_p]

clang_getDiagnosticSeverity = _lib.clang_getDiagnosticSeverity
clang_getDiagnosticSeverity.argtypes = [c_void_p]
clang_getDiagnosticSeverity.restype = DiagnosticSeverity

clang_getDiagnosticLocation = _lib.clang_getDiagnosticLocation
clang_getDiagnosticLocation.argtypes = [c_void_p]
clang_getDiagnosticLocation.restype = SourceLocation

clang_getDiagnosticSpelling = _lib.clang_getDiagnosticSpelling
clang_getDiagnosticSpelling.argtypes = [c_void_p]
clang_getDiagnosticSpelling.restype = String
clang_getDiagnosticSpelling.errcheck = lambda result, *_: decode_str(clang_getCString(result))

clang_parseTranslationUnit = _lib.clang_parseTranslationUnit
clang_parseTranslationUnit.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), c_int, POINTER(UnsavedFile), c_uint, c_uint]
clang_parseTranslationUnit.restype = POINTER(TranslationUnitImpl)

clang_disposeTranslationUnit = _lib.clang_disposeTranslationUnit
clang_disposeTranslationUnit.argtypes = [POINTER(TranslationUnitImpl)]

class CursorKind(EnumerateKindMixin, c_uint):
    pass
CursorKind.register("UNEXPOSED_DECL", 1)
CursorKind.register("STRUCT_DECL", 2)
CursorKind.register("UNION_DECL", 3)
CursorKind.register("CLASS_DECL", 4)
CursorKind.register("ENUM_DECL", 5)
CursorKind.register("FIELD_DECL", 6)
CursorKind.register("ENUM_CONSTANT_DECL", 7)
CursorKind.register("FUNCTION_DECL", 8)
CursorKind.register("VAR_DECL", 9)
CursorKind.register("PARM_DECL", 10)
CursorKind.register("OBJ_CINTERFACE_DECL", 11)
CursorKind.register("OBJ_CCATEGORY_DECL", 12)
CursorKind.register("OBJ_CPROTOCOL_DECL", 13)
CursorKind.register("OBJ_CPROPERTY_DECL", 14)
CursorKind.register("OBJ_CIVAR_DECL", 15)
CursorKind.register("OBJ_CINSTANCE_METHOD_DECL", 16)
CursorKind.register("OBJ_CCLASS_METHOD_DECL", 17)
CursorKind.register("OBJ_CIMPLEMENTATION_DECL", 18)
CursorKind.register("OBJ_CCATEGORY_IMPL_DECL", 19)
CursorKind.register("TYPEDEF_DECL", 20)
CursorKind.register("CXX_METHOD", 21)
CursorKind.register("NAMESPACE", 22)
CursorKind.register("LINKAGE_SPEC", 23)
CursorKind.register("CONSTRUCTOR", 24)
CursorKind.register("DESTRUCTOR", 25)
CursorKind.register("CONVERSION_FUNCTION", 26)
CursorKind.register("TEMPLATE_TYPE_PARAMETER", 27)
CursorKind.register("NON_TYPE_TEMPLATE_PARAMETER", 28)
CursorKind.register("TEMPLATE_TEMPLATE_PARAMETER", 29)
CursorKind.register("FUNCTION_TEMPLATE", 30)
CursorKind.register("CLASS_TEMPLATE", 31)
CursorKind.register("CLASS_TEMPLATE_PARTIAL_SPECIALIZATION", 32)
CursorKind.register("NAMESPACE_ALIAS", 33)
CursorKind.register("USING_DIRECTIVE", 34)
CursorKind.register("USING_DECLARATION", 35)
CursorKind.register("TYPE_ALIAS_DECL", 36)
CursorKind.register("OBJ_CSYNTHESIZE_DECL", 37)
CursorKind.register("OBJ_CDYNAMIC_DECL", 38)
CursorKind.register("CXX_ACCESS_SPECIFIER", 39)
CursorKind.register("FIRST_DECL", 1)
CursorKind.register("LAST_DECL", 39)
CursorKind.register("FIRST_REF", 40)
CursorKind.register("OBJ_CSUPER_CLASS_REF", 40)
CursorKind.register("OBJ_CPROTOCOL_REF", 41)
CursorKind.register("OBJ_CCLASS_REF", 42)
CursorKind.register("TYPE_REF", 43)
CursorKind.register("CXX_BASE_SPECIFIER", 44)
CursorKind.register("TEMPLATE_REF", 45)
CursorKind.register("NAMESPACE_REF", 46)
CursorKind.register("MEMBER_REF", 47)
CursorKind.register("LABEL_REF", 48)
CursorKind.register("OVERLOADED_DECL_REF", 49)
CursorKind.register("VARIABLE_REF", 50)
CursorKind.register("LAST_REF", 50)
CursorKind.register("FIRST_INVALID", 70)
CursorKind.register("INVALID_FILE", 70)
CursorKind.register("NO_DECL_FOUND", 71)
CursorKind.register("NOT_IMPLEMENTED", 72)
CursorKind.register("INVALID_CODE", 73)
CursorKind.register("LAST_INVALID", 73)
CursorKind.register("FIRST_EXPR", 100)
CursorKind.register("UNEXPOSED_EXPR", 100)
CursorKind.register("DECL_REF_EXPR", 101)
CursorKind.register("MEMBER_REF_EXPR", 102)
CursorKind.register("CALL_EXPR", 103)
CursorKind.register("OBJ_CMESSAGE_EXPR", 104)
CursorKind.register("BLOCK_EXPR", 105)
CursorKind.register("INTEGER_LITERAL", 106)
CursorKind.register("FLOATING_LITERAL", 107)
CursorKind.register("IMAGINARY_LITERAL", 108)
CursorKind.register("STRING_LITERAL", 109)
CursorKind.register("CHARACTER_LITERAL", 110)
CursorKind.register("PAREN_EXPR", 111)
CursorKind.register("UNARY_OPERATOR", 112)
CursorKind.register("ARRAY_SUBSCRIPT_EXPR", 113)
CursorKind.register("BINARY_OPERATOR", 114)
CursorKind.register("COMPOUND_ASSIGN_OPERATOR", 115)
CursorKind.register("CONDITIONAL_OPERATOR", 116)
CursorKind.register("CSTYLE_CAST_EXPR", 117)
CursorKind.register("COMPOUND_LITERAL_EXPR", 118)
CursorKind.register("INIT_LIST_EXPR", 119)
CursorKind.register("ADDR_LABEL_EXPR", 120)
CursorKind.register("STMT_EXPR", 121)
CursorKind.register("GENERIC_SELECTION_EXPR", 122)
CursorKind.register("GNUNULL_EXPR", 123)
CursorKind.register("CXX_STATIC_CAST_EXPR", 124)
CursorKind.register("CXX_DYNAMIC_CAST_EXPR", 125)
CursorKind.register("CXX_REINTERPRET_CAST_EXPR", 126)
CursorKind.register("CXX_CONST_CAST_EXPR", 127)
CursorKind.register("CXX_FUNCTIONAL_CAST_EXPR", 128)
CursorKind.register("CXX_TYPEID_EXPR", 129)
CursorKind.register("CXX_BOOL_LITERAL_EXPR", 130)
CursorKind.register("CXX_NULL_PTR_LITERAL_EXPR", 131)
CursorKind.register("CXX_THIS_EXPR", 132)
CursorKind.register("CXX_THROW_EXPR", 133)
CursorKind.register("CXX_NEW_EXPR", 134)
CursorKind.register("CXX_DELETE_EXPR", 135)
CursorKind.register("UNARY_EXPR", 136)
CursorKind.register("OBJ_CSTRING_LITERAL", 137)
CursorKind.register("OBJ_CENCODE_EXPR", 138)
CursorKind.register("OBJ_CSELECTOR_EXPR", 139)
CursorKind.register("OBJ_CPROTOCOL_EXPR", 140)
CursorKind.register("OBJ_CBRIDGED_CAST_EXPR", 141)
CursorKind.register("PACK_EXPANSION_EXPR", 142)
CursorKind.register("SIZE_OF_PACK_EXPR", 143)
CursorKind.register("LAMBDA_EXPR", 144)
CursorKind.register("OBJ_CBOOL_LITERAL_EXPR", 145)
CursorKind.register("OBJ_CSELF_EXPR", 146)
CursorKind.register("LAST_EXPR", 146)
CursorKind.register("FIRST_STMT", 200)
CursorKind.register("UNEXPOSED_STMT", 200)
CursorKind.register("LABEL_STMT", 201)
CursorKind.register("COMPOUND_STMT", 202)
CursorKind.register("CASE_STMT", 203)
CursorKind.register("DEFAULT_STMT", 204)
CursorKind.register("IF_STMT", 205)
CursorKind.register("SWITCH_STMT", 206)
CursorKind.register("WHILE_STMT", 207)
CursorKind.register("DO_STMT", 208)
CursorKind.register("FOR_STMT", 209)
CursorKind.register("GOTO_STMT", 210)
CursorKind.register("INDIRECT_GOTO_STMT", 211)
CursorKind.register("CONTINUE_STMT", 212)
CursorKind.register("BREAK_STMT", 213)
CursorKind.register("RETURN_STMT", 214)
CursorKind.register("GCCASM_STMT", 215)
CursorKind.register("ASM_STMT", 215)
CursorKind.register("OBJ_CAT_TRY_STMT", 216)
CursorKind.register("OBJ_CAT_CATCH_STMT", 217)
CursorKind.register("OBJ_CAT_FINALLY_STMT", 218)
CursorKind.register("OBJ_CAT_THROW_STMT", 219)
CursorKind.register("OBJ_CAT_SYNCHRONIZED_STMT", 220)
CursorKind.register("OBJ_CAUTORELEASE_POOL_STMT", 221)
CursorKind.register("OBJ_CFOR_COLLECTION_STMT", 222)
CursorKind.register("CXX_CATCH_STMT", 223)
CursorKind.register("CXX_TRY_STMT", 224)
CursorKind.register("CXX_FOR_RANGE_STMT", 225)
CursorKind.register("SEHTRY_STMT", 226)
CursorKind.register("SEHEXCEPT_STMT", 227)
CursorKind.register("SEHFINALLY_STMT", 228)
CursorKind.register("MSASM_STMT", 229)
CursorKind.register("NULL_STMT", 230)
CursorKind.register("DECL_STMT", 231)
CursorKind.register("OMPPARALLEL_DIRECTIVE", 232)
CursorKind.register("LAST_STMT", 232)
CursorKind.register("TRANSLATION_UNIT", 300)
CursorKind.register("FIRST_ATTR", 400)
CursorKind.register("UNEXPOSED_ATTR", 400)
CursorKind.register("IBACTION_ATTR", 401)
CursorKind.register("IBOUTLET_ATTR", 402)
CursorKind.register("IBOUTLET_COLLECTION_ATTR", 403)
CursorKind.register("CXX_FINAL_ATTR", 404)
CursorKind.register("CXX_OVERRIDE_ATTR", 405)
CursorKind.register("ANNOTATE_ATTR", 406)
CursorKind.register("ASM_LABEL_ATTR", 407)
CursorKind.register("LAST_ATTR", 407)
CursorKind.register("PREPROCESSING_DIRECTIVE", 500)
CursorKind.register("MACRO_DEFINITION", 501)
CursorKind.register("MACRO_EXPANSION", 502)
CursorKind.register("MACRO_INSTANTIATION", 502)
CursorKind.register("INCLUSION_DIRECTIVE", 503)
CursorKind.register("FIRST_PREPROCESSING", 500)
CursorKind.register("LAST_PREPROCESSING", 503)
CursorKind.register("MODULE_IMPORT_DECL", 600)
CursorKind.register("FIRST_EXTRA_DECL", 600)
CursorKind.register("LAST_EXTRA_DECL", 600)

class Cursor(CursorMixin, Structure):
    pass
Cursor._fields_ = [('kind', CursorKind),
                   ('xdata', c_int),
                   ('data', (c_void_p * 3))]

clang_getNullCursor = _lib.clang_getNullCursor
clang_getNullCursor.restype = Cursor

clang_getTranslationUnitCursor = _lib.clang_getTranslationUnitCursor
clang_getTranslationUnitCursor.argtypes = [POINTER(TranslationUnitImpl)]
clang_getTranslationUnitCursor.restype = Cursor
clang_getTranslationUnitCursor.errcheck = check_cursor

clang_equalCursors = _lib.clang_equalCursors
clang_equalCursors.argtypes = [Cursor, Cursor]
clang_equalCursors.restype = c_uint

clang_hashCursor = _lib.clang_hashCursor
clang_hashCursor.argtypes = [Cursor]
clang_hashCursor.restype = c_uint

clang_isDeclaration = _lib.clang_isDeclaration
clang_isDeclaration.argtypes = [CursorKind]
clang_isDeclaration.restype = c_uint

class LinkageKind(EnumerateKindMixin, c_uint):
    pass
LinkageKind.register("INVALID", 0)
LinkageKind.register("NO_LINKAGE", 1)
LinkageKind.register("INTERNAL", 2)
LinkageKind.register("UNIQUE_EXTERNAL", 3)
LinkageKind.register("EXTERNAL", 4)

clang_getCursorLinkage = _lib.clang_getCursorLinkage
clang_getCursorLinkage.argtypes = [Cursor]
clang_getCursorLinkage.restype = LinkageKind

clang_getCursorSemanticParent = _lib.clang_getCursorSemanticParent
clang_getCursorSemanticParent.argtypes = [Cursor]
clang_getCursorSemanticParent.restype = Cursor
clang_getCursorSemanticParent.errcheck = check_cursor

clang_getCursorLocation = _lib.clang_getCursorLocation
clang_getCursorLocation.argtypes = [Cursor]
clang_getCursorLocation.restype = SourceLocation

class TypeKind(EnumerateKindMixin, c_uint):
    pass
TypeKind.register("INVALID", 0)
TypeKind.register("UNEXPOSED", 1)
TypeKind.register("VOID", 2)
TypeKind.register("BOOL", 3)
TypeKind.register("CHAR_U", 4)
TypeKind.register("UCHAR", 5)
TypeKind.register("CHAR16", 6)
TypeKind.register("CHAR32", 7)
TypeKind.register("USHORT", 8)
TypeKind.register("UINT", 9)
TypeKind.register("ULONG", 10)
TypeKind.register("ULONGLONG", 11)
TypeKind.register("UINT128", 12)
TypeKind.register("CHAR_S", 13)
TypeKind.register("SCHAR", 14)
TypeKind.register("WCHAR", 15)
TypeKind.register("SHORT", 16)
TypeKind.register("INT", 17)
TypeKind.register("LONG", 18)
TypeKind.register("LONGLONG", 19)
TypeKind.register("INT128", 20)
TypeKind.register("FLOAT", 21)
TypeKind.register("DOUBLE", 22)
TypeKind.register("LONGDOUBLE", 23)
TypeKind.register("NULLPTR", 24)
TypeKind.register("OVERLOAD", 25)
TypeKind.register("DEPENDENT", 26)
TypeKind.register("OBJCID", 27)
TypeKind.register("OBJCCLASS", 28)
TypeKind.register("OBJCSEL", 29)
TypeKind.register("FIRSTBUILTIN", 2)
TypeKind.register("LASTBUILTIN", 29)
TypeKind.register("COMPLEX", 100)
TypeKind.register("POINTER", 101)
TypeKind.register("BLOCKPOINTER", 102)
TypeKind.register("LVALUEREFERENCE", 103)
TypeKind.register("RVALUEREFERENCE", 104)
TypeKind.register("RECORD", 105)
TypeKind.register("ENUM", 106)
TypeKind.register("TYPEDEF", 107)
TypeKind.register("OBJCINTERFACE", 108)
TypeKind.register("OBJCOBJECTPOINTER", 109)
TypeKind.register("FUNCTIONNOPROTO", 110)
TypeKind.register("FUNCTIONPROTO", 111)
TypeKind.register("CONSTANTARRAY", 112)
TypeKind.register("VECTOR", 113)
TypeKind.register("INCOMPLETEARRAY", 114)
TypeKind.register("VARIABLEARRAY", 115)
TypeKind.register("DEPENDENTSIZEDARRAY", 116)
TypeKind.register("MEMBERPOINTER", 117)

class Type(TypeMixin, Structure):
    pass
Type._fields_ = [('kind', TypeKind),
                 ('data', (c_void_p * 2))]

clang_getCursorType = _lib.clang_getCursorType
clang_getCursorType.argtypes = [Cursor]
clang_getCursorType.restype = Type
clang_getCursorType.errcheck = ref_translation_unit

clang_getTypedefDeclUnderlyingType = _lib.clang_getTypedefDeclUnderlyingType
clang_getTypedefDeclUnderlyingType.argtypes = [Cursor]
clang_getTypedefDeclUnderlyingType.restype = Type
clang_getTypedefDeclUnderlyingType.errcheck = ref_translation_unit

clang_getEnumDeclIntegerType = _lib.clang_getEnumDeclIntegerType
clang_getEnumDeclIntegerType.argtypes = [Cursor]
clang_getEnumDeclIntegerType.restype = Type
clang_getEnumDeclIntegerType.errcheck = ref_translation_unit

clang_getEnumConstantDeclValue = _lib.clang_getEnumConstantDeclValue
clang_getEnumConstantDeclValue.argtypes = [Cursor]
clang_getEnumConstantDeclValue.restype = c_longlong

clang_getEnumConstantDeclUnsignedValue = _lib.clang_getEnumConstantDeclUnsignedValue
clang_getEnumConstantDeclUnsignedValue.argtypes = [Cursor]
clang_getEnumConstantDeclUnsignedValue.restype = c_ulonglong

clang_getFieldDeclBitWidth = _lib.clang_getFieldDeclBitWidth
clang_getFieldDeclBitWidth.argtypes = [Cursor]
clang_getFieldDeclBitWidth.restype = c_int
Cursor.get_bitfield_width = _CtypesFunctor(clang_getFieldDeclBitWidth)

clang_Cursor_getNumArguments = _lib.clang_Cursor_getNumArguments
clang_Cursor_getNumArguments.argtypes = [Cursor]
clang_Cursor_getNumArguments.restype = c_int
Cursor.get_num_arguments = _CtypesFunctor(clang_Cursor_getNumArguments)

clang_Cursor_getArgument = _lib.clang_Cursor_getArgument
clang_Cursor_getArgument.argtypes = [Cursor, c_uint]
clang_Cursor_getArgument.restype = Cursor
clang_Cursor_getArgument.errcheck = check_cursor

clang_getCanonicalType = _lib.clang_getCanonicalType
clang_getCanonicalType.argtypes = [Type]
clang_getCanonicalType.restype = Type
clang_getCanonicalType.errcheck = ref_translation_unit
Type.get_canonical = _CtypesFunctor(clang_getCanonicalType)

clang_isConstQualifiedType = _lib.clang_isConstQualifiedType
clang_isConstQualifiedType.argtypes = [Type]
clang_isConstQualifiedType.restype = c_uint
Type.is_const_qualified = _CtypesFunctor(clang_isConstQualifiedType)

clang_isVolatileQualifiedType = _lib.clang_isVolatileQualifiedType
clang_isVolatileQualifiedType.argtypes = [Type]
clang_isVolatileQualifiedType.restype = c_uint
Type.is_volatile_qualified = _CtypesFunctor(clang_isVolatileQualifiedType)

clang_getPointeeType = _lib.clang_getPointeeType
clang_getPointeeType.argtypes = [Type]
clang_getPointeeType.restype = Type
clang_getPointeeType.errcheck = ref_translation_unit
Type.get_pointee = _CtypesFunctor(clang_getPointeeType)

clang_getTypeDeclaration = _lib.clang_getTypeDeclaration
clang_getTypeDeclaration.argtypes = [Type]
clang_getTypeDeclaration.restype = Cursor
clang_getTypeDeclaration.errcheck = check_cursor
Type.get_declaration = _CtypesFunctor(clang_getTypeDeclaration)

clang_getResultType = _lib.clang_getResultType
clang_getResultType.argtypes = [Type]
clang_getResultType.restype = Type
clang_getResultType.errcheck = ref_translation_unit
Type.get_result = _CtypesFunctor(clang_getResultType)

clang_getNumArgTypes = _lib.clang_getNumArgTypes
clang_getNumArgTypes.argtypes = [Type]
clang_getNumArgTypes.restype = c_int

clang_getArgType = _lib.clang_getArgType
clang_getArgType.argtypes = [Type, c_uint]
clang_getArgType.restype = Type
clang_getArgType.errcheck = ref_translation_unit

clang_isFunctionTypeVariadic = _lib.clang_isFunctionTypeVariadic
clang_isFunctionTypeVariadic.argtypes = [Type]
clang_isFunctionTypeVariadic.restype = c_uint
Type.is_function_variadic = _CtypesFunctor(clang_isFunctionTypeVariadic)

clang_getElementType = _lib.clang_getElementType
clang_getElementType.argtypes = [Type]
clang_getElementType.restype = Type
clang_getElementType.errcheck = ref_translation_unit
Type.get_element_type = _CtypesFunctor(clang_getElementType)

clang_getArrayElementType = _lib.clang_getArrayElementType
clang_getArrayElementType.argtypes = [Type]
clang_getArrayElementType.restype = Type
clang_getArrayElementType.errcheck = ref_translation_unit
Type.get_array_element_type = _CtypesFunctor(clang_getArrayElementType)

clang_getArraySize = _lib.clang_getArraySize
clang_getArraySize.argtypes = [Type]
clang_getArraySize.restype = c_longlong
Type.get_array_size = _CtypesFunctor(clang_getArraySize)

clang_getClassType = _lib.clang_getClassType
clang_getClassType.argtypes = [Type]
clang_getClassType.restype = Type
clang_getClassType.errcheck = ref_translation_unit
Type.get_class_type = _CtypesFunctor(clang_getClassType)

clang_Type_getAlignOf = _lib.clang_Type_getAlignOf
clang_Type_getAlignOf.argtypes = [Type]
clang_Type_getAlignOf.restype = c_longlong
Type.get_align = _CtypesFunctor(clang_Type_getAlignOf)

clang_Type_getOffsetOf = _lib.clang_Type_getOffsetOf
clang_Type_getOffsetOf.argtypes = [Type, c_char_p]
clang_Type_getOffsetOf.restype = c_longlong
Type.get_offset = _CtypesFunctor(clang_Type_getOffsetOf)

clang_Cursor_isBitField = _lib.clang_Cursor_isBitField
clang_Cursor_isBitField.argtypes = [Cursor]
clang_Cursor_isBitField.restype = c_uint
Cursor.is_bitfield = _CtypesFunctor(clang_Cursor_isBitField)

class ChildVisitResult(c_uint):
    pass

clang_visitChildren = _lib.clang_visitChildren
clang_visitChildren.argtypes = [Cursor, CFUNCTYPE(ChildVisitResult, Cursor, Cursor, c_void_p), c_void_p]
clang_visitChildren.restype = c_uint

clang_getCursorSpelling = _lib.clang_getCursorSpelling
clang_getCursorSpelling.argtypes = [Cursor]
clang_getCursorSpelling.restype = String
clang_getCursorSpelling.errcheck = lambda result, *_: decode_str(clang_getCString(result))

clang_isCursorDefinition = _lib.clang_isCursorDefinition
clang_isCursorDefinition.argtypes = [Cursor]
clang_isCursorDefinition.restype = c_uint
Cursor.is_definition = _CtypesFunctor(clang_isCursorDefinition)

