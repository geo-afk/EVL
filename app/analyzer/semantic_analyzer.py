from __future__ import annotations

from datetime import datetime
from math import pi, sqrt
from typing import Any, List
from app.eval.evaluator import Evaluator
from app.eval.handler.comparison_handler import ComparisonHandler
from app.eval.semantic_validation import SemanticValidation
from app.eval.steps_recorder import StepRecorder
from app.eval.variable_manager import VariableManager
from app.models.CustomError import ErrorResponse, WarningResponse
from app.models.Types import EvalType, TypeHandler
from app.models.Variable import Variable, Position
from app.models.custom_exceptions import EVALNameException, CastException, DeclarationException, CoercionException, \
    PowException
from app.eval.postfix import Postfix
from generated.EVALParser import EVALParser

try:
    from generated.EVALParserVisitor import EVALParserVisitor as BaseVisitor
except ImportError:
    from antlr4 import ParseTreeVisitor as BaseVisitor


class SemanticAnalyzer(BaseVisitor):

    def __init__(self) -> None:
        self._loop_depth      = 0
        self.validator        = SemanticValidation()
        self.variable_manager = VariableManager(validator=self.validator)
        self.recorder         = StepRecorder()

    # ── Error / warning access ────────────────────────────────────────────────

    @property
    def errors(self) -> List[ErrorResponse]:
        return self.validator.errors

    @property
    def warnings(self) -> List[WarningResponse]:
        return self.validator.warnings

    # ── Internal convenience ──────────────────────────────────────────────────

    def _record(
        self,
        phase:       str,
        title:       str,
        description: str,
        line:        int = 0,
        changed:     str = "",
        detail:      str = "",
        output_line: Any = None,
    ) -> None:
        """
        Thin wrapper that injects the current scope snapshot before forwarding
        to the recorder.  Keeps visit methods free of scope-snapshot boilerplate.
        """
        self.recorder.record(
            phase=phase,
            title=title,
            description=description,
            line=line,
            scope=self.variable_manager.scope_snapshot(),
            detail=detail,
            changed=changed,
            is_output=output_line is not None,
            output_line=output_line,
        )

    # ── Top-level ─────────────────────────────────────────────────────────────

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
            description=(
                f"Analysis finished. "
                f"Errors: {len(self.errors)}, Warnings: {len(self.warnings)}."
            ),
        )

    def visitBlock(self, ctx) -> None:
        self.variable_manager.enter_scope("block")
        self._record(
            phase="scope",
            title="Entered block scope",
            description="A new block scope has been pushed onto the scope stack.",
            line=ctx.start.line,
        )

        for stmt in ctx.statement():
            self.visit(stmt)

        self._record(
            phase="scope",
            title="Exiting block scope",
            description="Block scope is being popped; local variables are released.",
            line=ctx.stop.line if ctx.stop else 0,
        )
        self.variable_manager.exit_scope()

    # ── Declarations ──────────────────────────────────────────────────────────

    def visitVariableDeclaration(self, ctx: EVALParser.VariableDeclarationContext) -> None:
        type_text = ctx.type_().getText()
        decl_type = TypeHandler.get_eval_type(type_text)
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name = ident_tok.text
        line = ident_tok.line


        if self.variable_manager.is_defined_in_current_scope(name):
            msg = (
                f"Variable '{name}' is already declared in the current scope "
                f"[{self.variable_manager.get_scope_name()}]"
            )
            self.validator.push_error(ident_tok, msg)
            self._record(
                phase="declaration",
                title=f"Duplicate declaration: {name}",
                description=msg,
                line=line,
                changed=name,
                detail="error: duplicate declaration",
            )
            # raise DeclarationException(msg)

        var_value = self.visit(ctx.expression())
        val_type = self.variable_manager.type_check(var_value)

        #
        if val_type in TypeHandler.EMPTY or decl_type in TypeHandler.EMPTY:
            msg = (
                f"cannot initialise '{type_text}' variable '{name}' "
                f"with value of type '{val_type.name}'"
            )
            self.validator.push_error(ident_tok, msg)
            # raise DeclarationException(msg)

        coerced_val = None
        try:
            coerced_val = Evaluator.coerce_to_declared_type(
                val=VariableManager.unwrap_value(var_value),
                decl_type=decl_type,
                val_type=val_type,
                name=name,
                type_text=type_text,
            )
        except CoercionException as e:
            self.validator.push_error(ident_tok, str(e))
            # raise DeclarationException(str(e)) from e

        col, _ = self.validator.tok_col_line(ident_tok)
        variable = Variable(
            name=name,
            type=decl_type,
            value=coerced_val,
            position=Position(line=line, column=col),
        )
        print(variable)
        self.variable_manager.define(variable)

        self._record(
            phase="declaration",
            title=f"Declared: {type_text} {name}",
            description=(
                f"Variable '{name}' declared as '{type_text}' "
                f"with initial value {variable.value!r}."
            ),
            line=line,
            changed=name,
            detail=f"type={type_text}, value={variable.value!r}",
        )



    def visitConstDeclaration(self, ctx: EVALParser.ConstDeclarationContext) -> None:
        variable_declaration = ctx.variableDeclaration()
        self.visit(variable_declaration)

        name = variable_declaration.IDENTIFIER().getText()
        try:
            variable          = self.variable_manager.get_variable(name)
            variable.constant = True
            self.variable_manager.define(variable)

            self._record(
                phase="declaration",
                title=f"Declared const: {name}",
                description=f"Variable '{name}' marked as a constant.",
                line=variable_declaration.IDENTIFIER().getSymbol().line,
                changed=name,
                detail=f"const=True, value={variable.value!r}",
            )
        except EVALNameException as e:
            self.validator.push_error(
                variable_declaration.IDENTIFIER().getSymbol(),
                f"{e} in this scope",
            )

    # ── Assignment ────────────────────────────────────────────────────────────

    def visitAssignment(self, ctx: EVALParser.AssignmentContext) -> None:
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name      = ident_tok.text
        op        = ctx.assignOp().getText()
        line      = ident_tok.line

        try:
            variable = self.variable_manager.get_variable(name)
        except EVALNameException as e:
            self.validator.push_error(ident_tok, f"{e} in this scope")
            return

        if variable.constant:
            self.validator.push_error(
                ident_tok,
                f"cannot reassign const variable '{name}'",
            )
            self._record(
                phase="assignment",
                title=f"Const reassignment blocked: {name}",
                description=f"Attempted to reassign const variable '{name}'.",
                line=line,
                changed=name,
                detail="error: const reassignment",
            )
            return

        rhs      = self.visit(ctx.expression())
        rhs_type = self.variable_manager.type_check(rhs)
        rhs_val  = VariableManager.unwrap_value(rhs)
        var_type = self.variable_manager.type_check(variable)
        old_value = variable.value

        if op == "=":
            if (
                var_type not in TypeHandler.EMPTY
                and not self.validator.types_compatible(var_type, rhs_type)
            ):
                self.validator.push_error(
                    ident_tok,
                    f"cannot assign {rhs_type.name} to '{var_type.name}' variable '{name}'",
                )
            variable.value = rhs_val

        else:
            # Compound operators require numeric operands on both sides
            if var_type not in TypeHandler.EMPTY and var_type not in TypeHandler.NUMERIC:
                self.validator.push_error(
                    ident_tok,
                    f"compound operator '{op}' requires a numeric variable; "
                    f"'{name}' is {var_type.name}",
                )
                return

            if rhs_type not in TypeHandler.EMPTY and rhs_type not in TypeHandler.NUMERIC:
                self.validator.push_error(
                    ident_tok,
                    f"compound operator '{op}' requires a numeric right-hand side, "
                    f"got {rhs_type.name}",
                )
                return

            cur_val = VariableManager.unwrap_value(variable)
            if isinstance(cur_val, (int, float)) and isinstance(rhs_val, (int, float)):
                if   op == "+=": variable.value = cur_val + rhs_val
                elif op == "-=": variable.value = cur_val - rhs_val
                elif op == "*=": variable.value = cur_val * rhs_val
                elif op == "/=":
                    if rhs_val == 0:
                        self.validator.push_error(ident_tok, "division by zero")
                    else:
                        variable.value = cur_val / rhs_val

        self.variable_manager.define(variable)
        self._record(
            phase="assignment",
            title=f"Assigned: {name} {op}",
            description=(
                f"Variable '{name}' updated via '{op}'. "
                f"Old value: {old_value!r} → New value: {variable.value!r}."
            ),
            line=line,
            changed=name,
            detail=f"op={op}, rhs={rhs_val!r}",
        )

    # ── Print ─────────────────────────────────────────────────────────────────

    def visitPrintStatement(self, ctx: EVALParser.PrintStatementContext) -> str:
        """
        Evaluate every print argument, concatenate them into a single
        space-separated string, record the output step, and return the string.
        """
        parts = []
        for arg in ctx.printArg():
            val = self.visit(arg)
            raw = VariableManager.unwrap_value(val)
            parts.append("" if raw is None else str(raw))

        output_line = " ".join(parts)
        self._record(
            phase="output",
            title="Print",
            description=f"print({', '.join(repr(p) for p in parts)}) → {output_line!r}",
            line=ctx.start.line,
            output_line=output_line,
        )
        return output_line

    def visitPrintArg(self, ctx: EVALParser.PrintArgContext) -> Any:
        return self.visit(ctx.expression())

    # ── Control flow ──────────────────────────────────────────────────────────

    def visitIfStatement(self, ctx: EVALParser.IfStatementContext) -> None:
        expressions = ctx.expression()
        blocks      = ctx.block()
        has_else    = len(blocks) > len(expressions)

        self._record(
            phase="control_flow",
            title="If statement",
            description=(
                f"if with {len(expressions)} condition(s)"
                f"{', has else branch' if has_else else ''}."
            ),
            line=ctx.start.line,
        )

        for i, expr in enumerate(expressions):
            cond_result = self.visit(expr)
            cond_type   = self.variable_manager.type_check(cond_result)
            cond_value  = VariableManager.unwrap_value(cond_result)

            if cond_type not in (EvalType.BOOL, EvalType.UNKNOWN, None):
                self.validator.push_error(
                    expr.start,
                    f"{'if' if i == 0 else 'else if'} condition must be bool, "
                    f"got {cond_type.name}",
                )

            branch_label = "if" if i == 0 else f"else if [{i}]"
            self._record(
                phase="control_flow",
                title=f"Condition ({branch_label})",
                description=(
                    f"{branch_label} condition '{expr.getText()}' "
                    f"evaluated to {cond_value!r}."
                ),
                line=expr.start.line,
                detail=f"type={cond_type}, value={cond_value!r}",
            )
            self.visit(blocks[i])

        if has_else:
            self._record(
                phase="control_flow",
                title="Else branch",
                description="Analysing else branch.",
                line=blocks[-1].start.line,
            )
            self.visit(blocks[-1])

    def visitWhileStatement(self, ctx: EVALParser.WhileStatementContext) -> None:
        expr        = ctx.expression()
        cond_result = self.visit(expr)
        cond_type   = self.variable_manager.type_check(cond_result)
        cond_value  = VariableManager.unwrap_value(cond_result)

        if cond_type not in (EvalType.BOOL, EvalType.UNKNOWN, None):
            self.validator.push_error(
                expr.start,
                f"while condition must be bool, got {cond_type.name}",
            )

        if cond_value is False:
            self.validator.push_warnings(
                expr.start,
                "while condition is always false — loop body is unreachable",
            )
        elif cond_value is True:
            self.validator.push_warnings(
                expr.start,
                "while condition is always true — potential infinite loop",
            )

        self._record(
            phase="control_flow",
            title="While loop",
            description=(
                f"while condition '{expr.getText()}' "
                f"evaluated to {cond_value!r}."
            ),
            line=ctx.start.line,
            detail=f"type={cond_type}, value={cond_value!r}",
        )

        self._loop_depth += 1
        self.visit(ctx.block())
        self._loop_depth -= 1

    def visitTryStatement(self, ctx: EVALParser.TryStatementContext) -> None:
        try_block   = ctx.block(0)
        catch_block = ctx.block(1)
        ident_tok   = ctx.IDENTIFIER().getSymbol()
        catch_name  = ident_tok.text
        col, line   = self.validator.tok_col_line(ident_tok)

        self._record(
            phase="control_flow",
            title="Try block",
            description="Entering try block.",
            line=try_block.start.line,
        )
        self.visit(try_block)

        self.variable_manager.enter_scope("catch")
        catch_var = Variable(
            name=catch_name,
            type=EvalType.UNKNOWN,
            value=None,
            position=Position(line=line, column=col),
        )
        self.variable_manager.define(catch_var)

        self._record(
            phase="control_flow",
            title="Catch block",
            description=f"Entering catch block with exception variable '{catch_name}'.",
            line=catch_block.start.line,
            changed=catch_name,
            detail=f"exception variable '{catch_name}' bound as UNKNOWN type",
        )

        # Visit statements directly — do NOT call self.visit(catch_block)
        # because visitBlock would push a second scope on top of this one.
        for stmt in catch_block.statement():
            self.visit(stmt)

        self._record(
            phase="control_flow",
            title="Exiting catch block",
            description=f"Catch block complete; releasing '{catch_name}' from scope.",
            line=catch_block.stop.line if catch_block.stop else line,
        )
        self.variable_manager.exit_scope()

    def visitBreakStatement(self, ctx: EVALParser.BreakStatementContext) -> None:
        if self._loop_depth == 0:
            self.validator.push_error(ctx.start, "'break' used outside of a loop")
        self._record(
            phase="control_flow",
            title="Break statement",
            description="break encountered.",
            line=ctx.start.line,
        )

    def visitContinueStatement(self, ctx: EVALParser.ContinueStatementContext) -> None:
        if self._loop_depth == 0:
            self.validator.push_error(ctx.start, "'continue' used outside of a loop")
        self._record(
            phase="control_flow",
            title="Continue statement",
            description="continue encountered.",
            line=ctx.start.line,
        )

    # ── Binary / unary expressions ────────────────────────────────────────────

    def visitLogicalOrExpr(self, ctx: EVALParser.LogicalOrExprContext) -> EvalType:
        lt = self.variable_manager.type_check(self.visit(ctx.expression(0)))
        rt = self.variable_manager.type_check(self.visit(ctx.expression(1)))
        self.validator.check_logical_operands("||", lt, rt, ctx.start)
        return EvalType.BOOL

    def visitLogicalAndExpr(self, ctx: EVALParser.LogicalAndExprContext) -> EvalType:
        lt = self.variable_manager.type_check(self.visit(ctx.expression(0)))
        rt = self.variable_manager.type_check(self.visit(ctx.expression(1)))
        self.validator.check_logical_operands("&&", lt, rt, ctx.start)
        return EvalType.BOOL

    def visitEqualityExpr(self, ctx: EVALParser.EqualityExprContext) -> EvalType:
        lt = self.variable_manager.type_check(self.visit(ctx.expression(0)))
        rt = self.variable_manager.type_check(self.visit(ctx.expression(1)))
        if (
            lt not in TypeHandler.EMPTY
            and rt not in TypeHandler.EMPTY
            and not self.validator.types_compatible(lt, rt)
        ):
            self.validator.push_warnings(
                ctx.start,
                f"comparing incompatible types {lt.name} and {rt.name}",
            )
        return EvalType.BOOL

    def visitRelationalExpr(self, ctx: EVALParser.RelationalExprContext) -> bool | EvalType:
        """
        Evaluate a relational expression and return the boolean result when
        both operands are statically known, or EvalType.BOOL as a fallback.

        ComparisonHandler resolves and validates both operands; Evaluator
        applies the operator.  This visitor stays clean of operator logic.
        """
        op = ctx.op.text

        handler = ComparisonHandler(
            left_expr  = ctx.expression(0),
            right_expr = ctx.expression(1),
            visitor    = self,
        )
        try:
            left_val, right_val = handler.check()
        except ValueError as exc:
            self.validator.push_error(ctx.op, str(exc))
            return EvalType.BOOL

        return Evaluator.evaluate_relational(left_val, op, right_val)

    def visitAdditiveExpr(self, ctx: EVALParser.AdditiveExprContext) -> Any:
        lhs = self.visit(ctx.expression(0))
        rhs = self.visit(ctx.expression(1))
        op  = ctx.op.text

        lt = self.variable_manager.type_check(lhs)
        rt = self.variable_manager.type_check(rhs)

        result_type = self.validator.numeric_result(op, lt, rt, ctx.start)
        if result_type == EvalType.UNKNOWN:
            return EvalType.UNKNOWN

        lv = VariableManager.unwrap_value(lhs)
        rv = VariableManager.unwrap_value(rhs)
        if isinstance(lv, (int, float)) and isinstance(rv, (int, float)):
            return Postfix.get_result(f"{lv} {op} {rv}")

        return result_type

    def visitMultiplicativeExpr(self, ctx: EVALParser.MultiplicativeExprContext) -> Any:
        lhs = self.visit(ctx.expression(0))
        rhs = self.visit(ctx.expression(1))
        op  = ctx.op.text

        lt = self.variable_manager.type_check(lhs)
        rt = self.variable_manager.type_check(rhs)

        result_type = self.validator.numeric_result(op, lt, rt, ctx.start)
        if result_type == EvalType.UNKNOWN:
            return EvalType.UNKNOWN

        lv = VariableManager.unwrap_value(lhs)
        rv = VariableManager.unwrap_value(rhs)
        if isinstance(lv, (int, float)) and isinstance(rv, (int, float)):
            try:
                return Postfix.get_result(f"{lv} {op} {rv}")
            except ZeroDivisionError:
                self.validator.push_error(
                    ctx.start,
                    f"{'division' if op == '/' else 'modulo'} by zero",
                )
                return EvalType.UNKNOWN

        return result_type

    def visitUnaryMinusExpr(self, ctx: EVALParser.UnaryMinusExprContext) -> Any:
        inner = self.visit(ctx.expression())
        t     = self.variable_manager.type_check(inner)

        if t not in TypeHandler.EMPTY and t not in TypeHandler.NUMERIC:
            self.validator.push_error(
                ctx.start,
                f"unary '-' requires a numeric operand, got {t.name}",
            )
            return EvalType.UNKNOWN

        v = VariableManager.unwrap_value(inner)
        if isinstance(v, (int, float)):
            return Postfix.get_result(f"0 - {v}")

        return t if t in TypeHandler.NUMERIC else EvalType.UNKNOWN

    def visitUnaryNotExpr(self, ctx: EVALParser.UnaryNotExprContext) -> EvalType:
        inner = self.visit(ctx.expression())
        t     = self.variable_manager.type_check(inner)
        if t not in (EvalType.BOOL, EvalType.UNKNOWN, None):
            self.validator.push_warnings(
                ctx.start,
                f"'!' applied to {t.name} — expected bool",
            )
        return EvalType.BOOL

    def visitParenExpr(self, ctx: EVALParser.ParenExprContext) -> Any:
        return self.visit(ctx.expression())

    def visitBuiltinExpr(self, ctx: EVALParser.BuiltinExprContext) -> Any:
        return self.visit(ctx.builtinFunc())

    # ── Identifier / literals ─────────────────────────────────────────────────

    def visitIdentExpr(self, ctx: EVALParser.IdentExprContext) -> Variable | None:
        tok  = ctx.IDENTIFIER().getSymbol()
        name = tok.text
        try:
            return self.variable_manager.get_variable(name)
        except EVALNameException as e:
            self.validator.push_error(ctx.start, str(e))
            return None

    def visitIntLiteral(self, ctx) -> int:
        return int(ctx.INTEGER().getText())

    def visitRealLiteral(self, ctx) -> float:
        return float(ctx.REAL().getText())

    def visitStringLiteral(self, ctx) -> str:
        return ctx.STRING().getText()

    def visitTrueLiteral(self, ctx) -> bool:
        return True

    def visitFalseLiteral(self, ctx) -> bool:
        return False

    def visitNullLiteral(self, _ctx) -> None:
        return None

    def visitMacroExpr(self, ctx: EVALParser.MacroExprContext) -> Any:
        return self.visit(ctx.macroValue())

    # ── Built-in functions ────────────────────────────────────────────────────

    def visitBuiltinFunc(self, ctx: EVALParser.BuiltinFuncContext) -> Any:
        return self.visitChildren(ctx)

    def visitCastCall(self, ctx) -> Any:
        expression = ctx.expression()
        visited_val = self.visit(expression)
        target_text = ctx.type_().getText()
        target_type = TypeHandler.get_eval_type(target_text)


        _INVALID_CAST_TARGETS = {EvalType.NULL, EvalType.UNKNOWN}
        if target_type in _INVALID_CAST_TARGETS:
            msg = (
                f"invalid cast target type '{target_text}': "
                f"cannot cast to '{target_type.value}'"
            )
            self.validator.push_error(ctx.type_().start, msg)
            raise CastException(msg)


        if visited_val is None:
            msg = "cast argument could not be resolved"
            self.validator.push_error(expression.start, msg)
            raise CastException(msg)


        if isinstance(visited_val, Variable):
            val = VariableManager.unwrap_value(visited_val)
        elif isinstance(visited_val, (int, float, str, bool)):
            val = visited_val
        else:
            msg = (
                f"cast argument has unsupported type '{type(visited_val).__name__}': "
                f"expected int, float, str, bool, or Variable"
            )
            self.validator.push_error(expression.start, msg)
            raise CastException(msg)

        if val is None:
            msg = "cast argument evaluates to null and cannot be cast"
            self.validator.push_error(expression.start, msg)
            raise CastException(msg)

        result = Evaluator.cast(val, target_type)
        if result is None:
            msg = f"cast failed: could not convert '{val!r}' to '{target_type.value}'"
            self.validator.push_error(expression.start, msg)
            raise CastException(msg)

        return result

    def visitPowCall(self, ctx: EVALParser.PowCallContext) -> Any:
        left_expr = ctx.expression(0)
        right_expr = ctx.expression(1)

        left_val = self.visit(left_expr)
        right_val = self.visit(right_expr)

        # ── 1. Validate both sides resolved to something ──────────────────────
        if left_val is None:
            msg = f"pow() first argument could not be resolved"
            self.validator.push_error(left_expr.start, msg)
            raise PowException(msg)

        if right_val is None:
            msg = f"pow() second argument could not be resolved"
            self.validator.push_error(right_expr.start, msg)
            raise PowException(msg)


        left_type = self.variable_manager.type_check(left_val)
        right_type = self.variable_manager.type_check(right_val)

        if left_type not in TypeHandler.NUMERIC:
            msg = f"pow() first argument must be numeric, got '{left_type.name}'"
            self.validator.push_error(left_expr.start, msg)
            raise PowException(msg)

        if right_type not in TypeHandler.NUMERIC:
            msg = f"pow() second argument must be numeric, got '{right_type.name}'"
            self.validator.push_error(right_expr.start, msg)
            raise PowException(msg)


        left_unwrapped = VariableManager.unwrap_value(left_val)
        right_unwrapped = VariableManager.unwrap_value(right_val)

        if left_unwrapped is None:
            msg = "pow() first argument evaluates to null"
            self.validator.push_error(left_expr.start, msg)
            raise PowException(msg)

        if right_unwrapped is None:
            msg = "pow() second argument evaluates to null"
            self.validator.push_error(right_expr.start, msg)
            raise PowException(msg)


        try:
            result = pow(left_unwrapped, right_unwrapped)
        except (ValueError, TypeError, ZeroDivisionError) as e:
            msg = (
                f"pow() failed for operands "
                f"'{left_unwrapped!r}' and '{right_unwrapped!r}': {e}"
            )
            self.validator.push_error(left_expr.start, msg)
            raise PowException(msg) from e

        if left_type == EvalType.FLOAT or right_type == EvalType.FLOAT:
            return float(result)

        return int(result)

    def visitSqrtCall(self, ctx: EVALParser.SqrtCallContext) -> Any:
        expression = ctx.expression()
        value      = self.visit(expression)

        if value is None:
            self.validator.push_warnings(
                expression.start,
                "sqrt() argument could not be resolved",
            )
            return EvalType.FLOAT

        t = self.variable_manager.type_check(value)
        if t not in TypeHandler.EMPTY and t not in TypeHandler.NUMERIC:
            self.validator.push_error(
                expression.start,
                f"sqrt() requires a numeric argument, got {t.name}",
            )
            return EvalType.UNKNOWN

        v = VariableManager.unwrap_value(value)
        if isinstance(v, (int, float)):
            if v < 0:
                self.validator.push_error(
                    expression.start,
                    "sqrt() argument must be non-negative",
                )
                return EvalType.UNKNOWN
            return sqrt(v)

        return EvalType.FLOAT

    def visitMinCall(self, ctx: EVALParser.MinCallContext) -> Any:
        first_val  = self.visit(ctx.expression(0))
        second_val = self.visit(ctx.expression(1))

        ft = self.variable_manager.type_check(first_val)
        st = self.variable_manager.type_check(second_val)

        self.validator.require_numeric(ft, ctx.expression(0), "min() first argument")
        self.validator.require_numeric(st, ctx.expression(1), "min() second argument")

        fv = VariableManager.unwrap_value(first_val)
        sv = VariableManager.unwrap_value(second_val)
        if isinstance(fv, (int, float)) and isinstance(sv, (int, float)):
            return min(fv, sv)

        return EvalType.FLOAT if EvalType.FLOAT in (ft, st) else EvalType.INT

    def visitMaxCall(self, ctx: EVALParser.MaxCallContext) -> Any:
        first_val  = self.visit(ctx.expression(0))
        second_val = self.visit(ctx.expression(1))

        ft = self.variable_manager.type_check(first_val)
        st = self.variable_manager.type_check(second_val)

        self.validator.require_numeric(ft, ctx.expression(0), "max() first argument")
        self.validator.require_numeric(st, ctx.expression(1), "max() second argument")

        fv = VariableManager.unwrap_value(first_val)
        sv = VariableManager.unwrap_value(second_val)
        if isinstance(fv, (int, float)) and isinstance(sv, (int, float)):
            return max(fv, sv)

        return EvalType.FLOAT if EvalType.FLOAT in (ft, st) else EvalType.INT

    def visitRoundCall(self, ctx: EVALParser.RoundCallContext) -> Any:
        expression = ctx.expression()
        value      = self.visit(expression)

        t = self.variable_manager.type_check(value)
        self.validator.require_numeric(t, expression, "round() argument")

        v = VariableManager.unwrap_value(value)
        if isinstance(v, (int, float)):
            return round(v)

        return EvalType.FLOAT

    def visitAbsCall(self, ctx: EVALParser.AbsCallContext) -> Any:
        expression = ctx.expression()
        value      = self.visit(expression)

        t = self.variable_manager.type_check(value)
        self.validator.require_numeric(t, expression, "abs() argument")

        v = VariableManager.unwrap_value(value)
        if isinstance(v, (int, float)):
            return abs(v)

        return t if t in TypeHandler.NUMERIC else EvalType.UNKNOWN

    # ── Macro constants ───────────────────────────────────────────────────────

    def visitMacroValue(self, ctx: EVALParser.MacroValueContext) -> Any:
        if ctx.PI():
            return pi

        now = datetime.now()
        if ctx.DAYS_IN_WEEK():
            return now.weekday()   # 0 = Monday … 6 = Sunday
        if ctx.HOURS_IN_DAY():
            return now.hour
        if ctx.YEAR():
            return now.year

        return None