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



    def define(self, sym: Symbol) -> bool:
        """Register symbol in THIS scope. Returns False if already declared."""
        if sym.name in self._symbols:
            return False
        self._symbols[sym.name] = sym
        return True

    def resolve(self, name: str) -> Optional[Symbol]:
        """Walk the scope chain to find a symbol."""
        try:
            if name in self._symbols:
                return self._symbols[name]
            if self.parent:
                return self.parent.resolve(name)
        except Exception as e:
            # Log error or handle appropriately
            print(f"Error resolving symbol '{name}': {e}")
            return None
        return None


    def snapshot(self) -> str:
        """Return a JSON representation of this scope's symbols."""
        data = {
            name: {
                "type": sym.eval_type.name,
                "const": sym.is_const,
                "line": sym.line,
                "column": sym.column,
            }
            for name, sym in self._symbols.items()
        }

        return json.dumps(data, indent=4)
