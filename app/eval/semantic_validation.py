from app.models.CustomError import ErrorResponse, WarningResponse
from app.models.Types import EvalType, TypeHandler
from typing import List, Any


class SemanticValidation:


    def __init__(self):
        self.errors: List[ErrorResponse] = []
        self.warnings: List[WarningResponse] = []

    @staticmethod
    def types_compatible(expected: EvalType, actual: EvalType) -> bool:
        """
        True when actual can be used where expected is declared.
        Widening int→float is allowed (weak-typing rule of EVAL).
        """
        if expected == actual:
            return True
        # Widening: int is assignable to float
        if expected == EvalType.FLOAT and actual == EvalType.INT:
            return True
        # NULL is assignable to any non-primitive (future-proofing)
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
            if t not in TypeHandler.EMPTY and t not in TypeHandler.NUMERIC:
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
            if t not in (EvalType.BOOL, EvalType.UNKNOWN, None):
                self.push_warnings(
                    token,
                    f"logical '{op}' used with non-bool operand {t.name}",
                )

    def require_numeric(self,
                        eval_type: Any,
                        expr_ctx: Any,
                        label: str
        ) -> EvalType:
        if eval_type not in TypeHandler.EMPTY and eval_type not in TypeHandler.NUMERIC:
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