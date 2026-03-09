from app.models.Scope import Scope
from typing import Any

from app.models.Types import TypeHandler
from app.models.Variable import Variable, Position
from app.models.custom_exceptions import EVALTypeException, EVALNameException, EVALConstException


class VariableManager:

    def __init__(self, validator) -> None:
        self._global_scope = Scope(name="global")
        self._current_scope = self._global_scope
        self._scope_depth = 0

        self.validator = validator


    # ── Scope management ─────────────────────────────────────────────────────

    def enter_scope(self, name: str) -> None:
        """Enter a new block scope (called on every LBRACE)."""
        self._current_scope = Scope.push_scope(
            scope=self._current_scope,
            name=name
        )
        self._scope_depth +=1

    def exit_scope(self) -> None:
        self._current_scope = Scope.pop_scope(
            current_scope=self._current_scope,
            validator=self.validator
        )
        self._scope_depth -=1



    @property
    def depth(self) -> int:
        """Current nesting depth (0 = global)."""
        return self._scope_depth



    @staticmethod
    def _coerce(eval_type: str, value: Any) -> Any:
        """
        Validate and coerce a Python value to the declared EVAL type.
        Raises EVALTypeError on mismatch.
        """
        if TypeHandler.is_valid_type(eval_type):
            raise EVALTypeException(f"Unknown type '{eval_type}'.")


        target = TypeHandler.is_python_type(eval_type)
        if not isinstance(value, target):
            # Allow silent int → float widening (e.g. int x = 3.0 is still an error,
            # but float x = 3 is fine since int is a subtype of float in practice)
            if eval_type == "float" and isinstance(value, int):
                return float(value)
            raise EVALTypeException(
                f"Type mismatch: expected '{eval_type}' "
                f"but got '{type(value).__name__}' for value {value!r}."
            )
        return value

    def _find_scope(self, name: str) -> dict[str, Variable] | None:
        """
        Walk the scope stack from innermost outward.
        Returns the scope dict that contains the variable, or None.
        """

        scope = self._current_scope

        while scope is not None:
            if name == scope.variables[name]:
                return scope
            scope = scope.parent

        return None


    # ── Declaration ──────────────────────────────────────────────────────────

    def declare(self, eval_type: str, name: str,
                value: Any, line: int, column: int,
                constant: bool = False,
    ) -> Variable:
        """
        Declare a new variable in the CURRENT scope.

        Corresponds to grammar rules:
            variableDeclaration : type IDENTIFIER ASSIGN expression
            constDeclaration    : CONST variableDeclaration
        """
        coerced = self._coerce(eval_type, value)
        var = Variable(
            name=name, type=eval_type, value=coerced,
            constant=constant, position=Position(
                line=line,
                column=column,
            ))

        self._current_scope.variables[name] = var
        return var


    def get_variable(self, name: str) -> Variable:
        """Return the full Variable record (type, value, constant flag)."""
        scope = self._find_scope(name)
        if scope is None:
            raise EVALNameException(f"Variable '{name}' is not defined.")
        return scope[name]


    def assign(self, name: str, value: Any) -> Any:
        """
        Reassign an existing variable (plain '=' operator).

        Corresponds to grammar rule:
            assignment : IDENTIFIER ASSIGN expression
        """
        scope = self._find_scope(name)
        if scope is None:
            raise EVALNameException(f"Variable '{name}' is not defined.")

        var = scope[name]
        if var.constant:
            raise EVALConstException(f"Cannot reassign const variable '{name}'.")

        var.value = self._coerce(var.type, value)
        return var.value

    def assign_op(self, name: str, op: str, value: Any) -> Any:
        """
        Compound assignment: +=  -=  *=  /=

        Corresponds to grammar rule:
            assignOp : PLUS_ASSIGN | MINUS_ASSIGN | MULTI_ASSIGN | DIV_ASSIGN
        """
        current = self.get_variable(name)
        var_val = current.value

        match op:
            case "+=": result = var_val + value
            case "-=": result = var_val - value
            case "*=": result = var_val * value
            case "/=":
                if value == 0:
                    raise ZeroDivisionError(f"Division by zero in '{name} /= 0'.")
                result = var_val / value
            case _:
                raise EVALTypeException(f"Unknown compound operator '{op}'.")

        return self.assign(name, result)


    # ── Introspection / debug ─────────────────────────────────────────────────

    def exists(self, name: str) -> bool:
        """Return True if the variable is visible in the current scope chain."""
        return self._find_scope(name) is not None

    def current_scope_vars(self) -> dict[str, Variable]:
        """Return a snapshot of variables declared in the current scope only."""
        return dict(self._current_scope.variables)

    def all_visible_vars(self) -> dict[str, Variable]:
        """
        Return all variables visible from the current scope.
        Inner scope variables shadow outer ones (same name resolution as get()).
        """
        visible: dict[str, Variable] = {}

        for key, value in self._current_scope.variables.items():
            visible[key] = value

        return visible

    def __repr__(self) -> str:
        lines = [f"VariableManager (depth={self.depth})"]
        for i, variables in enumerate(self._current_scope.variables.items()):
            label = "global" if i == 0 else f"scope[{i}]"
            lines.append(f"  {label}:")
            if not variables:
                lines.append("    <empty>")
            for name, var in variables:
                const_tag = " [const]" if var.constant else ""
                lines.append(f"    {var.type} {name} = {var.value!r}{const_tag}")
        return "\n".join(lines)