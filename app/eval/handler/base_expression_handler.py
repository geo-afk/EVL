"""
base_expression_handler.py
──────────────────────────
Abstract base class that centralises expression-type dispatch for any handler
that needs to inspect or evaluate EVAL parse-tree expression nodes.

Concrete subclasses (ComparisonHandler, future ArithmeticHandler, etc.) inherit
the full dispatch table and every per-node handler, overriding only what they need.
"""

from __future__ import annotations

from abc import ABC
from typing import Any, Dict, Optional

from app.models.Types import EvalType
from generated.EVALParser import EVALParser


class BaseExpressionHandler(ABC):
    """
    Reusable expression dispatcher.

    Responsibilities
    ────────────────
    • Build a {ContextType → handler} dispatch table on construction.
    • Expose ``_analyze_expression(expr, side)`` — resolves the right handler
      and returns a unified ``Dict[str, Any]`` result.
    • Provide default per-node handler implementations that any subclass can
      override individually without duplicating the entire table.

    Visitor contract
    ────────────────
    An optional *visitor* (typically the SemanticAnalyzer) is stored as
    ``self.visitor``.  Handlers that need a fully-evaluated value call
    ``self._eval(expr)`` which delegates to ``visitor.visit(expr)`` safely.
    """

    def __init__(self, visitor: Optional[Any] = None) -> None:
        self.visitor = visitor

        # Populated once; subclasses can mutate after calling super().__init__()
        # to add or override individual entries.
        self._type_handlers: Dict[type, Any] = {
            EVALParser.IdentExprContext:          self._handle_identifier,
            EVALParser.IntLiteralContext:          self._handle_integer,
            EVALParser.RealLiteralContext:         self._handle_real,
            EVALParser.StringLiteralContext:       self._handle_string,
            EVALParser.TrueLiteralContext:         self._handle_true,
            EVALParser.FalseLiteralContext:        self._handle_false,
            EVALParser.NullLiteralContext:         self._handle_null,
            EVALParser.MacroExprContext:           self._handle_macro,
            EVALParser.ParenExprContext:           self._handle_paren,
            EVALParser.UnaryMinusExprContext:      self._handle_unary_minus,
            EVALParser.UnaryNotExprContext:        self._handle_unary_not,
            EVALParser.AdditiveExprContext:        self._handle_additive,
            EVALParser.MultiplicativeExprContext:  self._handle_multiplicative,
            EVALParser.BuiltinExprContext:         self._handle_builtin,
            EVALParser.LogicalOrExprContext:       self._handle_logical_or,
            EVALParser.LogicalAndExprContext:      self._handle_logical_and,
            EVALParser.EqualityExprContext:        self._handle_equality,
        }

    # ── Public API ────────────────────────────────────────────────────────────

    def _analyze_expression(
        self,
        expr: EVALParser.ExpressionContext,
        side: str = "",
    ) -> Dict[str, Any]:
        """
        Dispatch *expr* to the correct handler and return a normalised result dict.

        Every result dict is guaranteed to contain at least:
          • ``'type'``          – EvalType or descriptive string tag
          • ``'value'``         – resolved Python value, or None
          • ``'raw_text'``      – expr.getText()
          • ``'context_type'``  – class name of the parse-tree node
          • ``'handler_called'``– name of the handler that fired (or None)
        """
        result: Dict[str, Any] = {
            "type":          EvalType.UNKNOWN,
            "value":         None,
            "raw_text":      expr.getText(),
            "context_type":  type(expr).__name__,
            "handler_called": None,
        }

        for ctx_type, handler in self._type_handlers.items():
            if isinstance(expr, ctx_type):
                result.update(handler(expr, side))
                result["handler_called"] = ctx_type.__name__
                return result

        # Fallback – no specific handler matched
        result.update(self._handle_generic(expr, side))
        return result

    # ── Internal utilities ────────────────────────────────────────────────────

    def _eval(self, expr: Any) -> Any:
        """
        Safely delegate evaluation to the visitor.
        Returns *None* when no visitor is set or the visit raises.
        """
        if self.visitor is None:
            return None
        try:
            return self.visitor.visit(expr)
        except Exception:
            return None

    @staticmethod
    def python_value_to_eval_type(value: Any) -> EvalType:
        """
        Map a raw Python runtime value to the corresponding EvalType.

        Note: bool must be checked before int because ``bool`` is a subclass
        of ``int`` in Python.
        """
        if isinstance(value, bool):  return EvalType.BOOL
        if isinstance(value, int):   return EvalType.INT
        if isinstance(value, float): return EvalType.FLOAT
        if isinstance(value, str):   return EvalType.STRING
        if value is None:            return EvalType.NULL
        return EvalType.UNKNOWN

    def _resolve_identifier_value(self, name: str) -> Any:
        """
        Look up a variable's current value from the visitor's variable manager.
        Returns *None* if the variable is not found or the visitor is unavailable.
        """
        if self.visitor and hasattr(self.visitor, "variable_manager"):
            try:
                return self.visitor.variable_manager.get_variable(name).value
            except Exception:
                pass
        return None

    def _visitor_delegated(self, expr: Any, type_tag: str) -> Dict[str, Any]:
        """
        Shared helper for expression nodes that are fully evaluated by the visitor.
        Avoids copy-pasting the same six-line dict for additive, multiplicative, etc.
        """
        value = self._eval(expr)
        return {
            "type":            type_tag,
            "expression":      expr.getText(),
            "value":           value,
            "numeric_value":   value if isinstance(value, (int, float)) else None,
            "needs_evaluation": value is None,
        }

    # ── Per-node handlers ─────────────────────────────────────────────────────
    # Each returns a *partial* dict that is merged into the base result by
    # ``_analyze_expression``.  Only override the keys you need to change.

    def _handle_identifier(
        self, expr: EVALParser.IdentExprContext, side: str
    ) -> Dict[str, Any]:
        name  = expr.IDENTIFIER().getText()
        value = self._resolve_identifier_value(name)
        return {
            "type":             "identifier",
            "subtype":          "variable",
            "name":             name,
            "value":            value,
            "value_type":       self.python_value_to_eval_type(value),
            "needs_resolution": value is None,
        }

    def _handle_integer(
        self, expr: EVALParser.IntLiteralContext, side: str
    ) -> Dict[str, Any]:
        val = int(expr.INTEGER().getText())
        return {"type": EvalType.INT, "value": val, "numeric_value": val}

    def _handle_real(
        self, expr: EVALParser.RealLiteralContext, side: str
    ) -> Dict[str, Any]:
        val = float(expr.REAL().getText())
        return {"type": EvalType.FLOAT, "value": val, "numeric_value": val}

    def _handle_string(
        self, expr: EVALParser.StringLiteralContext, side: str
    ) -> Dict[str, Any]:
        # Strip surrounding quotes
        val = expr.STRING().getText()[1:-1]
        return {"type": EvalType.STRING, "value": val, "length": len(val)}

    def _handle_true(
        self, expr: EVALParser.TrueLiteralContext, side: str
    ) -> Dict[str, Any]:
        return {"type": EvalType.BOOL, "value": True,  "literal": "true"}

    def _handle_false(
        self, expr: EVALParser.FalseLiteralContext, side: str
    ) -> Dict[str, Any]:
        return {"type": EvalType.BOOL, "value": False, "literal": "false"}

    def _handle_null(
        self, expr: EVALParser.NullLiteralContext, side: str
    ) -> Dict[str, Any]:
        return {"type": EvalType.NULL, "value": None}

    def _handle_macro(
        self, expr: EVALParser.MacroExprContext, side: str
    ) -> Dict[str, Any]:
        """
        Resolve macro constants.  If a visitor is available it is used so that
        runtime-dynamic macros (YEAR, HOURS_IN_DAY, …) are evaluated correctly.
        Falls back to a static lookup table for offline use.
        """
        macro_name = expr.getText()

        # Try visitor first (honours runtime-dynamic macros)
        value = self._eval(expr)
        if value is None:
            _STATIC_MACROS: Dict[str, Any] = {
                "PI":           3.141592653589793,
                "DAYS_IN_WEEK": 7,
                "HOURS_IN_DAY": 24,
                "YEAR":         2024,
            }
            value = _STATIC_MACROS.get(macro_name)

        return {
            "type":          "macro",
            "name":          macro_name,
            "value":         value,
            "numeric_value": value if isinstance(value, (int, float)) else None,
        }

    def _handle_paren(
        self, expr: EVALParser.ParenExprContext, side: str
    ) -> Dict[str, Any]:
        inner = expr.expression()
        value = self._eval(inner)
        return {
            "type":             "parenthesized",
            "inner_expression": inner.getText(),
            "value":            value,
            "value_type":       self.python_value_to_eval_type(value),
            "needs_evaluation": value is None,
        }

    def _handle_unary_minus(
        self, expr: EVALParser.UnaryMinusExprContext, side: str
    ) -> Dict[str, Any]:
        inner     = expr.expression()
        inner_val = self._eval(inner)
        value     = -inner_val if isinstance(inner_val, (int, float)) else None
        return {
            "type":             "unary_minus",
            "inner_expression": inner.getText(),
            "value":            value,
            "numeric_value":    value,
            "needs_evaluation": value is None,
        }

    def _handle_unary_not(
        self, expr: EVALParser.UnaryNotExprContext, side: str
    ) -> Dict[str, Any]:
        inner     = expr.expression()
        inner_val = self._eval(inner)
        value     = not inner_val if isinstance(inner_val, bool) else None
        return {
            "type":             "unary_not",
            "inner_expression": inner.getText(),
            "value":            value,
            "needs_evaluation": value is None,
        }

    def _handle_additive(
        self, expr: EVALParser.AdditiveExprContext, side: str
    ) -> Dict[str, Any]:
        return self._visitor_delegated(expr, "additive_expression")

    def _handle_multiplicative(
        self, expr: EVALParser.MultiplicativeExprContext, side: str
    ) -> Dict[str, Any]:
        return self._visitor_delegated(expr, "multiplicative_expression")

    def _handle_logical_or(
        self, expr: EVALParser.LogicalOrExprContext, side: str
    ) -> Dict[str, Any]:
        return self._visitor_delegated(expr, "logical_or")

    def _handle_logical_and(
        self, expr: EVALParser.LogicalAndExprContext, side: str
    ) -> Dict[str, Any]:
        return self._visitor_delegated(expr, "logical_and")

    def _handle_equality(
        self, expr: EVALParser.EqualityExprContext, side: str
    ) -> Dict[str, Any]:
        return self._visitor_delegated(expr, "equality_expression")

    def _handle_builtin(
        self, expr: EVALParser.BuiltinExprContext, side: str
    ) -> Dict[str, Any]:
        builtin = expr.builtinFunc()
        value   = self._eval(builtin)
        return {
            "type":            "builtin_call",
            "function":        builtin.getText(),
            "value":           value,
            "numeric_value":   value if isinstance(value, (int, float)) else None,
            "needs_evaluation": value is None,
        }

    def _handle_generic(
        self, expr: EVALParser.ExpressionContext, side: str
    ) -> Dict[str, Any]:
        """Fallback handler for expression types with no dedicated handler."""
        value = self._eval(expr)
        return {
            "type":             "generic_expression",
            "value":            value,
            "needs_evaluation": value is None,
        }