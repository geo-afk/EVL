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
    "==": _op.eq,
    "!=": _op.ne,
}


def _strip_quotes(s: str) -> str:
    """Remove a single layer of surrounding single or double quotes."""
    s = s.strip()
    if len(s) >= 2 and s[0] in ('"', "'") and s[-1] == s[0]:
        return s[1:-1]
    return s


class Evaluator:

    @staticmethod
    def cast(
        value: int | float | str | bool,
        target_type: EvalType,
    ) -> int | float | str | bool | None:
        return TypeHandler.convert(value, target_type)

    @staticmethod
    def evaluate_relational(
        left_val: int | float,
        operator: str,
        right_val: int | float,
    ) -> bool:
        try:
            fn = _RELATIONAL_OPS[operator]
        except KeyError:
            raise ValueError(
                f"Unknown relational operator {operator!r}. "
                f"Valid operators: {list(_RELATIONAL_OPS)}"
            )
        return fn(left_val, right_val)

    @staticmethod
    def coerce_to_declared_type(
        val: Any,
        decl_type: EvalType,
        val_type: EvalType,
        name: str,
        type_text: str,
    ) -> Any:
        # NULL is assignable to any type — check before anything else
        if val_type == EvalType.NULL:
            return val

        # Exact match — nothing to do
        if decl_type == val_type:
            return val

        # ── Numeric coercions ────────────────────────────────────────────────

        # Widening: int → float (always safe)
        if decl_type == EvalType.FLOAT and val_type == EvalType.INT:
            return float(val)

        # Narrowing: float → int (may lose precision)
        if decl_type == EvalType.INT and val_type == EvalType.FLOAT:
            try:
                return int(val)
            except (ValueError, TypeError):
                raise CoercionException(
                    f"Cannot narrow float value {val!r} to int "
                    f"for variable '{name}'"
                )

        # ── String → numeric coercions ───────────────────────────────────────

        if val_type == EvalType.STRING:
            cleaned = _strip_quotes(str(val))

            if decl_type == EvalType.INT:
                try:
                    # Accept "3.0"-style strings by going via float first
                    as_float = float(cleaned)
                    if not as_float.is_integer():
                        raise CoercionException(
                            f"Cannot convert string {val!r} to int without "
                            f"losing precision for variable '{name}'"
                        )
                    return int(as_float)
                except (ValueError, TypeError):
                    raise CoercionException(
                        f"Cannot convert string {val!r} to int "
                        f"for variable '{name}'"
                    )

            if decl_type == EvalType.FLOAT:
                try:
                    return float(cleaned)
                except (ValueError, TypeError):
                    raise CoercionException(
                        f"Cannot convert string {val!r} to float "
                        f"for variable '{name}'"
                    )

        # ── Hard type mismatch ───────────────────────────────────────────────
        raise CoercionException(
            f"Cannot initialise '{type_text}' variable '{name}' "
            f"with value of type '{val_type.name}'"
        )

    @staticmethod
    def apply_compound_op(
            op: str,
            cur_val: int | float,
            rhs_val: int | float,
    ) -> tuple[Any, str | None]:

        if op == "+=":
            return cur_val + rhs_val, None
        elif op == "-=":
            return cur_val - rhs_val, None
        elif op == "*=":
            return cur_val * rhs_val, None
        elif op == "/=":
            if rhs_val == 0:
                return None, "division by zero"
            return cur_val / rhs_val, None
        return None, f"unknown compound operator '{op}'"

    @staticmethod
    def coerce_for_assignment(
            val: Any,
            decl_type: EvalType,
            val_type: EvalType,
            name: str,
    ) -> tuple[Any, str | None]:
        """
        Coerces *val* to *decl_type* for an assignment statement.

        Returns (coerced_value, None) on success,
        or      (original_val, error_message) on failure.
        """
        try:
            result = Evaluator.coerce_to_declared_type(
                val=val,
                decl_type=decl_type,
                val_type=val_type,
                name=name,
                type_text=decl_type.value,
            )
            return result, None
        except CoercionException as e:
            return val, str(e)