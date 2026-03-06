from __future__ import annotations
from dataclasses import dataclass
from typing import Any


# ═══════════════════════════════════════════════════════════════════════════════
#  TYPE SYSTEM
#  Mirrors the four types defined in the EVAL grammar:
#      type : INT | FLOAT | STRING_TYPE | BOOL
# ═══════════════════════════════════════════════════════════════════════════════

EVAL_TYPES = {"int", "float", "string", "bool"}

PYTHON_TYPE_MAP: dict[str, type] = {
    "int":    int,
    "float":  float,
    "string": str,
    "bool":   bool,
}


# ═══════════════════════════════════════════════════════════════════════════════
#  VARIABLE ENTRY
#  One record stored per declared variable.
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Variable:
    name:     str
    type:     str           # "int" | "float" | "string" | "bool"
    value:    Any
    constant: bool = False  # declared with CONST


# ═══════════════════════════════════════════════════════════════════════════════
#  EXCEPTIONS
#  Distinct error types make try/catch handling in the interpreter cleaner.
# ═══════════════════════════════════════════════════════════════════════════════

class EVALTypeError(Exception):
    """Raised when a value does not match the declared type."""

class EVALNameError(Exception):
    """Raised when a variable is used before it is declared."""

class EVALConstError(Exception):
    """Raised when a const variable is reassigned."""

class EVALScopeError(Exception):
    """Raised on scope stack misuse (popping the global scope)."""


# ═══════════════════════════════════════════════════════════════════════════════
#  VARIABLE MANAGER
#  Maintains a stack of scopes.  Each scope is a dict[name -> Variable].
#
#  Scope lifecycle:
#    push_scope()  — called when entering a block  { ... }
#    pop_scope()   — called when leaving  a block  { ... }
#
#  The bottom of the stack (index 0) is always the global scope.
# ═══════════════════════════════════════════════════════════════════════════════

class VariableManager:

    def __init__(self) -> None:
        # Stack of scopes: each scope is {identifier: Variable}
        self._scopes: list[dict[str, Variable]] = [{}]   # global scope


    # ── Scope management ─────────────────────────────────────────────────────

    def push_scope(self) -> None:
        """Enter a new block scope (called on every LBRACE)."""
        self._scopes.append({})

    def pop_scope(self) -> None:
        """Leave the current block scope (called on every RBRACE)."""
        if len(self._scopes) == 1:
            raise EVALScopeError("Cannot pop the global scope.")
        self._scopes.pop()

    @property
    def depth(self) -> int:
        """Current nesting depth (0 = global)."""
        return len(self._scopes) - 1


    # ── Internal helpers ─────────────────────────────────────────────────────

    def _coerce(self, eval_type: str, value: Any) -> Any:
        """
        Validate and coerce a Python value to the declared EVAL type.
        Raises EVALTypeError on mismatch.
        """
        if eval_type not in EVAL_TYPES:
            raise EVALTypeError(f"Unknown type '{eval_type}'.")

        target = PYTHON_TYPE_MAP[eval_type]
        if not isinstance(value, target):
            # Allow silent int → float widening (e.g. int x = 3.0 is still an error,
            # but float x = 3 is fine since int is a subtype of float in practice)
            if eval_type == "float" and isinstance(value, int):
                return float(value)
            raise EVALTypeError(
                f"Type mismatch: expected '{eval_type}' "
                f"but got '{type(value).__name__}' for value {value!r}."
            )
        return value

    def _find_scope(self, name: str) -> dict[str, Variable] | None:
        """
        Walk the scope stack from innermost outward.
        Returns the scope dict that contains the variable, or None.
        """
        for scope in reversed(self._scopes):
            if name in scope:
                return scope
        return None


    # ── Declaration ──────────────────────────────────────────────────────────

    def declare(self, eval_type: str, name: str, value: Any,
                constant: bool = False) -> Variable:
        """
        Declare a new variable in the CURRENT scope.

        Corresponds to grammar rules:
            variableDeclaration : type IDENTIFIER ASSIGN expression
            constDeclaration    : CONST variableDeclaration
        """
        coerced = self._coerce(eval_type, value)
        var = Variable(name=name, type=eval_type, value=coerced, constant=constant)
        self._scopes[-1][name] = var
        return var


    # ── Lookup ───────────────────────────────────────────────────────────────

    def get(self, name: str) -> Any:
        """
        Return the value of a variable, searching from innermost scope outward.
        Raises EVALNameError if not found.

        Corresponds to grammar rule:
            identExpr : IDENTIFIER
        """
        scope = self._find_scope(name)
        if scope is None:
            raise EVALNameError(f"Variable '{name}' is not defined.")
        return scope[name].value

    def get_variable(self, name: str) -> Variable:
        """Return the full Variable record (type, value, constant flag)."""
        scope = self._find_scope(name)
        if scope is None:
            raise EVALNameError(f"Variable '{name}' is not defined.")
        return scope[name]


    # ── Assignment ───────────────────────────────────────────────────────────

    def assign(self, name: str, value: Any) -> Any:
        """
        Reassign an existing variable (plain '=' operator).

        Corresponds to grammar rule:
            assignment : IDENTIFIER ASSIGN expression
        """
        scope = self._find_scope(name)
        if scope is None:
            raise EVALNameError(f"Variable '{name}' is not defined.")

        var = scope[name]
        if var.constant:
            raise EVALConstError(f"Cannot reassign const variable '{name}'.")

        var.value = self._coerce(var.type, value)
        return var.value

    def assign_op(self, name: str, op: str, value: Any) -> Any:
        """
        Compound assignment: +=  -=  *=  /=

        Corresponds to grammar rule:
            assignOp : PLUS_ASSIGN | MINUS_ASSIGN | MULTI_ASSIGN | DIV_ASSIGN
        """
        current = self.get(name)

        match op:
            case "+=": result = current + value
            case "-=": result = current - value
            case "*=": result = current * value
            case "/=":
                if value == 0:
                    raise ZeroDivisionError(f"Division by zero in '{name} /= 0'.")
                result = current / value
            case _:
                raise EVALTypeError(f"Unknown compound operator '{op}'.")

        return self.assign(name, result)


    # ── Introspection / debug ─────────────────────────────────────────────────

    def exists(self, name: str) -> bool:
        """Return True if the variable is visible in the current scope chain."""
        return self._find_scope(name) is not None

    def current_scope_vars(self) -> dict[str, Variable]:
        """Return a snapshot of variables declared in the current scope only."""
        return dict(self._scopes[-1])

    def all_visible_vars(self) -> dict[str, Variable]:
        """
        Return all variables visible from the current scope.
        Inner scope variables shadow outer ones (same name resolution as get()).
        """
        visible: dict[str, Variable] = {}
        for scope in self._scopes:          # outer → inner so inner wins
            visible.update(scope)
        return visible

    def __repr__(self) -> str:
        lines = [f"VariableManager (depth={self.depth})"]
        for i, scope in enumerate(self._scopes):
            label = "global" if i == 0 else f"scope[{i}]"
            lines.append(f"  {label}:")
            if not scope:
                lines.append("    <empty>")
            for name, var in scope.items():
                const_tag = " [const]" if var.constant else ""
                lines.append(f"    {var.type} {name} = {var.value!r}{const_tag}")
        return "\n".join(lines)