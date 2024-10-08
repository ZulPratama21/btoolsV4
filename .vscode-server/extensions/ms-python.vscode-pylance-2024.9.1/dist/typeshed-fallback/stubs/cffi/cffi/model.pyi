from _typeshed import Incomplete
from collections.abc import Generator

from .error import CDefError as CDefError, VerificationError as VerificationError, VerificationMissing as VerificationMissing
from .lock import allocate_lock as allocate_lock

Q_CONST: int
Q_RESTRICT: int
Q_VOLATILE: int

def qualify(quals, replace_with): ...

class BaseTypeByIdentity:
    is_array_type: bool
    is_raw_function: bool
    def get_c_name(self, replace_with: str = "", context: str = "a C file", quals: int = 0): ...
    def has_c_name(self): ...
    def is_integer_type(self): ...
    def get_cached_btype(self, ffi, finishlist, can_delay: bool = False): ...

class BaseType(BaseTypeByIdentity):
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __hash__(self) -> int: ...

class VoidType(BaseType):
    c_name_with_marker: str
    def __init__(self) -> None: ...
    def build_backend_type(self, ffi, finishlist): ...

void_type: Incomplete

class BasePrimitiveType(BaseType):
    def is_complex_type(self): ...

class PrimitiveType(BasePrimitiveType):
    ALL_PRIMITIVE_TYPES: Incomplete
    name: Incomplete
    c_name_with_marker: Incomplete
    def __init__(self, name) -> None: ...
    def is_char_type(self): ...
    def is_integer_type(self): ...
    def is_float_type(self): ...
    def is_complex_type(self): ...
    def build_backend_type(self, ffi, finishlist): ...

class UnknownIntegerType(BasePrimitiveType):
    name: Incomplete
    c_name_with_marker: Incomplete
    def __init__(self, name) -> None: ...
    def is_integer_type(self): ...
    def build_backend_type(self, ffi, finishlist) -> None: ...

class UnknownFloatType(BasePrimitiveType):
    name: Incomplete
    c_name_with_marker: Incomplete
    def __init__(self, name) -> None: ...
    def build_backend_type(self, ffi, finishlist) -> None: ...

class BaseFunctionType(BaseType):
    args: Incomplete
    result: Incomplete
    ellipsis: Incomplete
    abi: Incomplete
    c_name_with_marker: Incomplete
    def __init__(self, args, result, ellipsis, abi: Incomplete | None = None) -> None: ...

class RawFunctionType(BaseFunctionType):
    is_raw_function: bool
    def build_backend_type(self, ffi, finishlist) -> None: ...
    def as_function_pointer(self): ...

class FunctionPtrType(BaseFunctionType):
    def build_backend_type(self, ffi, finishlist): ...
    def as_raw_function(self): ...

class PointerType(BaseType):
    totype: Incomplete
    quals: Incomplete
    c_name_with_marker: Incomplete
    def __init__(self, totype, quals: int = 0) -> None: ...
    def build_backend_type(self, ffi, finishlist): ...

voidp_type: Incomplete

def ConstPointerType(totype): ...

const_voidp_type: Incomplete

class NamedPointerType(PointerType):
    name: Incomplete
    c_name_with_marker: Incomplete
    def __init__(self, totype, name, quals: int = 0) -> None: ...

class ArrayType(BaseType):
    is_array_type: bool
    item: Incomplete
    length: Incomplete
    c_name_with_marker: Incomplete
    def __init__(self, item, length) -> None: ...
    def length_is_unknown(self): ...
    def resolve_length(self, newlength): ...
    def build_backend_type(self, ffi, finishlist): ...

char_array_type: Incomplete

class StructOrUnionOrEnum(BaseTypeByIdentity):
    forcename: Incomplete
    c_name_with_marker: Incomplete
    def build_c_name_with_marker(self) -> None: ...
    def force_the_name(self, forcename) -> None: ...
    def get_official_name(self): ...

class StructOrUnion(StructOrUnionOrEnum):
    fixedlayout: Incomplete
    completed: int
    partial: bool
    packed: int
    name: Incomplete
    fldnames: Incomplete
    fldtypes: Incomplete
    fldbitsize: Incomplete
    fldquals: Incomplete
    def __init__(self, name, fldnames, fldtypes, fldbitsize, fldquals: Incomplete | None = None) -> None: ...
    def anonymous_struct_fields(self) -> Generator[Incomplete, None, None]: ...
    def enumfields(self, expand_anonymous_struct_union: bool = True) -> Generator[Incomplete, None, None]: ...
    def force_flatten(self) -> None: ...
    def get_cached_btype(self, ffi, finishlist, can_delay: bool = False): ...
    def finish_backend_type(self, ffi, finishlist) -> None: ...
    def check_not_partial(self) -> None: ...
    def build_backend_type(self, ffi, finishlist): ...

class StructType(StructOrUnion):
    kind: str

class UnionType(StructOrUnion):
    kind: str

class EnumType(StructOrUnionOrEnum):
    kind: str
    partial: bool
    partial_resolved: bool
    name: Incomplete
    enumerators: Incomplete
    enumvalues: Incomplete
    baseinttype: Incomplete
    def __init__(self, name, enumerators, enumvalues, baseinttype: Incomplete | None = None) -> None: ...
    forcename: Incomplete
    def force_the_name(self, forcename) -> None: ...
    def check_not_partial(self) -> None: ...
    def build_backend_type(self, ffi, finishlist): ...
    def build_baseinttype(self, ffi, finishlist): ...

def unknown_type(name, structname: Incomplete | None = None): ...
def unknown_ptr_type(name, structname: Incomplete | None = None): ...

global_lock: Incomplete

def get_typecache(backend): ...
def global_cache(srctype, ffi, funcname, *args, **kwds): ...
def pointer_cache(ffi, BType): ...
def attach_exception_info(e, name) -> None: ...
