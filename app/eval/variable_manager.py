from __future__ import annotations

from typing import Any

from app.models.Scope import Scope
from app.models.Types import EvalType, TypeHandler
from app.models.Variable import Variable
from app.models.custom_exceptions import EVALNameException


class VariableManager:

    def __init__(self, validator) -> None:
        self._global_scope  = Scope(name="global")
        self._current_scope = self._global_scope
        self._scope_depth   = 0
        self.validator      = validator

    # ── Scope management ─────────────────────────────────────────────────────

    def enter_scope(self, name: str) -> None:
        """Push a new child scope onto the stack."""
        self._current_scope = Scope.push_scope(
            scope=self._current_scope,
            name=name,
        )
        self._scope_depth += 1

    def get_scope_name(self):
        return self._current_scope.name

    def exit_scope(self) -> None:
        """Pop the current scope and return to its parent."""
        self._current_scope = Scope.pop_scope(
            current_scope=self._current_scope,
            validator=self.validator,
        )
        self._scope_depth -= 1



    @property
    def depth(self) -> int:
        """Current nesting depth (0 = global)."""
        return self._scope_depth

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _find_scope(self, name: str) -> Scope | None:
        """Walk the scope stack from innermost outward; return the owning scope or None."""
        scope = self._current_scope
        while scope is not None:
            if scope.variables.get(name) is not None:
                return scope
            scope = scope.parent
        return None

    # ── Declaration ──────────────────────────────────────────────────────────

    def define(self, variable: Variable) -> Variable:
        """
        Define (or overwrite) a variable in the CURRENT scope.

        Used for:
          • initial variable / const declarations
          • updating a variable's value or type after assignment / cast
        """
        self._current_scope.variables[variable.name] = variable
        return variable

    def is_defined_in_current_scope(self, name: str) -> bool:
        """
        True only if *name* is declared in the innermost scope.
        Allows shadowing in nested scopes while catching re-declarations in the
        same scope.
        """
        return name in self._current_scope.variables

    # ── Lookup ───────────────────────────────────────────────────────────────

    def get_variable(self, name: str) -> Variable:
        """Return the full Variable record; raises EVALNameException when absent."""
        scope = self._find_scope(name)
        if scope is None:
            raise EVALNameException(f"Variable '{name}' is not defined or used before assigned")
        return scope.variables[name]

    def exists(self, name: str) -> bool:
        """True if *name* is visible anywhere in the current scope chain."""
        return self._find_scope(name) is not None

    # ── Introspection / snapshots ─────────────────────────────────────────────

    def current_scope_vars(self) -> dict[str, Variable]:
        """Snapshot of variables declared in the innermost scope only."""
        return dict(self._current_scope.variables)


    def all_visible_vars(self) -> dict[str, Variable]:
        """
        All variables visible from the current scope, with inner-scope names
        shadowing outer ones.
        """
        visible: dict[str, Variable] = {}
        scope = self._current_scope
        while scope is not None:
            for name, var in scope.variables.items():
                if name not in visible:
                    visible[name] = var
            scope = scope.parent
        return visible

    def scope_snapshot(self) -> dict[str, dict]:
        """
        JSON-serialisable snapshot of every variable visible from the current
        scope.  Captured at each step so the frontend can replay state changes.
        """
        return {
            name: {
                "type":  str(var.type),
                "value": var.value,
                "const": var.constant,
            }
            for name, var in self.all_visible_vars().items()
        }

    # ── Static utilities ─────────────────────────────────────────────────────

    @staticmethod
    def unwrap_value(val: Any) -> Any:

        # Walk Variable chains
        while isinstance(val, Variable):
            val = val.value

        # Raw primitives — returned directly
        if isinstance(val, bool):  # bool is subclass of int — must check first
            return val
        if isinstance(val, (int, float, str)):
            return val

        return None

    @staticmethod
    def get_type(val: Any) -> EvalType:
        """
        Extract an EvalType from any visitor result.
        Handles Variable objects, EvalType sentinels, and raw Python values.
        """
        if isinstance(val, Variable):
            t = val.type
            return t if isinstance(t, EvalType) else TypeHandler.get_eval_type(str(t))
        if isinstance(val, EvalType):
            return val
        if isinstance(val, bool):   # bool is a subclass of int — must check first
            return EvalType.BOOL
        if isinstance(val, int):
            return EvalType.INT
        if isinstance(val, float):
            return EvalType.FLOAT
        if isinstance(val, str):
            return EvalType.STRING
        if val is None:
            return EvalType.NULL
        return EvalType.UNKNOWN

    def __repr__(self) -> str:
        lines = [f"VariableManager (depth={self.depth})"]
        visible = self.all_visible_vars()
        if not visible:
            lines.append("  <empty>")
        for name, var in visible.items():
            const_tag = " [const]" if var.constant else ""
            lines.append(f"  {var.type} {name} = {var.value!r}{const_tag}")
        return "\n".join(lines)

