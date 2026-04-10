from __future__ import annotations

from typing import Any, List

from app.analyzer.semantic_analyzer_support import SemanticAnalyzerSupport
from app.eval.semantic_validation import SemanticValidation
from app.eval.steps_recorder import StepRecorder
from app.eval.variable_manager import VariableManager
from app.models.SyntaxError import ErrorResponse, WarningResponse
from app.models.custom_exceptions import BreakSignal, ContinueSignal

try:
    from generated.EVALParserVisitor import EVALParserVisitor as BaseVisitor
except ImportError:
    from antlr4 import ParseTreeVisitor as BaseVisitor


class SemanticAnalyzer(BaseVisitor):
    def __init__(self) -> None:
        self._loop_depth = 0
        self.validator = SemanticValidation()
        self.variable_manager = VariableManager(validator=self.validator)
        self.recorder = StepRecorder()
        self.helper = SemanticAnalyzerSupport(self)

    @property
    def errors(self) -> List[ErrorResponse]:
        return self.validator.errors

    @property
    def warnings(self) -> List[WarningResponse]:
        return self.validator.warnings

    def _record(
        self,
        phase: str,
        title: str,
        description: str,
        line: int = 0,
        changed: str = "",
        detail: str = "",
        output_line: Any = None,
    ) -> None:
        self.helper.record(
            phase=phase,
            title=title,
            description=description,
            line=line,
            changed=changed,
            detail=detail,
            output_line=output_line,
        )

    def _error(
        self,
        phase: str,
        title: str,
        token: Any,
        msg: str,
        line: int,
        changed: str = "",
        detail: str = "",
        description: str = "",
    ) -> None:
        self.helper.error(
            phase=phase,
            title=title,
            token=token,
            msg=msg,
            line=line,
            changed=changed,
            detail=detail,
            description=description,
        )

    def visitProgram(self, ctx) -> None:
        self._record(
            phase="analysis",
            title="Semantic analysis started",
            description="Beginning semantic analysis pass over the program.",
        )
        self.visitChildren(ctx)
        self._record(
            phase="analysis",
            title="Semantic analysis complete",
            description=f"Analysis finished. Errors: {len(self.errors)}, Warnings: {len(self.warnings)}.",
        )

    def visitBlock(self, ctx) -> None:
        self.variable_manager.enter_scope("block")
        statements = list(ctx.statement())
        self._record(
            phase="scope",
            title="Entered block scope",
            description=f"New block scope pushed — {len(statements)} statement(s) to process.",
            line=ctx.start.line,
        )

        count = 0
        try:
            for index, stmt in enumerate(statements):
                self._record(
                    phase="scope",
                    title=f"Block statement {index + 1}/{len(statements)}",
                    description=f"Visiting statement {index + 1} of {len(statements)}: '{stmt.getText()}'.",
                    line=stmt.start.line,
                )
                self.visit(stmt)
                count += 1
        except (BreakSignal, ContinueSignal) as signal:
            remaining = statements[count + 1:]
            if remaining:
                keyword = "break" if isinstance(signal, BreakSignal) else "continue"
                self.validator.push_warnings(
                    remaining[0].start,
                    f"{len(remaining)} unreachable statement(s) after '{keyword}' will never execute",
                )
                self._record(
                    phase="scope",
                    title=f"Unreachable statements after '{keyword}'",
                    description=(
                        f"{len(remaining)} statement(s) after '{keyword}' on line "
                        f"{statements[count].start.line} will never execute."
                    ),
                    line=remaining[0].start.line,
                )
            raise
        finally:
            self._record(
                phase="scope",
                title="Exiting block scope",
                description=f"Block scope popped — {count} of {len(statements)} statement(s) executed.",
                line=ctx.stop.line if ctx.stop else 0,
            )
            self.variable_manager.exit_scope()

    def visitVariableDeclaration(self, ctx):
        return self.helper.handle_variable_declaration(ctx)

    def visitConstDeclaration(self, ctx):
        return self.helper.handle_const_declaration(ctx)

    def visitAssignment(self, ctx):
        return self.helper.handle_assignment(ctx)

    def visitPrintStatement(self, ctx):
        return self.helper.handle_print_statement(ctx)

    def visitPrintArg(self, ctx):
        return self.visit(ctx.expression())

    def visitIfStatement(self, ctx):
        return self.helper.handle_if_statement(ctx)

    def visitWhileStatement(self, ctx):
        return self.helper.handle_while_statement(ctx)

    def visitTryStatement(self, ctx):
        return self.helper.handle_try_statement(ctx)

    def visitBreakStatement(self, ctx) -> None:
        if self._loop_depth == 0:
            self._error(
                phase="control_flow",
                title="Break (error — outside loop)",
                token=ctx.start,
                msg="'break' used outside of a loop",
                line=ctx.start.line,
                description="'break' has no enclosing loop — statement has no effect.",
                detail="error: break outside loop",
            )
            return

        self._record(
            phase="control_flow",
            title="Break",
            description=f"break encountered at loop depth {self._loop_depth} — signalling loop exit.",
            line=ctx.start.line,
            detail=f"loop_depth={self._loop_depth}",
        )
        raise BreakSignal()

    def visitContinueStatement(self, ctx) -> None:
        if self._loop_depth == 0:
            self._error(
                phase="control_flow",
                title="Continue (error — outside loop)",
                token=ctx.start,
                msg="'continue' used outside of a loop",
                line=ctx.start.line,
                description="'continue' has no enclosing loop — statement has no effect.",
                detail="error: continue outside loop",
            )
            return

        self._record(
            phase="control_flow",
            title="Continue",
            description=f"continue encountered at loop depth {self._loop_depth} — signalling skip to next iteration.",
            line=ctx.start.line,
            detail=f"loop_depth={self._loop_depth}",
        )
        raise ContinueSignal()

    def visitLogicalOrExpr(self, ctx):
        return self.helper.evaluate_logical_or(ctx)

    def visitLogicalAndExpr(self, ctx):
        return self.helper.evaluate_logical_and(ctx)

    def visitEqualityExpr(self, ctx):
        return self.helper.evaluate_equality(ctx)

    def visitRelationalExpr(self, ctx):
        return self.helper.evaluate_relational(ctx)

    def visitAdditiveExpr(self, ctx):
        return self.helper.evaluate_additive(ctx)

    def visitMultiplicativeExpr(self, ctx):
        return self.helper.evaluate_multiplicative(ctx)

    def visitUnaryMinusExpr(self, ctx):
        return self.helper.evaluate_unary_minus(ctx)

    def visitUnaryNotExpr(self, ctx):
        return self.helper.evaluate_unary_not(ctx)

    def visitParenExpr(self, ctx):
        return self.helper.evaluate_parenthesized(ctx)

    def visitBuiltinExpr(self, ctx):
        return self.visit(ctx.builtinFunc())

    def visitIdentExpr(self, ctx):
        return self.helper.evaluate_identifier(ctx)

    def visitIntLiteral(self, ctx):
        return self.helper.evaluate_int_literal(ctx)

    def visitRealLiteral(self, ctx):
        return self.helper.evaluate_real_literal(ctx)

    def visitStringLiteral(self, ctx):
        return self.helper.evaluate_string_literal(ctx)

    def visitTrueLiteral(self, ctx):
        return self.helper.evaluate_true_literal(ctx)

    def visitFalseLiteral(self, ctx):
        return self.helper.evaluate_false_literal(ctx)

    def visitNullLiteral(self, ctx):
        return self.helper.evaluate_null_literal(ctx)

    def visitMacroExpr(self, ctx):
        return self.visit(ctx.macroValue())

    def visitBuiltinFunc(self, ctx):
        return self.visitChildren(ctx)

    def visitCastCall(self, ctx):
        return self.helper.evaluate_cast_call(ctx)

    def visitPowCall(self, ctx):
        return self.helper.evaluate_pow_call(ctx)

    def visitSqrtCall(self, ctx):
        return self.helper.evaluate_sqrt_call(ctx)

    def visitMinCall(self, ctx):
        return self.helper.evaluate_min_call(ctx)

    def visitMaxCall(self, ctx):
        return self.helper.evaluate_max_call(ctx)

    def visitRoundCall(self, ctx):
        return self.helper.evaluate_round_call(ctx)

    def visitAbsCall(self, ctx):
        return self.helper.evaluate_abs_call(ctx)

    def visitMacroValue(self, ctx):
        return self.helper.evaluate_macro_value(ctx)
