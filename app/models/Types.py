from enum import Enum
from typing import Any


class EvalType(str, Enum):
    INT     = "int"
    FLOAT   = "float"
    STRING  = "string"
    BOOL    = "bool"
    NULL    = "null"
    UNKNOWN = "unknown"


class TypeHandler:
    _TYPE_HANDLERS = {
        EvalType.INT:    lambda x: int(x),
        EvalType.FLOAT:  lambda x: float(x),
        EvalType.STRING: lambda x: str(x),
        EvalType.BOOL:   lambda x: bool(x),
    }

    # Numeric types
    NUMERIC = {EvalType.INT, EvalType.FLOAT}

    # Empty / sentinel types
    EMPTY = {EvalType.UNKNOWN, EvalType.NULL}

    @staticmethod
    def convert(value: Any, type_enum: "EvalType") -> Any:
        handler = TypeHandler._TYPE_HANDLERS.get(type_enum)
        return handler(value) if handler else None

    @staticmethod
    def is_valid_type(type_string: str) -> bool:
        return type_string in [t.value for t in EvalType]

    @staticmethod
    def is_python_type(eval_type: Any) -> type:
        python_type_map = {
            EvalType.INT:    int,
            EvalType.FLOAT:  float,
            EvalType.STRING: str,
            EvalType.BOOL:   bool,
        }
        return python_type_map.get(eval_type, object)

    @staticmethod
    def get_eval_type(str_type: str) -> "EvalType":
        if TypeHandler.is_valid_type(str_type):
            return EvalType(str_type)
        return EvalType.UNKNOWN
