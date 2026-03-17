from __future__ import annotations

from abc import ABC
from typing import Any, Optional

from app.eval.variable_manager import VariableManager


class BaseExpressionHandler(ABC):
    """
    Shared utilities for expression handlers.

    Responsibilities
    ────────────────
    • Delegate expression evaluation to the visitor via ``_eval``.
    • Unwrap Variable chains and EvalType sentinels via ``_unwrap``.

    What this class does NOT do
    ────────────────────────────
    SemanticAnalyzer already has correct, typed visit methods for every
    primary and compound expression.  Nothing here duplicates that work.
    Subclasses call ``_eval`` which routes straight through visitor.visit()
    to those existing methods.
    """

    def __init__(self, visitor: Optional[Any] = None) -> None:
        self.visitor = visitor

    # ── Core utilities ────────────────────────────────────────────────────────

    def _eval(self, expr: Any) -> Any:
        """
        Delegate to visitor.visit(expr).

        Returns None if no visitor is attached or if the visit raises.
        """
        if self.visitor is None:
            return None
        try:
            return self.visitor.visit(expr)
        except Exception:
            return None

    @staticmethod
    def _unwrap(value: Any) -> Any:
        """
        Resolve a visitor result to a concrete Python value.

        Delegates to VariableManager.unwrap_value — the single canonical
        implementation shared across the analyzer and all handlers.
        """
        return VariableManager.unwrap_value(value)