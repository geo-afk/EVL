from enum import Enum, auto


class EvalType(Enum):
    INT    = auto()
    FLOAT  = auto()
    STRING = auto()
    BOOL   = auto()
    NULL   = auto()
    UNKNOWN = auto()   # propagates on error to suppress cascade errors


# Map keyword strings → EvalType
TYPE_MAP: dict[str, EvalType] = {
    "int":    EvalType.INT,
    "float":  EvalType.FLOAT,
    "string": EvalType.STRING,
    "bool":   EvalType.BOOL,
}

# Numeric types
NUMERIC   = {EvalType.INT, EvalType.FLOAT}


# Empty TYPE
NULL = {EvalType.UNKNOWN, None}

