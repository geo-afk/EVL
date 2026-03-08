from antlr4.ParserRuleContext import ParserRuleContext

from app.models.CustomError import ErrorResponse, WarningResponse
from app.models.Types import EvalType, NUMERIC, NULL
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
            line: int,
            col: int,
    ) -> EvalType:
        for t in (lt, rt):
            if t not in NULL and t not in NUMERIC:
                self.push_error(
                    line_number=line,
                    column_number=col,
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
            line: int,
            col: int,
    ) -> None:
        for t in (lt, rt):
            if t not in (EvalType.BOOL, EvalType.UNKNOWN, None):
                self._warn(
                    f"logical '{op}' used with non-bool operand {t.name}",
                    line, col,
                )

    def require_numeric(self, expr_ctx, label: str) -> EvalType:
        t = self.visit(expr_ctx)
        if t not in (EvalType.UNKNOWN, None) and t not in NUMERIC:
            self._error(
                f"{label} must be numeric, got {t.name}",
                expr_ctx.start.line,
                expr_ctx.start.column,
            )
            return EvalType.UNKNOWN
        return t



    @staticmethod
    def _tok_col_line(token) -> tuple[int, int]:
        column = token.column if token else 0
        line = token.line if token else 0
        return column, line

    def push_error(self, token: , message: str):

        self.errors.append(
            ErrorResponse(
                message=message,
                line_number=line_number,
                column_number=column_number,
            )
        )

    def push_warnings(self, line_number: int, column_number: int, message: str):
        self.warnings.append(
            WarningResponse(
                message=message,
                line_number=line_number,
                column_number=column_number,
            )
        )