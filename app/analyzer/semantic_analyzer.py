from __future__ import annotations


from math import sqrt
from typing import Any, List, Literal
from app.eval.evaluator import Evaluator
from app.eval.expression_builder import ExpressionStringBuilder
from app.eval.handler.comparison_handler import ComparisonHandler
from app.eval.semantic_validation import SemanticValidation
from app.eval.steps_recorder import StepRecorder
from app.eval.variable_manager import VariableManager
from app.models.MacroValue import MacroValue
from app.models.SyntaxError import ErrorResponse, WarningResponse
from app.models.Types import EvalType, TypeHandler
from app.models.Variable import Variable, Position
from app.models.custom_exceptions import EVALNameException, CastException, CoercionException, PowException, BreakSignal, \
    ContinueSignal
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


    @property
    def errors(self) -> List[ErrorResponse]:
        return self.validator.errors

    @property
    def warnings(self) -> List[WarningResponse]:
        return self.validator.warnings



    _CATCHABLE = (
        ArithmeticError,    # division by zero, bad operand types, unary minus
        ZeroDivisionError,  # direct zero-division (sub-class of ArithmeticError, listed for clarity)
        TypeError,          # type mismatches from unary/binary expression visitors
        CastException,      # invalid cast
        PowException,       # pow() failures
        EVALNameException,  # undeclared / unknown identifier
        CoercionException,  # type coercion failure
        ValueError,         # raised by comparison handlers
    )


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


    def _error(
        self,
        phase:       str,
        title:       str,
        token:       Any,
        msg:         str,
        line:        int,
        changed:     str = "",
        detail:      str = "",
        description: str = "",
    ) -> None:
        """
        Push a semantic error and record the step in one call.
        `description` defaults to `msg` when omitted; `detail` defaults to
        ``"error: {msg}"`` when omitted.
        """
        self.validator.push_error(token, msg)
        self._record(
            phase=phase,
            title=title,
            description=description or msg,
            line=line,
            changed=changed,
            detail=detail or f"error: {msg}",
        )


    def _run_comparison(self, ctx: Any, op: str, label: str) -> tuple:
        """
        Run a ComparisonHandler for equality/relational expressions.
        Records and re-raises ValueError on failure.
        Returns (left_val, right_val) on success.
        """
        handler = ComparisonHandler(
            left_expr  = ctx.expression(0),
            right_expr = ctx.expression(1),
            visitor    = self,
        )
        try:
            return handler.check()
        except ValueError as exc:
            self.validator.push_error(ctx.op, str(exc))
            self._record(
                phase="expression",
                title=f"{label} check failed ({op})",
                description=f"Comparison handler raised an error: {exc}",
                line=ctx.start.line,
                detail=f"error: {exc}",
            )
            raise exc


    def _eval_postfix(self, ctx: Any, label: str, op: str, result_type) -> Any:
        """
        Build a postfix expression string, evaluate it, record the result, and
        return it.  Returns None when the string cannot be built (indeterminate
        operands).  ZeroDivisionError is intentionally not caught here — callers
        that need division-by-zero handling should wrap this call themselves.
        """
        expr_string = ExpressionStringBuilder.build(ctx, self.variable_manager, self.visit)
        if expr_string is None:
            return None
        result = Postfix.get_result(expr_string)
        self._record(
            phase="expression",
            title=f"{label} result ({op})",
            description=f"Expression '{expr_string}' evaluated to {result!r} (type: {result_type.name}).",
            line=ctx.start.line,
            detail=f"expr={expr_string!r}, result={result!r}",
        )
        return result


    def _visit_unary_numeric_call(self, ctx, fn, fn_name: str) -> Any:
        """
        Shared implementation for single-argument numeric built-ins (round, abs).
        Validates the argument type, applies `fn`, records the result.
        """
        expression   = ctx.expression()
        value        = self.visit(expression)
        value_type   = self.variable_manager.get_type(value)
        checked_type = self.validator.require_numeric(value_type, expression, f"{fn_name}() argument")


        if checked_type == EvalType.UNKNOWN:
            self._record(
                phase="expression",
                title=f"{fn_name}() type error",
                description=f"{fn_name}() requires a numeric argument, got {value_type.name}.",
                line=ctx.start.line,
                detail=f"error: expected NUMERIC, got {value_type.name}",
            )
            return None

        v  = VariableManager.unwrap_value(value)
        result = fn(v)
        self._record(
            phase="expression",
            title=f"{fn_name}() result",
            description=f"{fn_name}({v!r}) → {result!r}.",
            line=ctx.start.line,
            detail=f"input={v!r}, result={result!r}",
        )
        return result


    def _visit_binary_numeric_call(self, ctx, fn, fn_name: str) -> Any:
        """
        Shared implementation for two-argument numeric built-ins (min, max).
        Validates both argument types, applies `fn`, records the result.
        """
        first_val  = self.visit(ctx.expression(0))
        second_val = self.visit(ctx.expression(1))

        first_type  = self.variable_manager.get_type(first_val)
        second_type = self.variable_manager.get_type(second_val)

        checked_type1 = self.validator.require_numeric(first_type,  ctx.expression(0), f"{fn_name}() first argument")
        checked_type2 = self.validator.require_numeric(second_type, ctx.expression(1), f"{fn_name}() second argument")

        if checked_type1 == EvalType.UNKNOWN or checked_type2 == EvalType.UNKNOWN:
            self._record(
                phase="expression",
                title=f"{fn_name}() type error",
                description=f"{fn_name}() requires numeric arguments — got {first_type.name} and {second_type.name}.",
                line=ctx.start.line,
                detail=f"error: types={first_type.name}, {second_type.name}",
            )
            return None

        first_value  = VariableManager.unwrap_value(first_val)
        second_value = VariableManager.unwrap_value(second_val)
        result       = fn(first_value, second_value)
        self._record(
            phase="expression",
            title=f"{fn_name}() result",
            description=f"{fn_name}({first_value!r}, {second_value!r}) → {result!r}.",
            line=ctx.start.line,
            detail=f"a={first_value!r}, b={second_value!r}, result={result!r}",
        )
        return result


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
        statements = list(ctx.statement())
        self._record(
            phase="scope",
            title="Entered block scope",
            description=f"New block scope pushed — {len(statements)} statement(s) to process.",
            line=ctx.start.line,
        )

        count = 0
        try:
            for i, stmt in enumerate(statements):
                self._record(
                    phase="scope",
                    title=f"Block statement {i + 1}/{len(statements)}",
                    description=f"Visiting statement {i + 1} of {len(statements)}: '{stmt.getText()}'.",
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
                    f"{len(remaining)} unreachable statement(s) after '{keyword}' "
                    f"will never execute",
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


    # ─────────────────────────────────────────────────────────────────────────
    # Declarations
    # ─────────────────────────────────────────────────────────────────────────

    def visitVariableDeclaration(self, ctx: EVALParser.VariableDeclarationContext) -> None:
        type_text = ctx.type_().getText()
        decl_type = TypeHandler.get_eval_type(type_text)
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name      = ident_tok.text
        line      = ident_tok.line


        if self.validator.check_reserved_keyword(name, ident_tok):
            self._record(
                phase="declaration",
                title=f"Reserved name blocked: {name}",
                description=(
                    f"'{name}' is a reserved identifier and cannot be used "
                    f"as a variable name — declaration aborted."
                ),
                line=line,
                changed=name,
                detail="error: reserved identifier",
            )
            return

        # ── Shadow check ──────────────────────────────────────────────────────
        in_current   = self.variable_manager.is_defined_in_current_scope(name)
        exists_outer = self.variable_manager.exists(name)
        self.validator.check_shadow(
            name=name,
            token=ident_tok,
            is_in_current=in_current,
            exists_outer=exists_outer,
        )
        if not in_current and exists_outer:
            self._record(
                phase="declaration",
                title=f"Shadow warning: {name}",
                description=f"'{name}' shadows an outer-scope variable — warning issued.",
                line=line,
                changed=name,
                detail="warning: shadows outer declaration",
            )

        if in_current:
            msg = (
                f"Variable '{name}' is already declared in the current scope "
                f"[{self.variable_manager.get_scope_name()}]"
            )
            self._error(
                phase="declaration",
                title=f"Duplicate declaration: {name}",
                token=ident_tok,
                msg=msg,
                line=line,
                changed=name,
                detail="error: duplicate declaration",
            )
            return

        var_value = self.visit(ctx.expression())
        val_type  = self.variable_manager.get_type(var_value)

        # ── Cast-type consistency check ───────────────────────────────────────
        cast_target = self.validator.direct_cast_type(ctx.expression())
        if cast_target is not None and cast_target != decl_type:
            msg = (
                f"cast-type mismatch: cast produces '{cast_target.name}' "
                f"but variable '{name}' is declared as '{type_text}' — "
                f"change either the cast target or the variable type"
            )
            self._error(
                phase="declaration",
                title=f"Cast-type mismatch: {name}",
                token=ident_tok,
                msg=msg,
                line=line,
                changed=name,
                detail=f"error: cast target '{cast_target.name}' != declared '{type_text}'",
            )
            return

        # ── Type compatibility check ──────────────────────────────────────────
        if val_type in TypeHandler.EMPTY or decl_type in TypeHandler.EMPTY:
            msg = (
                f"cannot initialise '{type_text}' variable '{name}' "
                f"with value of type '{val_type.name}'"
            )
            self._error(
                phase="declaration",
                title=f"Type error: {name}",
                token=ident_tok,
                msg=msg,
                line=line,
                changed=name,
                detail=f"error: incompatible types — declared '{type_text}', got '{val_type.name}'",
            )
            return

        # ── Narrowing check ───────────────────────────────────────────────────
        self.validator.check_narrowing(decl_type, val_type, name, ident_tok)
        if decl_type == EvalType.INT and val_type == EvalType.FLOAT:
            self._record(
                phase="declaration",
                title=f"Narrowing warning: {name}",
                description=f"Float value implicitly narrowed to int for '{name}' — fractional part will be lost.",
                line=line,
                detail="warning: float → int narrowing",
            )

        # ── Coercion ──────────────────────────────────────────────────────────
        coerced_val = None
        try:
            coerced_val = Evaluator.coerce_to_declared_type(
                val=VariableManager.unwrap_value(var_value),
                decl_type=decl_type,
                val_type=val_type,
                name=name,
                type_text=type_text,
            )
            self._record(
                phase="declaration",
                title=f"Coercion for {name}",
                description=f"Value coerced to '{type_text}': {coerced_val!r}.",
                line=line,
                detail=f"coerced={coerced_val!r}",
            )
        except CoercionException as e:
            self._error(
                phase="declaration",
                title=f"Coercion failed: {name}",
                token=ident_tok,
                msg=str(e),
                line=line,
                description=f"Could not coerce value to '{type_text}': {e}",
                detail=f"error: {e}",
            )
            return

        col, _ = self.validator.tok_col_line(ident_tok)
        variable = Variable(
            name=name,
            type=decl_type,
            value=coerced_val,
            position=Position(line=line, column=col),
        )
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
            variable = self.variable_manager.get_variable(name)
            variable.constant = True
            self.variable_manager.define(variable)

            self._record(
                phase="declaration",
                title=f"Declared const: {name}",
                description=f"Variable '{name}' marked as constant — reassignment is now forbidden.",
                line=variable_declaration.IDENTIFIER().getSymbol().line,
                changed=name,
                detail=f"const=True, value={variable.value!r}",
            )
        except EVALNameException as e:
            self._error(
                phase="declaration",
                title=f"Const lookup failed: {name}",
                token=variable_declaration.IDENTIFIER().getSymbol(),
                msg=f"{e} in this scope",
                line=ctx.start.line,
                description=f"Could not mark '{name}' as const — variable not found in scope: {e}",
                detail=f"error: {e}",
            )


    # ─────────────────────────────────────────────────────────────────────────
    # Assignment
    # ─────────────────────────────────────────────────────────────────────────

    def visitAssignment(self, ctx: EVALParser.AssignmentContext) -> None:
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name      = ident_tok.text
        op        = ctx.assignOp().getText()
        line      = ident_tok.line

        # ── Variable lookup ───────────────────────────────────────────────────
        try:
            variable = self.variable_manager.get_variable(name)
            self._record(
                phase="assignment",
                title=f"Variable found: {name}",
                description=(
                    f"'{name}' resolved — current value: {variable.value!r}, "
                    f"type: {self.variable_manager.get_type(variable).name}."
                ),
                line=line,
                detail=f"current_value={variable.value!r}",
            )
        except EVALNameException as e:
            self._error(
                phase="assignment",
                title=f"Undeclared variable: {name}",
                token=ident_tok,
                msg=f"{e} in this scope",
                line=line,
                description=f"'{name}' is not declared in any accessible scope — assignment aborted.",
                detail=f"error: {e}",
            )
            return

        # ── Const guard ───────────────────────────────────────────────────────
        if variable.constant:
            self._error(
                phase="assignment",
                title=f"Const reassignment blocked: {name}",
                token=ident_tok,
                msg=f"cannot reassign const variable '{name}'",
                line=line,
                changed=name,
                description=f"Attempted to reassign const variable '{name}' — operation rejected.",
                detail="error: const reassignment",
            )
            return

        # ── Evaluate RHS ──────────────────────────────────────────────────────
        rhs       = self.visit(ctx.expression())
        rhs_type  = self.variable_manager.get_type(rhs)
        rhs_val   = VariableManager.unwrap_value(rhs)
        var_type  = self.variable_manager.get_type(variable)
        old_value = variable.value

        self._record(
            phase="assignment",
            title=f"RHS evaluated for {name}",
            description=f"RHS = {rhs_val!r} (type: {rhs_type.name}), LHS type: {var_type.name}.",
            line=line,
            detail=f"rhs_val={rhs_val!r}, rhs_type={rhs_type.name}, var_type={var_type.name}",
        )

        if op == "=":
            if (
                var_type not in TypeHandler.EMPTY
                and not self.validator.types_compatible(var_type, rhs_type)
            ):
                self._error(
                    phase="assignment",
                    title=f"Type mismatch: {name}",
                    token=ident_tok,
                    msg=f"cannot assign {rhs_type.name} to '{var_type.name}' variable '{name}'",
                    line=line,
                    description=(
                        f"Cannot assign {rhs_type.name} value to '{var_type.name}' "
                        f"variable '{name}' — assignment aborted."
                    ),
                    detail=f"error: {rhs_type.name} → {var_type.name}",
                )
                return
            variable.value = rhs_val

        else:
            # ── Compound operators (+=, -=, *=, /=, %=) ──────────────────────
            if Evaluator.is_non_numeric(var_type):
                self._error(
                    phase="assignment",
                    title=f"Compound op type error: {name}",
                    token=ident_tok,
                    msg=(
                        f"compound operator '{op}' requires a numeric variable; "
                        f"'{name}' is {var_type.name}"
                    ),
                    line=line,
                    description=f"'{op}' requires a numeric variable; '{name}' is {var_type.name}.",
                    detail=f"error: non-numeric LHS ({var_type.name})",
                )
                return

            if Evaluator.is_non_numeric(rhs_type):
                self._error(
                    phase="assignment",
                    title=f"Compound op RHS type error: {name}",
                    token=ident_tok,
                    msg=(
                        f"compound operator '{op}' requires a numeric right-hand side, "
                        f"got {rhs_type.name}"
                    ),
                    line=line,
                    description=f"'{op}' requires numeric RHS; got {rhs_type.name}.",
                    detail=f"error: non-numeric RHS ({rhs_type.name})",
                )
                return

            cur_val = VariableManager.unwrap_value(variable)
            if self.validator.is_numeric_val(cur_val) and self.validator.is_numeric_val(rhs_val):
                new_val, err = Evaluator.apply_compound_op(op, cur_val, rhs_val)
                if err:
                    self._error(
                        phase="assignment",
                        title=f"Compound op failed: {name}",
                        token=ident_tok,
                        msg=err,
                        line=line,
                        description=f"Compound op '{op}' failed: {err}",
                        detail=f"error: {err}",
                    )
                    return
                elif new_val is not None:
                    new_val_type = self.variable_manager.get_type(new_val)
                    self.validator.check_narrowing(var_type, new_val_type, name, ident_tok)
                    coerced, err = Evaluator.coerce_for_assignment(new_val, var_type, new_val_type, name)
                    if err:
                        self._error(
                            phase="assignment",
                            title=f"Coercion failed: {name}",
                            token=ident_tok,
                            msg=err,
                            line=line,
                            description=f"Compound op coercion failed: {err}",
                            detail=f"error: {err}",
                        )
                        return
                    else:
                        variable.value = coerced

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
            detail=f"op={op}, rhs={rhs_val!r}, old={old_value!r}, new={variable.value!r}",
        )


    def visitPrintStatement(self, ctx: EVALParser.PrintStatementContext) -> str:
        args = list(ctx.printArg())

        parts = []
        for idx, arg in enumerate(args):
            val = self.visit(arg)
            raw = VariableManager.unwrap_value(val)
            part = Evaluator.process_print_arg(raw)


            parts.append(part)
            self._record(
                phase="output",
                title=f"Print arg {idx + 1}/{len(args)}",
                description=f"Argument {idx + 1} ('{arg.getText()}') evaluated to {raw!r}.",
                line=arg.start.line,
                detail=f"arg={arg.getText()!r}, value={raw!r}",
            )

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

        branch_taken = False

        for i, expr in enumerate(expressions):
            branch_label = "if" if i == 0 else f"else if [{i}]"

            self._record(
                phase="control_flow",
                title=f"Evaluating condition ({branch_label})",
                description=f"Evaluating {branch_label} condition: '{expr.getText()}'.",
                line=expr.start.line,
            )

            cond_result = self.visit(expr)
            cond_type   = self.variable_manager.get_type(cond_result)
            cond_value  = VariableManager.unwrap_value(cond_result)


            if cond_type != EvalType.BOOL:
                self.validator.push_error(
                    expr.start,
                    f"{branch_label} condition must be bool, got {cond_type.name}",
                )
                self._record(
                    phase="control_flow",
                    title=f"Condition type error ({branch_label})",
                    description=(
                        f"{branch_label} condition '{expr.getText()}' has type "
                        f"{cond_type.name}, expected bool — branch skipped."
                    ),
                    line=expr.start.line,
                    detail=f"error: expected BOOL, got {cond_type.name}",
                )
                continue

            self._record(
                phase="control_flow",
                title=f"Condition result ({branch_label})",
                description=(
                    f"{branch_label} condition '{expr.getText()}' "
                    f"evaluated to {cond_value!r}."
                ),
                line=expr.start.line,
                detail=f"type={cond_type.name}, value={cond_value!r}",
            )

            if cond_value is True:
                self._record(
                    phase="control_flow",
                    title=f"Branch taken ({branch_label})",
                    description=f"Condition is True — entering {branch_label} block.",
                    line=blocks[i].start.line,
                )
                self.visit(blocks[i])
                branch_taken = True
                break

            elif cond_value is False:
                self._record(
                    phase="control_flow",
                    title=f"Branch skipped ({branch_label})",
                    description=f"{branch_label} condition is False — branch not taken.",
                    line=expr.start.line,
                )
                continue

            else:
                # Statically indeterminate — visit block to collect errors.
                self._record(
                    phase="control_flow",
                    title=f"Condition indeterminate ({branch_label})",
                    description=(
                        f"{branch_label} condition '{expr.getText()}' cannot be resolved "
                        f"statically — visiting block to collect any errors inside it."
                    ),
                    line=expr.start.line,
                    detail="indeterminate: both branches analysed",
                )
                self.visit(blocks[i])

        if has_else and not branch_taken:
            self._record(
                phase="control_flow",
                title="Else branch taken",
                description="No preceding condition was true — executing else branch.",
                line=blocks[-1].start.line,
            )
            self.visit(blocks[-1])
        elif has_else and branch_taken:
            self._record(
                phase="control_flow",
                title="Else branch skipped",
                description="A preceding branch was taken — else block will not execute.",
                line=blocks[-1].start.line,
            )







    def visitWhileStatement(self, ctx: EVALParser.WhileStatementContext) -> None:
        _MAX_ITERATIONS = 1_000

        expr = ctx.expression()

        self._record(
            phase="control_flow",
            title="While statement",
            description=f"Evaluating initial while condition: '{expr.getText()}'.",
            line=ctx.start.line,
        )

        cond_result = self.visit(expr)
        cond_type   = self.variable_manager.get_type(cond_result)
        cond_value  = VariableManager.unwrap_value(cond_result)

        if cond_type not in (EvalType.BOOL, EvalType.UNKNOWN, None):
            self.validator.push_error(
                expr.start,
                f"while condition must be bool, got {cond_type.name}",
            )
            self._record(
                phase="control_flow",
                title="While condition type error",
                description=f"Condition has type {cond_type.name}, expected bool.",
                line=ctx.start.line,
                detail=f"error: expected BOOL, got {cond_type.name}",
            )

        if cond_value is False:
            self.validator.push_warnings(
                expr.start,
                "while condition is always false — loop body is unreachable",
            )
            self._record(
                phase="control_flow",
                title="While loop skipped (condition always false)",
                description=(
                    f"while condition '{expr.getText()}' evaluated to False — "
                    f"loop body will never execute."
                ),
                line=ctx.start.line,
                detail=f"type={cond_type}, value=False",
            )
            return

        self._record(
            phase="control_flow",
            title="While loop entered",
            description=(
                f"while condition '{expr.getText()}' "
                f"evaluated to {cond_value!r} — beginning loop execution."
            ),
            line=ctx.start.line,
            detail=f"type={cond_type}, value={cond_value!r}",
        )

        # ── Infinite-loop guard ───────────────────────────────────────────────
        # Collect every variable referenced in the condition, then check whether
        # all of them are const (i.e. can never be mutated by the loop body).
        # If they are all const the condition can never flip to False on its own,
        # so the only legal exit is a break statement.
        cond_vars      = Evaluator().collect_condition_vars(expr)
        assigned_vars  = Evaluator().assigned_vars_in_block(ctx.block())
        loop_has_break = Evaluator().has_break(ctx.block())

        # Variables in the condition that are const AND not assigned in the body.
        frozen_cond_vars = {
            v for v in cond_vars
            if self.variable_manager.exists(v)
            and self.variable_manager.get_variable(v).constant
            and v not in assigned_vars
        }

        if frozen_cond_vars and frozen_cond_vars == cond_vars:
            # Every condition variable is frozen — condition can never change.
            frozen_list = ", ".join(sorted(frozen_cond_vars))
            if not loop_has_break:
                # No break either → definite infinite loop.
                msg = (
                    f"infinite loop detected: condition variable(s) [{frozen_list}] "
                    f"are all const and the loop body contains no break statement — "
                    f"the condition '{expr.getText()}' can never become False"
                )
                self._error(
                    phase="control_flow",
                    title="Infinite loop (const condition, no break)",
                    token=expr.start,
                    msg=msg,
                    line=ctx.start.line,
                    detail="error: const condition vars, no break",
                    description=(
                        f"All variable(s) in the while condition [{frozen_list}] are declared "
                        f"const and are never assigned inside the loop body. With no break "
                        f"statement present the loop cannot terminate — infinite loop."
                    ),
                )
                return
            else:
                # Break exists but condition vars are all const → the only exit
                # is that break, which may itself be unreachable (e.g. guarded by
                # a condition that is always false).  Emit a warning so the
                # programmer is aware.
                msg = (
                    f"possible infinite loop: condition variable(s) [{frozen_list}] "
                    f"are all const — the loop can only exit via break, "
                    f"which may be unreachable"
                )
                self.validator.push_warnings(expr.start, msg)
                self._record(
                    phase="control_flow",
                    title="Possible infinite loop (const condition, break present)",
                    description=(
                        f"All variable(s) in the while condition [{frozen_list}] are const "
                        f"and never assigned in the loop body. A break exists but may not be "
                        f"reachable — verify the loop can actually terminate."
                    ),
                    line=ctx.start.line,
                    detail=f"warning: const condition vars={frozen_list}, break present",
                )

        self._loop_depth += 1
        iteration = 0
        try:
            while True:
                cond_result = self.visit(expr)
                cond_value  = VariableManager.unwrap_value(cond_result)

                if cond_value is not True:
                    self._record(
                        phase="control_flow",
                        title="While condition false — loop exited",
                        description=(
                            f"After {iteration} iteration(s), condition "
                            f"'{expr.getText()}' is now False — loop ends."
                        ),
                        line=ctx.start.line,
                    )
                    break

                if iteration >= _MAX_ITERATIONS:
                    self.validator.push_warnings(
                        expr.start,
                        f"while loop halted after {_MAX_ITERATIONS} iterations "
                        f"— possible infinite loop",
                    )
                    self._record(
                        phase="control_flow",
                        title="While loop halted (max iterations reached)",
                        description=(
                            f"Loop exceeded the {_MAX_ITERATIONS}-iteration safety "
                            f"cap and was stopped to prevent an infinite loop."
                        ),
                        line=ctx.start.line,
                    )
                    break

                iteration += 1
                self._record(
                    phase="control_flow",
                    title=f"While iteration {iteration}",
                    description=(
                        f"Condition '{expr.getText()}' = {cond_value!r} — "
                        f"executing loop body (iteration {iteration})."
                    ),
                    line=ctx.block().start.line,
                    detail=f"iteration={iteration}, condition={cond_value!r}",
                )

                try:
                    self.visit(ctx.block())

                except ContinueSignal:
                    self._record(
                        phase="control_flow",
                        title=f"Continue — iteration {iteration}",
                        description=(
                            f"continue hit on iteration {iteration}; "
                            f"re-evaluating loop condition."
                        ),
                        line=ctx.start.line,
                    )
                    continue

                except BreakSignal:
                    self._record(
                        phase="control_flow",
                        title=f"Break — loop exited at iteration {iteration}",
                        description=(
                            f"break hit on iteration {iteration}; "
                            f"exiting loop."
                        ),
                        line=ctx.start.line,
                    )
                    break

        finally:
            self._loop_depth -= 1
            self._record(
                phase="control_flow",
                title="While loop complete",
                description=(
                    f"Loop finished after {iteration} iteration(s). "
                    f"Loop depth restored to {self._loop_depth}."
                ),
                line=ctx.start.line,
                detail=f"iterations={iteration}, loop_depth={self._loop_depth}",
            )

    def visitTryStatement(self, ctx: EVALParser.TryStatementContext) -> None:
        try_block   = ctx.block(0)
        catch_block = ctx.block(1)
        ident_tok   = ctx.IDENTIFIER().getSymbol()
        catch_name  = ident_tok.text
        col, line   = self.validator.tok_col_line(ident_tok)

        self._record(
            phase="control_flow",
            title="Try/catch statement",
            description=f"Processing try block with catch parameter '{catch_name}' on line {line}.",
            line=ctx.start.line,
        )

        errors_before_kw = len(self.errors)
        is_reserved = self.validator.check_reserved_keyword(catch_name, ident_tok)
        if is_reserved:
            # Strip the error check_reserved_keyword pushed and downgrade to warning.
            while len(self.errors) > errors_before_kw:
                self.errors.pop()
            self.validator.push_warnings(
                ident_tok,
                f"'{catch_name}' is a reserved identifier; "
                f"using it as a catch parameter name is discouraged",
            )
            self._record(
                phase="control_flow",
                title=f"Reserved catch parameter (warning): {catch_name}",
                description=(
                    f"'{catch_name}' is a reserved identifier — "
                    f"warning issued, analysis continues."
                ),
                line=line,
                changed=catch_name,
                detail="warning: reserved identifier — downgraded from error",
            )


        self._record(
            phase="control_flow",
            title="Entering try block",
            description="Visiting try block — any runtime exceptions will be intercepted.",
            line=try_block.start.line,
        )

        errors_before_try              = len(self.errors)
        caught_exception: Exception | None = None
        caught_line: int               = try_block.start.line

        try:
            self.visit(try_block)
        except (BreakSignal, ContinueSignal):
            raise
        except self._CATCHABLE as exc:
            caught_exception = exc
            caught_line      = try_block.start.line

        errors_after_try = len(self.errors)

        # ── Record what happened inside the try block ─────────────────────────
        if caught_exception is not None:
            self._record(
                phase="control_flow",
                title="Exception intercepted in try block",
                description=(
                    f"[{type(caught_exception).__name__}] raised inside try block: "
                    f"{caught_exception}"
                ),
                line=caught_line,
                detail=f"exception={type(caught_exception).__name__}: {caught_exception}",
            )
        elif errors_after_try > errors_before_try:
            self._record(
                phase="control_flow",
                title="Semantic errors in try block",
                description=(
                    f"{errors_after_try - errors_before_try} new semantic error(s) "
                    f"produced inside the try block."
                ),
                line=try_block.start.line,
                detail=f"new_errors={errors_after_try - errors_before_try}",
            )
        else:
            self._record(
                phase="control_flow",
                title="Try block completed without errors",
                description="No exceptions or semantic errors were raised in the try block.",
                line=try_block.start.line,
            )

        # ── Decide whether to enter the catch block ───────────────────────────
        has_error = caught_exception is not None or errors_after_try > errors_before_try

        if not has_error:
            self._record(
                phase="control_flow",
                title="Catch block skipped",
                description="No errors in the try block — catch block will not execute.",
                line=catch_block.start.line,
            )
            return

        # ── Build catch_var value from exception + validator errors ───────────
        # ErrorResponse fields: message (str), line_number (int), column_number (int)
        parts: list[str] = []
        if caught_exception is not None:
            exc_type = type(caught_exception).__name__
            parts.append(f" {exc_type}: ")
        new_validator_errors = self.errors[errors_before_try:]
        for err in new_validator_errors:
            parts.append(f"line {err.line_number}: {err.message}")
        error_details: str = " ".join(parts) if parts else "error occurred"

        # ── Catch block — its own fresh scope, separate from the try scope ────
        self.variable_manager.enter_scope("catch")
        try:

            catch_var = Variable(
                name=catch_name,
                type=EvalType.STRING,
                value=error_details,
                position=Position(line=line, column=col),
            )
            self.variable_manager.define(catch_var)

            self._record(
                phase="control_flow",
                title=f"Catch variable defined: {catch_name}",
                description=(
                    f"'{catch_name}' defined as STRING in catch scope with error details."
                ),
                line=line,
                changed=catch_name,
                detail=f"type=STRING, value={error_details!r}",
            )

            self._record(
                phase="control_flow",
                title="Entering catch block",
                description=f"Visiting catch block — '{catch_name}' is available as a STRING.",
                line=catch_block.start.line,
            )

            # Visit statements directly — do NOT call self.visit(catch_block)
            # because visitBlock would push a second scope on top of this one.
            statements = list(catch_block.statement())
            for i, stmt in enumerate(statements):
                self._record(
                    phase="control_flow",
                    title=f"Catch statement {i + 1}/{len(statements)}",
                    description=f"Visiting catch statement {i + 1}: '{stmt.getText()}'.",
                    line=stmt.start.line,
                )
                try:
                    self.visit(stmt)
                except (BreakSignal, ContinueSignal) as signal:
                    remaining = statements[i + 1:]
                    if remaining:
                        keyword = "break" if isinstance(signal, BreakSignal) else "continue"
                        self.validator.push_warnings(
                            remaining[0].start,
                            f"{len(remaining)} unreachable statement(s) after "
                            f"'{keyword}' will never execute",
                        )
                        self._record(
                            phase="control_flow",
                            title=f"Unreachable statements in catch after '{keyword}'",
                            description=(
                                f"{len(remaining)} statement(s) after '{keyword}' "
                                f"in catch block will never execute."
                            ),
                            line=remaining[0].start.line,
                        )
                    raise

        finally:
            self._record(
                phase="control_flow",
                title="Exiting catch block",
                description=f"Catch block complete — releasing '{catch_name}' from scope.",
                line=catch_block.stop.line if catch_block.stop else line,
            )
            self.variable_manager.exit_scope()

    def visitBreakStatement(self, ctx: EVALParser.BreakStatementContext) -> None:
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

    def visitContinueStatement(self, ctx: EVALParser.ContinueStatementContext) -> None:
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


    # ─────────────────────────────────────────────────────────────────────────
    # Binary / unary expressions
    # ─────────────────────────────────────────────────────────────────────────

    def visitLogicalOrExpr(self, ctx: EVALParser.LogicalOrExprContext) -> bool | None:
        self._record(
            phase="expression",
            title="Logical OR (||)",
            description=f"Evaluating left operand of '||': '{ctx.expression(0).getText()}'.",
            line=ctx.start.line,
        )
        left_result = self.visit(ctx.expression(0))
        lt          = self.variable_manager.get_type(left_result)
        left_val    = VariableManager.unwrap_value(left_result)

        if left_val is True:
            self.validator.check_logical_operands("||", lt, lt, ctx.start)
            self._record(
                phase="expression",
                title="Logical OR short-circuit (left=True)",
                description="Left operand is True — right not evaluated (short-circuit). Result: True.",
                line=ctx.start.line,
                detail="short-circuit: True || any → True",
            )
            return True

        self._record(
            phase="expression",
            title="Logical OR — evaluating right operand",
            description=f"Left is {left_val!r} — evaluating right: '{ctx.expression(1).getText()}'.",
            line=ctx.start.line,
        )
        right_result = self.visit(ctx.expression(1))
        rt           = self.variable_manager.get_type(right_result)
        right_val    = VariableManager.unwrap_value(right_result)

        self.validator.check_logical_operands("||", lt, rt, ctx.start)

        if isinstance(left_val, bool) and isinstance(right_val, bool):
            result = left_val or right_val
            self._record(
                phase="expression",
                title="Logical OR result",
                description=f"{left_val!r} || {right_val!r} = {result!r}.",
                line=ctx.start.line,
                detail=f"left={left_val!r}, right={right_val!r}, result={result!r}",
            )
            return result

        self._record(
            phase="expression",
            title="Logical OR result (indeterminate)",
            description="One or both operands are not statically known — result is indeterminate.",
            line=ctx.start.line,
        )
        return None

    def visitLogicalAndExpr(self, ctx: EVALParser.LogicalAndExprContext) -> bool | None:
        self._record(
            phase="expression",
            title="Logical AND (&&)",
            description=f"Evaluating left operand of '&&': '{ctx.expression(0).getText()}'.",
            line=ctx.start.line,
        )
        left_result = self.visit(ctx.expression(0))
        lt          = self.variable_manager.get_type(left_result)
        left_val    = VariableManager.unwrap_value(left_result)

        if left_val is False:
            self.validator.check_logical_operands("&&", lt, lt, ctx.start)
            self._record(
                phase="expression",
                title="Logical AND short-circuit (left=False)",
                description="Left operand is False — right not evaluated (short-circuit). Result: False.",
                line=ctx.start.line,
                detail="short-circuit: False && any → False",
            )
            return False

        self._record(
            phase="expression",
            title="Logical AND — evaluating right operand",
            description=f"Left is {left_val!r} — evaluating right: '{ctx.expression(1).getText()}'.",
            line=ctx.start.line,
        )
        right_result = self.visit(ctx.expression(1))
        rt           = self.variable_manager.get_type(right_result)
        right_val    = VariableManager.unwrap_value(right_result)

        self.validator.check_logical_operands("&&", lt, rt, ctx.start)

        if isinstance(left_val, bool) and isinstance(right_val, bool):
            result = left_val and right_val
            self._record(
                phase="expression",
                title="Logical AND result",
                description=f"{left_val!r} && {right_val!r} = {result!r}.",
                line=ctx.start.line,
                detail=f"left={left_val!r}, right={right_val!r}, result={result!r}",
            )
            return result

        self._record(
            phase="expression",
            title="Logical AND result (indeterminate)",
            description="One or both operands are not statically known — result is indeterminate.",
            line=ctx.start.line,
        )
        return None

    def visitEqualityExpr(self, ctx: EVALParser.EqualityExprContext) -> Literal[EvalType.BOOL] | bool:
        op = ctx.op.text
        self._record(
            phase="expression",
            title=f"Equality expression ({op})",
            description=f"Evaluating '{ctx.expression(0).getText()}' {op} '{ctx.expression(1).getText()}'.",
            line=ctx.start.line,
        )

        left_visited  = self.visit(ctx.expression(0))
        right_visited = self.visit(ctx.expression(1))
        lt = self.variable_manager.get_type(left_visited)
        rt = self.variable_manager.get_type(right_visited)

        self.validator.check_float_equality(op, lt, rt, ctx.start)

        left_val, right_val = self._run_comparison(ctx, op, "Equality")

        result = Evaluator.evaluate_relational(left_val, op, right_val)
        self._record(
            phase="expression",
            title=f"Equality result ({op})",
            description=f"{left_val!r} {op} {right_val!r} → {result!r} (left: {lt.name}, right: {rt.name}).",
            line=ctx.start.line,
            detail=f"left={left_val!r} ({lt.name}), right={right_val!r} ({rt.name}), result={result!r}",
        )
        return result

    def visitRelationalExpr(self, ctx: EVALParser.RelationalExprContext) -> bool:
        op = ctx.op.text
        self._record(
            phase="expression",
            title=f"Relational expression ({op})",
            description=f"Evaluating '{ctx.expression(0).getText()}' {op} '{ctx.expression(1).getText()}'.",
            line=ctx.start.line,
        )

        left_val, right_val = self._run_comparison(ctx, op, "Relational")

        result = Evaluator.evaluate_relational(left_val, op, right_val)
        self._record(
            phase="expression",
            title=f"Relational result ({op})",
            description=f"{left_val!r} {op} {right_val!r} → {result!r}.",
            line=ctx.start.line,
            detail=f"left={left_val!r}, right={right_val!r}, result={result!r}",
        )
        return result

    def visitAdditiveExpr(self, ctx: EVALParser.AdditiveExprContext) -> Any:
        op  = ctx.op.text
        lhs = self.visit(ctx.expression(0))
        rhs = self.visit(ctx.expression(1))

        lt = self.variable_manager.get_type(lhs)
        rt = self.variable_manager.get_type(rhs)

        self._record(
            phase="expression",
            title=f"Additive expression ({op})",
            description=(
                f"'{ctx.expression(0).getText()}' {op} '{ctx.expression(1).getText()}' — "
                f"left: {VariableManager.unwrap_value(lhs)!r} ({lt.name}), "
                f"right: {VariableManager.unwrap_value(rhs)!r} ({rt.name})."
            ),
            line=ctx.start.line,
            detail=f"op={op}, lt={lt.name}, rt={rt.name}",
        )

        # numeric_result() pushes the error internally; EMPTY contains sentinel
        # bad-result types (UNKNOWN, NULL) — abort only when result IS one of those.
        result_type = self.validator.numeric_result(op, lt, rt, ctx.start)
        if result_type in TypeHandler.EMPTY:
            self._record(
                phase="expression",
                title=f"Additive type error ({op})",
                description=f"Operator '{op}' cannot be applied to '{lt.name}' and '{rt.name}'.",
                line=ctx.start.line,
                detail=f"error: incompatible types {lt.name} {op} {rt.name}",
            )
            raise ArithmeticError(
                f"additive operator '{op}' cannot be applied to "
                f"'{lt.name}' and '{rt.name}'"
            )

        return self._eval_postfix(ctx, "Additive", op, result_type)

    def visitMultiplicativeExpr(self, ctx: EVALParser.MultiplicativeExprContext) -> Any:
        op  = ctx.op.text
        lhs = self.visit(ctx.expression(0))
        rhs = self.visit(ctx.expression(1))

        lt = self.variable_manager.get_type(lhs)
        rt = self.variable_manager.get_type(rhs)

        self._record(
            phase="expression",
            title=f"Multiplicative expression ({op})",
            description=(
                f"'{ctx.expression(0).getText()}' {op} '{ctx.expression(1).getText()}' — "
                f"left: {VariableManager.unwrap_value(lhs)!r} ({lt.name}), "
                f"right: {VariableManager.unwrap_value(rhs)!r} ({rt.name})."
            ),
            line=ctx.start.line,
            detail=f"op={op}, lt={lt.name}, rt={rt.name}",
        )

        result_type = self.validator.numeric_result(op, lt, rt, ctx.start)
        if result_type == EvalType.UNKNOWN:
            self._record(
                phase="expression",
                title=f"Multiplicative type error ({op})",
                description=f"Operator '{op}' cannot be applied to '{lt.name}' and '{rt.name}'.",
                line=ctx.start.line,
                detail=f"error: incompatible types {lt.name} {op} {rt.name}",
            )
            raise ArithmeticError(
                f"multiplicative operator '{op}' cannot be applied to "
                f"'{lt.name}' and '{rt.name}'"
            )

        if op == "%" and result_type not in TypeHandler.EMPTY:
            self.validator.check_modulo_float(lt, rt, ctx.start)

        try:
            return self._eval_postfix(ctx, "Multiplicative", op, result_type)
        except ZeroDivisionError as e:
            op_name = "division" if op == "/" else "modulo"
            msg     = f"{op_name} by zero"
            self.validator.push_error(ctx.start, msg)
            self._record(
                phase="expression",
                title=f"Division by zero ({op})",
                description=f"{op_name.capitalize()} by zero.",
                line=ctx.start.line,
                detail=f"error: {msg}",
            )
            raise ArithmeticError(f"{op_name} by zero") from e

    def visitUnaryMinusExpr(self, ctx: EVALParser.UnaryMinusExprContext) -> Any:
        self._record(
            phase="expression",
            title="Unary minus (-)",
            description=f"Evaluating unary minus on: '{ctx.expression().getText()}'.",
            line=ctx.start.line,
        )
        inner = self.visit(ctx.expression())
        t     = self.variable_manager.get_type(inner)

        if t not in TypeHandler.NUMERIC:
            self._error(
                phase="expression",
                title="Unary minus type error",
                token=ctx.start,
                msg=f"unary '-' requires a numeric operand, got {t.name}",
                line=ctx.start.line,
                description=f"Cannot apply unary '-' to type {t.name} — expected a numeric type.",
                detail=f"error: expected NUMERIC, got {t.name}",
            )
            raise ArithmeticError(
                f"unary '-' requires a numeric operand, got '{t.name}'"
            )

        expr_string = ExpressionStringBuilder.build(ctx, self.variable_manager, self.visit)
        if expr_string is not None:
            result = Postfix.get_result(expr_string)
            self._record(
                phase="expression",
                title="Unary minus result",
                description=f"Unary minus on '{ctx.expression().getText()}' → {result!r}.",
                line=ctx.start.line,
                detail=f"operand_type={t.name}, result={result!r}",
            )
            return result

        return None

    def visitUnaryNotExpr(self, ctx: EVALParser.UnaryNotExprContext) -> bool | EvalType:
        self._record(
            phase="expression",
            title="Unary NOT (!)",
            description=f"Evaluating logical NOT on: '{ctx.expression().getText()}'.",
            line=ctx.start.line,
        )
        inner = self.visit(ctx.expression())
        t     = self.variable_manager.get_type(inner)

        if t != EvalType.BOOL:
            self.validator.push_warnings(
                ctx.start,
                f"'!' applied to {t.name} — expected bool",
            )
            self._record(
                phase="expression",
                title="Unary NOT type error",
                description=f"'!' applied to non-bool type {t.name} — expected BOOL.",
                line=ctx.start.line,
                detail=f"error: expected BOOL, got {t.name}",
            )
            raise TypeError(
                f"'!' requires a bool operand, got '{t.name}'"
            )

        val = VariableManager.unwrap_value(inner)
        if isinstance(val, bool):
            result = not val
            self._record(
                phase="expression",
                title="Unary NOT result",
                description=f"!{val!r} → {result!r}.",
                line=ctx.start.line,
                detail=f"operand={val!r}, result={result!r}",
            )
            return result

        self._record(
            phase="expression",
            title="Unary NOT result (indeterminate)",
            description="Operand value not statically known — returning False as safe default.",
            line=ctx.start.line,
        )
        return False

    def visitParenExpr(self, ctx: EVALParser.ParenExprContext) -> Any:
        result = self.visit(ctx.expression())
        self._record(
            phase="expression",
            title="Parenthesised expression result",
            description=f"'({ctx.expression().getText()})' → {VariableManager.unwrap_value(result)!r}.",
            line=ctx.start.line,
            detail=f"result={VariableManager.unwrap_value(result)!r}",
        )
        return result

    def visitBuiltinExpr(self, ctx: EVALParser.BuiltinExprContext) -> Any:
        return self.visit(ctx.builtinFunc())


    # ─────────────────────────────────────────────────────────────────────────
    # Identifier / literals
    # ─────────────────────────────────────────────────────────────────────────

    def visitIdentExpr(self, ctx: EVALParser.IdentExprContext) -> Variable | None:
        tok  = ctx.IDENTIFIER().getSymbol()
        name = tok.text
        self._record(
            phase="expression",
            title=f"Identifier lookup: {name}",
            description=f"Resolving identifier '{name}' in scope.",
            line=tok.line,
        )
        try:
            var = self.variable_manager.get_variable(name)
            self._record(
                phase="expression",
                title=f"Identifier resolved: {name}",
                description=(
                    f"'{name}' found — value: {var.value!r}, "
                    f"type: {self.variable_manager.get_type(var).name}."
                ),
                line=tok.line,
                detail=f"value={var.value!r}, type={self.variable_manager.get_type(var).name}",
            )
            return var
        except EVALNameException as e:
            self._error(
                phase="expression",
                title=f"Undeclared identifier: {name}",
                token=ctx.start,
                msg=str(e),
                line=tok.line,
                description=f"'{name}' is not declared in any accessible scope.",
                detail=f"error: {e}",
            )
            return None

    def visitIntLiteral(self, ctx) -> int:
        value = int(ctx.INTEGER().getText())
        self._record(
            phase="expression",
            title=f"Integer literal: {value}",
            description=f"Integer literal {value} evaluated.",
            line=ctx.start.line,
            detail=f"value={value}, type=INT",
        )
        return value

    def visitRealLiteral(self, ctx) -> float:
        value = float(ctx.REAL().getText())
        self._record(
            phase="expression",
            title=f"Float literal: {value}",
            description=f"Float literal {value} evaluated.",
            line=ctx.start.line,
            detail=f"value={value}, type=FLOAT",
        )
        return value

    def visitStringLiteral(self, ctx) -> str:
        value = ctx.STRING().getText()
        self._record(
            phase="expression",
            title="String literal",
            description=f"String literal {value!r} evaluated.",
            line=ctx.start.line,
            detail=f"value={value!r}, type=STRING",
        )
        return value

    def visitTrueLiteral(self, ctx) -> bool:
        self._record(
            phase="expression",
            title="Boolean literal: true",
            description="Literal 'true' evaluated.",
            line=ctx.start.line,
            detail="value=True, type=BOOL",
        )
        return True

    def visitFalseLiteral(self, ctx) -> bool:
        self._record(
            phase="expression",
            title="Boolean literal: false",
            description="Literal 'false' evaluated.",
            line=ctx.start.line,
            detail="value=False, type=BOOL",
        )
        return False

    def visitNullLiteral(self, _ctx) -> None:
        self._record(
            phase="expression",
            title="Null literal",
            description="Literal 'null' evaluated.",
            line=_ctx.start.line,
            detail="value=None, type=NULL",
        )
        return None

    def visitMacroExpr(self, ctx: EVALParser.MacroExprContext) -> Any:
        return self.visit(ctx.macroValue())


    # ─────────────────────────────────────────────────────────────────────────
    # Built-in functions
    # ─────────────────────────────────────────────────────────────────────────

    def visitBuiltinFunc(self, ctx: EVALParser.BuiltinFuncContext) -> Any:
        return self.visitChildren(ctx)

    def visitCastCall(self, ctx) -> Any:
        expression  = ctx.expression()
        target_text = ctx.type_().getText()
        target_type = TypeHandler.get_eval_type(target_text)

        self._record(
            phase="expression",
            title=f"cast() — target: {target_text}",
            description=f"Evaluating cast({expression.getText()}, {target_text}).",
            line=ctx.start.line,
        )

        visited_val = self.visit(expression)

        _INVALID_CAST_TARGETS = {EvalType.NULL, EvalType.UNKNOWN}
        if target_type in _INVALID_CAST_TARGETS:
            msg = (
                f"invalid cast target type '{target_text}': "
                f"cannot cast to '{target_type.value}'"
            )
            self._error(
                phase="expression",
                title="cast() invalid target",
                token=ctx.type_().start,
                msg=msg,
                line=ctx.start.line,
            )
            raise CastException(msg)

        if visited_val is None:
            msg = "cast argument could not be resolved"
            self._error(
                phase="expression",
                title="cast() unresolved argument",
                token=expression.start,
                msg=msg,
                line=ctx.start.line,
            )
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
            self._error(
                phase="expression",
                title="cast() unsupported argument type",
                token=expression.start,
                msg=msg,
                line=ctx.start.line,
            )
            raise CastException(msg)

        if val is None:
            msg = "cast argument evaluates to null and cannot be cast"
            self._error(
                phase="expression",
                title="cast() null argument",
                token=expression.start,
                msg=msg,
                line=ctx.start.line,
            )
            raise CastException(msg)

        result = Evaluator.cast(val, target_type)
        if result is None:
            msg = f"cast failed: could not convert '{val!r}' to '{target_type.value}'"
            self._error(
                phase="expression",
                title="cast() conversion failed",
                token=expression.start,
                msg=msg,
                line=ctx.start.line,
            )
            raise CastException(msg)

        self._record(
            phase="expression",
            title="cast() result",
            description=f"cast({val!r}, {target_text}) → {result!r}.",
            line=ctx.start.line,
            detail=f"input={val!r}, target={target_text}, result={result!r}",
        )
        return result

    def visitPowCall(self, ctx: EVALParser.PowCallContext) -> Any:
        left_expr  = ctx.expression(0)
        right_expr = ctx.expression(1)

        self._record(
            phase="expression",
            title="pow()",
            description=f"Evaluating pow({left_expr.getText()}, {right_expr.getText()}).",
            line=ctx.start.line,
        )


        try:
            result = self._visit_binary_numeric_call(ctx, pow, "pow")
            if result is None:
                raise PowException("pow: result could not be resolved")
        except (ValueError, TypeError, ZeroDivisionError) as e:
            msg = (
                f"pow() failed for operands "
                f"'{self.visit(left_expr)!r}' and '{self.visit(right_expr)!r}': {e}"
            )
            self._error(phase="expression", title="pow() computation failed", token=left_expr.start, msg=msg, line=ctx.start.line)
            raise PowException(msg) from e


        return result



    def visitSqrtCall(self, ctx: EVALParser.SqrtCallContext) -> Any:
        expression = ctx.expression()
        self._record(
            phase="expression",
            title="sqrt()",
            description=f"Evaluating sqrt({expression.getText()}).",
            line=ctx.start.line,
        )

        return self._visit_unary_numeric_call(ctx, sqrt, "sqrt")


    def visitMinCall(self, ctx: EVALParser.MinCallContext) -> Any:
        self._record(
            phase="expression",
            title="min()",
            description=f"Evaluating min({ctx.expression(0).getText()}, {ctx.expression(1).getText()}).",
            line=ctx.start.line,
        )
        return self._visit_binary_numeric_call(ctx, min, "min")

    def visitMaxCall(self, ctx: EVALParser.MaxCallContext) -> Any:
        self._record(
            phase="expression",
            title="max()",
            description=f"Evaluating max({ctx.expression(0).getText()}, {ctx.expression(1).getText()}).",
            line=ctx.start.line,
        )
        return self._visit_binary_numeric_call(ctx, max, "max")


    def visitRoundCall(self, ctx: EVALParser.RoundCallContext) -> Any:
        self._record(
            phase="expression",
            title="round()",
            description=f"Evaluating round({ctx.expression().getText()}).",
            line=ctx.start.line,
        )
        return self._visit_unary_numeric_call(ctx, round, "round")

    def visitAbsCall(self, ctx: EVALParser.AbsCallContext) -> Any:
        self._record(
            phase="expression",
            title="abs()",
            description=f"Evaluating abs({ctx.expression().getText()}).",
            line=ctx.start.line,
        )
        return self._visit_unary_numeric_call(ctx, abs, "abs")

    def visitMacroValue(self, ctx: EVALParser.MacroValueContext) -> Any:

        key: str = ctx.getText()
        macro_info = MacroValue.get_macro_info(key)

        if macro_info:
            self._record(
                phase="expression",
                title=macro_info.title,
                description=macro_info.description,
                line=ctx.start.line,
                detail=f"value={macro_info.value}",
            )

            return macro_info.value

        self._record(
            phase="expression",
            title="Macro: unknown",
            description="Encountered an unrecognised macro — returning None.",
            line=ctx.start.line,
        )
        return None