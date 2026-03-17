from app.models.CustomError import ErrorResponse, WarningResponse
from app.models.Types import EvalType, TypeHandler
from typing import List, Any


class SemanticValidation:

    # ── Reserved identifiers ──────────────────────────────────────────────────
    # Every token that the lexer recognises as a keyword, built-in function,
    # type name, or macro constant is forbidden as a variable / parameter name.
    # Keeping this here (rather than in the analyser) makes it easy to reuse
    # across any validation site and to extend as the language grows.
    RESERVED_NAMES: frozenset[str] = frozenset({
        # Primitive type keywords
        "int", "float", "string", "bool",
        # Modifier keyword
        "const",
        # Control-flow keywords
        "if", "else", "for", "while", "break", "continue", "return",
        "try", "catch",
        # Literal keywords
        "null", "true", "false",
        # Built-in functions
        "print", "cast", "pow", "sqrt", "min", "max", "round", "abs",
        # Built-in macro / constant identifiers
        "PI", "DAYS_IN_WEEK", "HOURS_IN_DAY", "YEAR",
    })

    def __init__(self):
        self.errors: List[ErrorResponse] = []
        self.warnings: List[WarningResponse] = []

    @staticmethod
    def types_compatible(expected: EvalType, actual: EvalType) -> bool:

        if expected == actual:
            return True
        # Widening: int is assignable to float
        if expected == EvalType.FLOAT and actual == EvalType.INT:
            return True
        # NULL is assignable to any non-primitive
        if actual == EvalType.NULL:
            return True
        return False

    def numeric_result(
            self,
            op: str,
            lt: EvalType,
            rt: EvalType,
            token: Any
    ) -> EvalType:
        for t in (lt, rt):
            if t not in TypeHandler.NUMERIC:
                self.push_error(
                    token,
                    message=f"operator '{op}' requires numeric operands, got {t.name}"
                )
                return EvalType.UNKNOWN
        # int op float → float (widening)
        if EvalType.FLOAT in (lt, rt):
            return EvalType.FLOAT
        return EvalType.INT

    def check_logical_operands(
            self,
            op: str,
            lt: EvalType,
            rt: EvalType,
            token: Any
    ) -> None:
        for t in (lt, rt):
            if t is not EvalType.BOOL:
                self.push_warnings(
                    token,
                    f"logical '{op}' used with non-bool operand {t.name}",
                )

    def require_numeric(self,
                        eval_type: Any,
                        expr_ctx: Any,
                        label: str
        ) -> EvalType:
        if eval_type not in TypeHandler.NUMERIC:
            self.push_error(
                expr_ctx.start,
                f"{label} must be numeric, got {eval_type.name}",
            )
            return EvalType.UNKNOWN
        return eval_type


    @staticmethod
    def tok_col_line(token) -> tuple[int, int]:
        column = token.column if token else 0
        line = token.line if token else 0
        return column, line

    def push_error(self, token: Any, message: str):

        column, line = self.tok_col_line(token)
        self.errors.append(
            ErrorResponse(
                message=message,
                line_number=line,
                column_number=column,
            )
        )

    def push_warnings(self, token: Any, message: str):

        column, line = self.tok_col_line(token)
        self.warnings.append(
            WarningResponse(
                message=message,
                line_number=line,
                column_number=column,
            )
        )

    # ── New validation helpers ────────────────────────────────────────────────

    def check_reserved_name(self, name: str, token: Any) -> bool:
        """
        Emit an error and return True if *name* clashes with a reserved
        identifier (keyword, built-in function, type name, or macro constant).
        Returns False when the name is safe to use.
        """
        if name in self.RESERVED_NAMES:
            self.push_error(
                token,
                f"'{name}' is a reserved identifier and cannot be used as a "
                f"variable name",
            )
            return True
        return False

    def check_shadow(self, name: str, token: Any, is_in_current: bool, exists_outer: bool) -> None:
        """
        Emit a warning when *name* is declared in an inner scope while an
        identically-named variable is already visible from an outer scope.
        Shadowing is legal but is almost always a latent bug.
        """
        if not is_in_current and exists_outer:
            self.push_warnings(
                token,
                f"variable '{name}' shadows an outer-scope declaration — "
                f"the outer variable will be inaccessible within this scope",
            )

    def check_narrowing(self, decl_type: EvalType, val_type: EvalType, name: str, token: Any) -> None:
        """
        Emit a warning when an implicit float → int narrowing coercion occurs.
        The conversion is technically legal (the coercer will truncate), but
        precision loss is a common source of bugs and should be surfaced.
        """
        if decl_type == EvalType.INT and val_type == EvalType.FLOAT:
            self.push_warnings(
                token,
                f"implicit narrowing: float expression assigned to int variable "
                f"'{name}' — fractional part will be truncated",
            )

    def check_float_equality(self, op: str, lt: EvalType, rt: EvalType, token: Any) -> None:
        """
        Warn when == or != is used to compare two floating-point values.
        IEEE 754 arithmetic means such comparisons are almost never reliable
        (e.g. 0.1 + 0.2 != 0.3).  This mirrors guidance from C, Java, and
        most static analysers.
        """
        if EvalType.FLOAT in (lt, rt):
            self.push_warnings(
                token,
                f"comparing floating-point values with '{op}' may produce "
                f"unexpected results due to floating-point precision — "
                f"consider using an epsilon-based comparison",
            )

    def check_modulo_float(self, lt: EvalType, rt: EvalType, token: Any) -> None:
        """
        Warn when the modulo operator '%' is applied to floating-point operands.
        While Python (and thus the runtime) permits float modulo, its semantics
        are surprising to most programmers and the operation is rarely intentional.
        Most statically-typed languages (Java, Go, Rust) restrict '%' to integers.
        """
        if EvalType.FLOAT in (lt, rt):
            self.push_warnings(
                token,
                "modulo '%' applied to floating-point operand(s) — "
                "result follows Python remainder semantics and may be unexpected; "
                "consider casting to int first",
            )