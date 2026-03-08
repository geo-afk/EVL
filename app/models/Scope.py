import json
from typing import Optional

from app.eval.semantic_validation import SemanticValidation
from app.models.Symbol import Symbol


class Scope:
    def __init__(self, parent: Optional["Scope"] = None, name: str = "global"):
        self.parent   = parent
        self.name     = name
        self._symbols: dict[str, Symbol] = {}


    @staticmethod
    def push_scope(scope: "Scope", name: str = "block") -> "Scope":
        scope = Scope(parent=scope, name=name)
        return scope


    @staticmethod
    def pop_scope(current_scope: "Scope", validator: SemanticValidation) -> None:
        if current_scope.parent is None:
            validator.push_error(None, "Scope is empty")
            return
        current_scope = current_scope.parent



    def define(self, sym: Symbol) -> bool:
        """Register symbol in THIS scope. Returns False if already declared."""
        if sym.name in self._symbols:
            return False
        self._symbols[sym.name] = sym
        return True

    def resolve(self, name: str) -> Optional[Symbol]:
        """Walk the scope chain to find a symbol."""
        if name in self._symbols:
            return self._symbols[name]
        if self.parent:
            return self.parent.resolve(name)
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
