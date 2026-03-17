import operator as _op
from typing import Any

from app.eval.variable_manager import VariableManager
from app.models.Types import EvalType, TypeHandler
from app.models.custom_exceptions import CoercionException

_RELATIONAL_OPS: dict[str, Any] = {
    "<":  _op.lt,
    ">":  _op.gt,
    "<=": _op.le,
    ">=": _op.ge,
}


class Evaluator:
    @staticmethod
    def evaluate(target_text: Any) -> int | float | str | None:
        """
        Coerce *target_text* to its natural Python numeric type.
        Returns None for any value that is not int, float, or str.
        """
        if type(target_text) is int:
            return int(target_text)
        if type(target_text) is float:
            return float(target_text)
        if type(target_text) is str:
            return target_text
        return None

    @staticmethod
    def cast(value: int | float | str | bool, target_type: EvalType) -> int | float | str | bool | None:
        _CAST_MAP: dict[EvalType, type] = {
            EvalType.INT: int,
            EvalType.FLOAT: float,
            EvalType.STRING: str,
            EvalType.BOOL: bool,
        }

        value = TypeHandler.convert(value, target_type)
        return value

    @staticmethod
    def evaluate_relational(left_val: int | float, operator: str, right_val: int | float) -> bool:
        return _RELATIONAL_OPS[operator](left_val, right_val)


    @staticmethod
    def coerce_to_declared_type(
            val: Any,
            decl_type: EvalType,
            val_type: EvalType,
            name: str,
            type_text: str,
    ) -> Any:

        if decl_type == val_type:
            return val

        # Widening: int value → float variable (always safe)
        if decl_type == EvalType.FLOAT and val_type == EvalType.INT:
            return float(val)

        # Narrowing: float value → int variable (may lose precision / fail)
        if decl_type == EvalType.INT and val_type == EvalType.FLOAT:
            try:
                return int(val)
            except (ValueError, TypeError):
                raise CoercionException(
                    f"cannot narrow float value '{val!r}' to int "
                    f"for variable '{name}'"
                )

        # NULL is assignable to any type
        if val_type == EvalType.NULL:
            return val

        # Everything else is a hard type mismatch
        raise CoercionException(
            f"cannot initialise '{type_text}' variable '{name}' "
            f"with value of type '{val_type.name}'"
        )
