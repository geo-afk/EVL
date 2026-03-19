from __future__ import annotations

from typing import Any, Tuple

from app.eval.handler.base_expression_handler import BaseExpressionHandler
from app.models.Variable import Variable
from generated.EVALParser import EVALParser


class ComparisonHandler(BaseExpressionHandler):
    """
    Resolves both operands of a relational expression and validates that
    they are numeric (int or float).

    The visitor already knows how to evaluate every expression kind:
      visitIntLiteral        → int
      visitRealLiteral       → float
      visitIdentExpr         → Variable  (unwrap to get the stored value)
      visitMacroExpr         → int | float  (PI, DAYS_IN_WEEK, HOURS_IN_DAY, YEAR)
      visitAdditiveExpr      → int | float
      visitMultiplicativeExpr→ int | float
      visitParenExpr         → delegates inward
      visitUnaryMinusExpr    → negated int | float
      visitBuiltinExpr       → result of sqrt / pow / abs / etc.

    This class does not reimplement any of that.  It calls visitor.visit()
    on each operand, unwraps the result, and checks it is numeric.

    Usage
    ─────
        handler = ComparisonHandler(
            left_expr  = ctx.expression(0),
            right_expr = ctx.expression(1),
            visitor    = self,
        )
        left_val, right_val = handler.check()   # raises ValueError if invalid
    """

    def __init__(
        self,
        left_expr:  EVALParser.ExpressionContext,
        right_expr: EVALParser.ExpressionContext,
        visitor:    Any = None,
    ) -> None:
        super().__init__(visitor=visitor)
        self.left_expr  = left_expr
        self.right_expr = right_expr

    # ── Public API ────────────────────────────────────────────────────────────

    def check(self) -> Tuple[int | float, int | float]:
        """
        Resolve both operands and return them as a (left, right) tuple.

        Raises
        ──────
        ValueError  — if either operand cannot be resolved or is not numeric.
                      The message describes which side failed and why, so the
                      caller can push it directly to the validator.
        """
        left_val  = self._resolve_numeric(self.left_expr,  "left")
        right_val = self._resolve_numeric(self.right_expr, "right")
        return left_val, right_val

    # ── Internal resolution ───────────────────────────────────────────────────

    def _resolve_numeric(
        self,
        expr: EVALParser.ExpressionContext,
        side: str,
    ) -> int | float:

        raw      = self._eval(expr)          # step 1 — visitor evaluates
        value    = self._unwrap(raw)         # step 2 — strip Variable / EvalType

        # step 3 — validation
        if value is None:
            # Determine a helpful label: variable name if we can get it
            label = self._label(raw, expr.getText())
            raise ValueError(
                f"Relational comparison requires a numeric operand on the {side} side, "
                f"but {label} could not be resolved to a concrete value at analysis time."
            )

        # bool is a subclass of int in Python, but true/false are not numeric
        # in the language semantics — reject them explicitly
        if isinstance(value, bool):
            raise ValueError(
                f"Relational comparison requires a numeric operand on the {side} side, "
                f"but '{expr.getText()}' is bool. "
                f"Use equality operators (== / !=) for boolean comparisons."
            )

        if not isinstance(value, (int, float)):
            raise ValueError(
                f"Relational comparison requires a numeric operand on the {side} side, "
                f"but '{expr.getText()}' resolved to {type(value).__name__!r} "
                f"(value: {value!r}). Only int and float are valid."
            )

        return value

    @staticmethod
    def _label(raw: Any, fallback: str) -> str:
        """
        Build a human-readable label for an unresolved operand.
        Uses the variable name when the visitor returned a Variable object
        (even if its value is unset), otherwise falls back to the source text.
        """
        if isinstance(raw, Variable):
            return f"variable '{raw.name}'"
        return f"'{fallback}'"