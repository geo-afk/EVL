from __future__ import annotations

import json
from typing import Dict, Optional

from app.eval.semantic_validation import SemanticValidation
from app.models.Types import EvalType
from app.models.Variable import Variable
from app.models.custom_exceptions import ScopeException


# Scope.parent -> Scope.parent -> null

class Scope:
    def __init__(self, parent: Optional[Scope] = None, name: str = "global") -> None:
        self.parent:    Optional[Scope]      = parent
        self.name:      str                  = name
        self.variables: Dict[str, Variable]  = {}

    def __str__(self) -> str:
        return f"Scope({self.name}) -> {self.variables}"

    # ── Scope stack management ────────────────────────────────────────────────

    @classmethod
    def push_scope(cls, scope: Scope, name: str = "block") -> Scope:
        """Create and return a new child scope."""
        return cls(parent=scope, name=name)

    @classmethod
    def pop_scope(
        cls,
        current_scope: Scope,
        validator: SemanticValidation,
    ) -> Optional[Scope]:
        """Pop the current scope and return its parent."""
        if current_scope.parent is None:
            validator.push_error(None, "Scope is empty")
            raise ScopeException("[Scope Error] Cannot exit global scope")
        return current_scope.parent

    # ── Introspection ─────────────────────────────────────────────────────────

    def snapshot(self) -> str:
        """
        Return a JSON representation of this scope's variables.

        ``sym.type`` may be an EvalType enum (str-subclass) or a plain str.
        Using ``.value`` when it is an EvalType guarantees a bare string is
        embedded in the JSON (e.g. ``"int"`` not ``"EvalType.INT"``).
        """
        data = {
            name: {
                "type":   sym.type.value if isinstance(sym.type, EvalType) else str(sym.type),
                "const":  sym.constant,
                "line":   sym.position.line,
                "column": sym.position.column,
            }
            for name, sym in self.variables.items()
        }
        return json.dumps(data, indent=4)