from __future__ import annotations

from symtable import Symbol
from typing import Optional, Self, Dict
import json

from app.eval.semantic_validation import SemanticValidation
from app.models.Variable import Variable
from app.models.custom_exceptions import ScopeException


class Scope:
    def __init__(self, parent: Optional[Self] = None, name: str = "global"):
        self.parent   = parent
        self.name     = name
        self.variables: Dict[str, Variable] = {}


    def __str__(self) -> str:
        return f"Scope({self.name}) -> {self.variables}"


    @classmethod
    def push_scope(cls, scope: "Scope", name: str = "block") -> "Scope":
        """Create and return a new child scope."""
        return cls(parent=scope, name=name)


    @classmethod
    def pop_scope(cls, current_scope: "Scope", validator: SemanticValidation) -> Optional["Scope"]:
        """Pop the current scope and return the parent scope."""
        if current_scope.parent is None:
            validator.push_error(None, "Scope is empty")
            raise ScopeException("[Scope Error] Cannot exit global scope")
        return current_scope.parent



    def snapshot(self) -> str:
        """Return a JSON representation of this scope's symbols."""
        data = {
            name: {
                "type": sym.type,
                "const": sym.constant,
                "line": sym.position.line,
                "column": sym.position.column,
            }
            for name, sym in self.variables.items()
        }

        return json.dumps(data, indent=4)
