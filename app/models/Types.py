from enum import Enum
from typing import Any


class EvalType(str, Enum):
    INT     = "int"
    FLOAT   = "float"
    STRING  = "string"
    BOOL    = "bool"
    NULL    = "null"
    UNKNOWN = "unknown"


def _strip_quotes(value: Any) -> str:
    """Strip a single layer of surrounding quotes from a string value."""
    s = str(value).strip()
    if len(s) >= 2 and s[0] in ('"', "'") and s[-1] == s[0]:
        return s[1:-1]
    return s


def _to_int(value: Any) -> int:
    """
    Convert value to int, handling:
      - quoted numeric strings  e.g. '"123"' or "'123'"
      - floats                  e.g. 3.99 → 3  (truncates toward zero)
    """
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    cleaned = _strip_quotes(value)
    try:
        return int(cleaned)
    except ValueError:
        return int(float(cleaned))


def _to_float(value: Any) -> float:
    """Convert value to float, stripping surrounding quotes when needed."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return float(_strip_quotes(value))


def _to_bool(value: Any) -> bool:
    """
    Convert value to bool.
    Accepts: True/False, 1/0, and case-insensitive 'true'/'false' strings.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    cleaned = _strip_quotes(value).lower()
    if cleaned == "true":
        return True
    if cleaned == "false":
        return False
    raise ValueError(f"Cannot convert {value!r} to bool")


class TypeHandler:
    _TYPE_HANDLERS = {
        EvalType.INT:    _to_int,
        EvalType.FLOAT:  _to_float,
        EvalType.STRING: lambda x: _strip_quotes(x) if isinstance(x, str) else str(x),
        EvalType.BOOL:   _to_bool,
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