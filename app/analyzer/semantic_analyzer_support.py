from __future__ import annotations

from math import sqrt
from typing import TYPE_CHECKING, Any, Literal

from app.eval.control_flow_analyzer import ControlFlowAnalyzer
from app.eval.evaluator import Evaluator
from app.eval.expression_builder import ExpressionStringBuilder
from app.eval.handler.comparison_handler import ComparisonHandler
from app.eval.postfix import Postfix
from app.eval.print_formatter import PrintFormatter
from app.eval.variable_manager import VariableManager
from app.models.MacroValue import MacroValue
from app.models.Types import EvalType, TypeHandler
from app.models.Variable import Position, Variable
from app.models.custom_exceptions import (
    BreakSignal,
    CastException,
    CoercionException,
    ContinueSignal,
    EVALNameException,
    PowException,
)
from generated.EVALParser import EVALParser

if TYPE_CHECKING:
    from app.analyzer.semantic_analyzer import SemanticAnalyzer


class SemanticAnalyzerSupport:
    _MAX_LOOP_ITERATIONS = 1_000
    _INVALID_CAST_TARGETS = {EvalType.NULL, EvalType.UNKNOWN}
    CATCHABLE_EXCEPTIONS = (
        ArithmeticError,
        ZeroDivisionError,
        TypeError,
        CastException,
        PowException,
        EVALNameException,
        CoercionException,
        ValueError,
    )

    def __init__(self, analyzer: "SemanticAnalyzer") -> None:
        self.analyzer = analyzer

    @property
    def validator(self):
        return self.analyzer.validator

    @property
    def variable_manager(self):
        return self.analyzer.variable_manager

    @property
    def recorder(self):
        return self.analyzer.recorder

    def record(
        self,
        phase: str,
        title: str,
        description: str,
        line: int = 0,
        changed: str = "",
        detail: str = "",
        output_line: Any = None,
    ) -> None:
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

    def error(
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
        self.validator.push_error(token, msg)
        self.record(
            phase=phase,
            title=title,
            description=description or msg,
            line=line,
            changed=changed,
            detail=detail or f"error: {msg}",
        )

    def handle_variable_declaration(self, ctx: EVALParser.VariableDeclarationContext) -> None:
        type_text = ctx.type_().getText()
        decl_type = TypeHandler.get_eval_type(type_text)
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name = ident_tok.text
        line = ident_tok.line

        if self.validator.check_reserved_keyword(name, ident_tok):
            self.record(
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

        in_current = self.variable_manager.is_defined_in_current_scope(name)
        exists_outer = self.variable_manager.exists(name)
        self.validator.check_shadow(
            name=name,
            token=ident_tok,
            is_in_current=in_current,
            exists_outer=exists_outer,
        )
        if not in_current and exists_outer:
            self.record(
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
            self.error(
                phase="declaration",
                title=f"Duplicate declaration: {name}",
                token=ident_tok,
                msg=msg,
                line=line,
                changed=name,
                detail="error: duplicate declaration",
            )
            return

        var_value = self.analyzer.visit(ctx.expression())
        val_type = self.variable_manager.get_type(var_value)

        cast_target = self.validator.direct_cast_type(ctx.expression())
        if cast_target is not None and cast_target != decl_type:
            msg = (
                f"cast-type mismatch: cast produces '{cast_target.name}' "
                f"but variable '{name}' is declared as '{type_text}' — "
                f"change either the cast target or the variable type"
            )
            self.error(
                phase="declaration",
                title=f"Cast-type mismatch: {name}",
                token=ident_tok,
                msg=msg,
                line=line,
                changed=name,
                detail=f"error: cast target '{cast_target.name}' != declared '{type_text}'",
            )
            return

        if val_type in TypeHandler.EMPTY or decl_type in TypeHandler.EMPTY:
            msg = (
                f"cannot initialise '{type_text}' variable '{name}' "
                f"with value of type '{val_type.name}'"
            )
            self.error(
                phase="declaration",
                title=f"Type error: {name}",
                token=ident_tok,
                msg=msg,
                line=line,
                changed=name,
                detail=f"error: incompatible types — declared '{type_text}', got '{val_type.name}'",
            )
            return

        self.validator.check_narrowing(decl_type, val_type, name, ident_tok)
        if decl_type == EvalType.INT and val_type == EvalType.FLOAT:
            self.record(
                phase="declaration",
                title=f"Narrowing warning: {name}",
                description=f"Float value implicitly narrowed to int for '{name}' — fractional part will be lost.",
                line=line,
                detail="warning: float → int narrowing",
            )

        try:
            coerced_val = Evaluator.coerce_to_declared_type(
                val=VariableManager.unwrap_value(var_value),
                decl_type=decl_type,
                val_type=val_type,
                name=name,
                type_text=type_text,
            )
            self.record(
                phase="declaration",
                title=f"Coercion for {name}",
                description=f"Value coerced to '{type_text}': {coerced_val!r}.",
                line=line,
                detail=f"coerced={coerced_val!r}",
            )
        except CoercionException as exc:
            self.error(
                phase="declaration",
                title=f"Coercion failed: {name}",
                token=ident_tok,
                msg=str(exc),
                line=line,
                description=f"Could not coerce value to '{type_text}': {exc}",
                detail=f"error: {exc}",
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

        self.record(
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

    def handle_const_declaration(self, ctx: EVALParser.ConstDeclarationContext) -> None:
        variable_declaration = ctx.variableDeclaration()
        ident_sym = variable_declaration.IDENTIFIER().getSymbol()
        name = ident_sym.text
        errors_before = len(self.analyzer.errors)
        self.analyzer.visit(variable_declaration)

        if len(self.analyzer.errors) > errors_before:
            return

        try:
            variable = self.variable_manager.get_variable(name)
            variable.constant = True
            self.variable_manager.define(variable)
            self.record(
                phase="declaration",
                title=f"Declared const: {name}",
                description=f"Variable '{name}' marked as constant — reassignment is now forbidden.",
                line=ident_sym.line,
                changed=name,
                detail=f"const=True, value={variable.value!r}",
            )
        except EVALNameException as exc:
            self.error(
                phase="declaration",
                title=f"Const lookup failed: {name}",
                token=ident_sym,
                msg=f"{exc} in this scope",
                line=ctx.start.line,
                description=f"Could not mark '{name}' as const — variable not found in scope: {exc}",
                detail=f"error: {exc}",
            )

    def handle_assignment(self, ctx: EVALParser.AssignmentContext) -> None:
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name = ident_tok.text
        op = ctx.assignOp().getText()
        line = ident_tok.line

        try:
            variable = self.variable_manager.get_variable(name)
            self.record(
                phase="assignment",
                title=f"Variable found: {name}",
                description=(
                    f"'{name}' resolved — current value: {variable.value!r}, "
                    f"type: {self.variable_manager.get_type(variable).name}."
                ),
                line=line,
                detail=f"current_value={variable.value!r}",
            )
        except EVALNameException as exc:
            self.error(
                phase="assignment",
                title=f"Undeclared variable: {name}",
                token=ident_tok,
                msg=f"{exc} in this scope",
                line=line,
                description=f"'{name}' is not declared in any accessible scope — assignment aborted.",
                detail=f"error: {exc}",
            )
            return

        if variable.constant:
            self.error(
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

        rhs = self.analyzer.visit(ctx.expression())
        rhs_type = self.variable_manager.get_type(rhs)
        rhs_val = VariableManager.unwrap_value(rhs)
        var_type = self.variable_manager.get_type(variable)
        old_value = variable.value

        self.record(
            phase="assignment",
            title=f"RHS evaluated for {name}",
            description=f"RHS = {rhs_val!r} (type: {rhs_type.name}), LHS type: {var_type.name}.",
            line=line,
            detail=f"rhs_val={rhs_val!r}, rhs_type={rhs_type.name}, var_type={var_type.name}",
        )

        if op == "=":
            if var_type not in TypeHandler.EMPTY and not self.validator.types_compatible(var_type, rhs_type):
                self.error(
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
            if Evaluator.is_non_numeric(var_type):
                self.error(
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
                self.error(
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
                    self.error(
                        phase="assignment",
                        title=f"Compound op failed: {name}",
                        token=ident_tok,
                        msg=err,
                        line=line,
                        description=f"Compound op '{op}' failed: {err}",
                        detail=f"error: {err}",
                    )
                    return
                if new_val is not None:
                    new_val_type = self.variable_manager.get_type(new_val)
                    self.validator.check_narrowing(var_type, new_val_type, name, ident_tok)
                    coerced, err = Evaluator.coerce_for_assignment(new_val, var_type, new_val_type, name)
                    if err:
                        self.error(
                            phase="assignment",
                            title=f"Coercion failed: {name}",
                            token=ident_tok,
                            msg=err,
                            line=line,
                            description=f"Compound op coercion failed: {err}",
                            detail=f"error: {err}",
                        )
                        return
                    variable.value = coerced

        self.variable_manager.define(variable)
        self.record(
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

    def handle_print_statement(self, ctx: EVALParser.PrintStatementContext) -> str:
        args = list(ctx.printArg())
        parts: list[str] = []

        for index, arg in enumerate(args):
            val = self.analyzer.visit(arg)
            raw = VariableManager.unwrap_value(val)
            part = PrintFormatter.format_arg(raw)
            parts.append(part)
            self.record(
                phase="output",
                title=f"Print arg {index + 1}/{len(args)}",
                description=f"Argument {index + 1} ('{arg.getText()}') evaluated to {raw!r}.",
                line=arg.start.line,
                detail=f"arg={arg.getText()!r}, value={raw!r}",
            )

        output_line = " ".join(parts)
        self.record(
            phase="output",
            title="Print",
            description=f"print({', '.join(repr(p) for p in parts)}) → {output_line!r}",
            line=ctx.start.line,
            output_line=output_line,
        )
        return output_line

    def handle_if_statement(self, ctx: EVALParser.IfStatementContext) -> None:
        expressions = ctx.expression()
        blocks = ctx.block()
        has_else = len(blocks) > len(expressions)

        self.record(
            phase="control_flow",
            title="If statement",
            description=(
                f"if with {len(expressions)} condition(s)"
                f"{', has else branch' if has_else else ''}."
            ),
            line=ctx.start.line,
        )

        branch_taken = False
        for index, expr in enumerate(expressions):
            branch_label = "if" if index == 0 else f"else if [{index}]"
            self.record(
                phase="control_flow",
                title=f"Evaluating condition ({branch_label})",
                description=f"Evaluating {branch_label} condition: '{expr.getText()}'.",
                line=expr.start.line,
            )

            cond_result = self.analyzer.visit(expr)
            cond_type = self.variable_manager.get_type(cond_result)
            cond_value = VariableManager.unwrap_value(cond_result)

            if cond_type != EvalType.BOOL:
                self.validator.push_error(
                    expr.start,
                    f"{branch_label} condition must be bool, got {cond_type.name}",
                )
                self.record(
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

            self.record(
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
                self.record(
                    phase="control_flow",
                    title=f"Branch taken ({branch_label})",
                    description=f"Condition is True — entering {branch_label} block.",
                    line=blocks[index].start.line,
                )
                self.analyzer.visit(blocks[index])
                branch_taken = True
                break

            if cond_value is False:
                self.record(
                    phase="control_flow",
                    title=f"Branch skipped ({branch_label})",
                    description=f"{branch_label} condition is False — branch not taken.",
                    line=expr.start.line,
                )
                continue

            self.record(
                phase="control_flow",
                title=f"Condition indeterminate ({branch_label})",
                description=(
                    f"{branch_label} condition '{expr.getText()}' cannot be resolved "
                    f"statically — visiting block to collect any errors inside it."
                ),
                line=expr.start.line,
                detail="indeterminate: both branches analysed",
            )
            self.analyzer.visit(blocks[index])

        if has_else and not branch_taken:
            self.record(
                phase="control_flow",
                title="Else branch taken",
                description="No preceding condition was true — executing else branch.",
                line=blocks[-1].start.line,
            )
            self.analyzer.visit(blocks[-1])
        elif has_else and branch_taken:
            self.record(
                phase="control_flow",
                title="Else branch skipped",
                description="A preceding branch was taken — else block will not execute.",
                line=blocks[-1].start.line,
            )

    def handle_while_statement(self, ctx: EVALParser.WhileStatementContext) -> None:
        expr = ctx.expression()
        self.record(
            phase="control_flow",
            title="While statement",
            description=f"Evaluating initial while condition: '{expr.getText()}'.",
            line=ctx.start.line,
        )
        # ctx.expression() relationalExpr
        cond_result = self.analyzer.visit(expr)
        cond_type = self.variable_manager.get_type(cond_result)
        cond_value = VariableManager.unwrap_value(cond_result)

        if cond_type not in (EvalType.BOOL, EvalType.UNKNOWN, None):
            self.validator.push_error(expr.start, f"while condition must be bool, got {cond_type.name}")
            self.record(
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
            self.record(
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

        self.record(
            phase="control_flow",
            title="While loop entered",
            description=(
                f"while condition '{expr.getText()}' "
                f"evaluated to {cond_value!r} — beginning loop execution."
            ),
            line=ctx.start.line,
            detail=f"type={cond_type}, value={cond_value!r}",
        )

        cond_vars = ControlFlowAnalyzer.collect_condition_vars(expr)
        assigned_vars = ControlFlowAnalyzer.assigned_vars_in_block(ctx.block())
        loop_has_break = ControlFlowAnalyzer.has_break(ctx.block())

        frozen_cond_vars = {
            name for name in cond_vars
            if self.variable_manager.exists(name)
            and self.variable_manager.get_variable(name).constant
            and name not in assigned_vars
        }

        if cond_vars and frozen_cond_vars == cond_vars:
            frozen_list = ", ".join(sorted(frozen_cond_vars))
            msg = (
                f"loop condition variable(s) [{frozen_list}] are declared const "
                f"and cannot be modified — the condition '{expr.getText()}' is "
                f"permanently fixed and the loop will never terminate naturally"
            )
            
            self.error(
                phase="control_flow",
                title="Infinite loop (const condition)",
                token=expr.start,
                msg=msg,
                line=ctx.start.line,
                detail="error: const condition — loop cannot terminate",
                description=(
                    f"All variable(s) referenced in the while condition "
                    f"[{frozen_list}] are declared const and can never be "
                    f"reassigned. Because the condition '{expr.getText()}' is "
                    f"permanently fixed, the loop body will run forever — "
                    f"declare the variable(s) as mutable or restructure the loop."
                ),
            )
            return

        cond_vars_modified = bool(cond_vars & assigned_vars)
        cond_list = ", ".join(sorted(cond_vars)) if cond_vars else "none detected"

        if not cond_vars_modified and not loop_has_break:
            msg = (
                f"potential infinite loop: no variable(s) referenced in the "
                f"condition ({cond_list}) are ever assigned inside the loop body "
                f"and no break statement is present — the loop may never terminate"
            )
            self.validator.push_warnings(expr.start, msg)
            self.record(
                phase="control_flow",
                title="Potential infinite loop (no termination mechanism)",
                description=(
                    f"None of the variable(s) referenced in the while condition "
                    f"({cond_list}) are assigned inside the loop body, and no "
                    f"break statement is present. The loop may never terminate — "
                    f"add an assignment that can make the condition False, or add "
                    f"a break statement."
                ),
                line=ctx.start.line,
                detail=f"warning: cond_vars=[{cond_list}], no mutations, no break",
            )
        elif loop_has_break and not cond_vars_modified:
            break_guards = ControlFlowAnalyzer.collect_break_guards(
                ctx.block(),
                visit=self.analyzer.visit,
                unwrap=VariableManager.unwrap_value,
            )
            all_unreachable = bool(break_guards) and all(value is False for value in break_guards)

            if all_unreachable:
                msg = (
                    f"infinite loop: no variable in the condition ({cond_list}) "
                    f"is ever assigned inside the loop body, and every break "
                    f"statement is guarded by a condition that is statically "
                    f"false — all exit paths are unreachable"
                )
                self.error(
                    phase="control_flow",
                    title="Infinite loop (unreachable break — guarded by false condition)",
                    token=expr.start,
                    msg=msg,
                    line=ctx.start.line,
                    detail="error: all breaks unreachable, cond vars never modified",
                    description=(
                        f"The while condition '{expr.getText()}' can never become "
                        f"False because no variable in ({cond_list}) is ever "
                        f"assigned inside the loop body. A break statement exists "
                        f"but it is enclosed in an if-condition that is always "
                        f"false given the current values — the break is permanently "
                        f"unreachable and the loop will run forever."
                    ),
                )
                return

            msg = (
                f"possible infinite loop: no variable in the condition "
                f"({cond_list}) is ever assigned inside the loop body — "
                f"the only exit is a break statement; verify it is always reachable"
            )
            self.validator.push_warnings(expr.start, msg)
            self.record(
                phase="control_flow",
                title="Possible infinite loop (break-only exit, condition never changes)",
                description=(
                    f"No variable in the while condition ({cond_list}) is ever "
                    f"assigned inside the loop body. The loop can only exit via "
                    f"a break statement — verify the break is always reachable "
                    f"and the loop cannot spin indefinitely before reaching it."
                ),
                line=ctx.start.line,
                detail=f"warning: cond_vars=[{cond_list}], unmodified, break-only exit",
            )

        self.analyzer._loop_depth += 1
        iteration = 0
        try:
            while True:
                cond_result = self.analyzer.visit(expr)
                cond_value = VariableManager.unwrap_value(cond_result)

                if cond_value is not True:
                    self.record(
                        phase="control_flow",
                        title="While condition false — loop exited",
                        description=(
                            f"After {iteration} iteration(s), condition "
                            f"'{expr.getText()}' is now False — loop ends."
                        ),
                        line=ctx.start.line,
                    )
                    break

                iteration += 1
                self.record(
                    phase="control_flow",
                    title=f"While iteration {iteration}",
                    description=(
                        f"Condition '{expr.getText()}' = {cond_value!r} — "
                        f"executing loop body (iteration {iteration})."
                    ),
                    line=ctx.block().start.line,
                    detail=f"iteration={iteration}, condition={cond_value!r}",
                )

                if iteration > self._MAX_LOOP_ITERATIONS:
                    self.validator.push_warnings(
                        expr.start,
                        f"while loop halted after {self._MAX_LOOP_ITERATIONS} iterations "
                        f"— possible infinite loop",
                    )
                    self.record(
                        phase="control_flow",
                        title="While loop halted (max iterations reached)",
                        description=(
                            f"Loop exceeded the {self._MAX_LOOP_ITERATIONS}-iteration safety "
                            f"cap and was stopped to prevent an infinite loop."
                        ),
                        line=ctx.start.line,
                    )
                    break

                try:
                    self.analyzer.visit(ctx.block())
                except ContinueSignal:
                    self.record(
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
                    self.record(
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
            self.analyzer._loop_depth -= 1
            self.record(
                phase="control_flow",
                title="While loop complete",
                description=(
                    f"Loop finished after {iteration} iteration(s). "
                    f"Loop depth restored to {self.analyzer._loop_depth}."
                ),
                line=ctx.start.line,
                detail=f"iterations={iteration}, loop_depth={self.analyzer._loop_depth}",
            )

    def handle_try_statement(self, ctx: EVALParser.TryStatementContext) -> None:
        try_block = ctx.block(0)
        catch_block = ctx.block(1)
        ident_tok = ctx.IDENTIFIER().getSymbol()
        catch_name = ident_tok.text
        col, line = self.validator.tok_col_line(ident_tok)

        self.record(
            phase="control_flow",
            title="Try/catch statement",
            description=f"Processing try block with catch parameter '{catch_name}' on line {line}.",
            line=ctx.start.line,
        )

        errors_before_kw = len(self.analyzer.errors)
        is_reserved = self.validator.check_reserved_keyword(catch_name, ident_tok)
        if is_reserved:
            while len(self.analyzer.errors) > errors_before_kw:
                self.analyzer.errors.pop()
            self.validator.push_warnings(
                ident_tok,
                f"'{catch_name}' is a reserved identifier; "
                f"using it as a catch parameter name is discouraged",
            )
            self.record(
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

        self.record(
            phase="control_flow",
            title="Entering try block",
            description="Visiting try block — any runtime exceptions will be intercepted.",
            line=try_block.start.line,
        )

        errors_before_try = len(self.analyzer.errors)
        caught_exception: Exception | None = None
        caught_line = try_block.start.line

        try:
            self.analyzer.visit(try_block)
        except (BreakSignal, ContinueSignal):
            raise
        except self.CATCHABLE_EXCEPTIONS as exc:
            caught_exception = exc
            caught_line = try_block.start.line

        errors_after_try = len(self.analyzer.errors)

        if caught_exception is not None:
            self.record(
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
            self.record(
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
            self.record(
                phase="control_flow",
                title="Try block completed without errors",
                description="No exceptions or semantic errors were raised in the try block.",
                line=try_block.start.line,
            )

        has_error = caught_exception is not None or errors_after_try > errors_before_try
        if not has_error:
            self.record(
                phase="control_flow",
                title="Catch block skipped",
                description="No errors in the try block — catch block will not execute.",
                line=catch_block.start.line,
            )
            return

        parts: list[str] = []
        if caught_exception is not None:
            parts.append(f" {type(caught_exception).__name__}: ")
        for err in self.analyzer.errors[errors_before_try:]:
            parts.append(f"line {err.line_number}: {err.message}")
        error_details = " ".join(parts) if parts else "error occurred"

        self.variable_manager.enter_scope("catch")
        try:
            catch_var = Variable(
                name=catch_name,
                type=EvalType.STRING,
                value=error_details,
                position=Position(line=line, column=col),
            )
            self.variable_manager.define(catch_var)

            self.record(
                phase="control_flow",
                title=f"Catch variable defined: {catch_name}",
                description=f"'{catch_name}' defined as STRING in catch scope with error details.",
                line=line,
                changed=catch_name,
                detail=f"type=STRING, value={error_details!r}",
            )
            self.record(
                phase="control_flow",
                title="Entering catch block",
                description=f"Visiting catch block — '{catch_name}' is available as a STRING.",
                line=catch_block.start.line,
            )

            statements = list(catch_block.statement())
            for index, stmt in enumerate(statements):
                self.record(
                    phase="control_flow",
                    title=f"Catch statement {index + 1}/{len(statements)}",
                    description=f"Visiting catch statement {index + 1}: '{stmt.getText()}'.",
                    line=stmt.start.line,
                )
                try:
                    self.analyzer.visit(stmt)
                except (BreakSignal, ContinueSignal) as signal:
                    remaining = statements[index + 1:]
                    if remaining:
                        keyword = "break" if isinstance(signal, BreakSignal) else "continue"
                        self.validator.push_warnings(
                            remaining[0].start,
                            f"{len(remaining)} unreachable statement(s) after "
                            f"'{keyword}' will never execute",
                        )
                        self.record(
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
            self.record(
                phase="control_flow",
                title="Exiting catch block",
                description=f"Catch block complete — releasing '{catch_name}' from scope.",
                line=catch_block.stop.line if catch_block.stop else line,
            )
            self.variable_manager.exit_scope()

    def evaluate_logical_or(self, ctx: EVALParser.LogicalOrExprContext) -> bool | None:
        self.record(
            phase="expression",
            title="Logical OR (||)",
            description=f"Evaluating left operand of '||': '{ctx.expression(0).getText()}'.",
            line=ctx.start.line,
        )
        left_result = self.analyzer.visit(ctx.expression(0))
        lt = self.variable_manager.get_type(left_result)
        left_val = VariableManager.unwrap_value(left_result)

        if left_val is True:
            self.validator.check_logical_operands("||", lt, lt, ctx.start)
            self.record(
                phase="expression",
                title="Logical OR short-circuit (left=True)",
                description="Left operand is True — right not evaluated (short-circuit). Result: True.",
                line=ctx.start.line,
                detail="short-circuit: True || any → True",
            )
            return True

        self.record(
            phase="expression",
            title="Logical OR — evaluating right operand",
            description=f"Left is {left_val!r} — evaluating right: '{ctx.expression(1).getText()}'.",
            line=ctx.start.line,
        )
        right_result = self.analyzer.visit(ctx.expression(1))
        rt = self.variable_manager.get_type(right_result)
        right_val = VariableManager.unwrap_value(right_result)

        self.validator.check_logical_operands("||", lt, rt, ctx.start)

        if isinstance(left_val, bool) and isinstance(right_val, bool):
            result = left_val or right_val
            self.record(
                phase="expression",
                title="Logical OR result",
                description=f"{left_val!r} || {right_val!r} = {result!r}.",
                line=ctx.start.line,
                detail=f"left={left_val!r}, right={right_val!r}, result={result!r}",
            )
            return result

        self.record(
            phase="expression",
            title="Logical OR result (indeterminate)",
            description="One or both operands are not statically known — result is indeterminate.",
            line=ctx.start.line,
        )
        return None

    def evaluate_logical_and(self, ctx: EVALParser.LogicalAndExprContext) -> bool | None:
        self.record(
            phase="expression",
            title="Logical AND (&&)",
            description=f"Evaluating left operand of '&&': '{ctx.expression(0).getText()}'.",
            line=ctx.start.line,
        )
        left_result = self.analyzer.visit(ctx.expression(0))
        lt = self.variable_manager.get_type(left_result)
        left_val = VariableManager.unwrap_value(left_result)

        if left_val is False:
            self.validator.check_logical_operands("&&", lt, lt, ctx.start)
            self.record(
                phase="expression",
                title="Logical AND short-circuit (left=False)",
                description="Left operand is False — right not evaluated (short-circuit). Result: False.",
                line=ctx.start.line,
                detail="short-circuit: False && any → False",
            )
            return False

        self.record(
            phase="expression",
            title="Logical AND — evaluating right operand",
            description=f"Left is {left_val!r} — evaluating right: '{ctx.expression(1).getText()}'.",
            line=ctx.start.line,
        )
        right_result = self.analyzer.visit(ctx.expression(1))
        rt = self.variable_manager.get_type(right_result)
        right_val = VariableManager.unwrap_value(right_result)

        self.validator.check_logical_operands("&&", lt, rt, ctx.start)

        if isinstance(left_val, bool) and isinstance(right_val, bool):
            result = left_val and right_val
            self.record(
                phase="expression",
                title="Logical AND result",
                description=f"{left_val!r} && {right_val!r} = {result!r}.",
                line=ctx.start.line,
                detail=f"left={left_val!r}, right={right_val!r}, result={result!r}",
            )
            return result

        self.record(
            phase="expression",
            title="Logical AND result (indeterminate)",
            description="One or both operands are not statically known — result is indeterminate.",
            line=ctx.start.line,
        )
        return None

    def evaluate_equality(self, ctx: EVALParser.EqualityExprContext) -> Literal[EvalType.BOOL] | bool:
        op = ctx.op.text
        self.record(
            phase="expression",
            title=f"Equality expression ({op})",
            description=f"Evaluating '{ctx.expression(0).getText()}' {op} '{ctx.expression(1).getText()}'.",
            line=ctx.start.line,
        )

        left_visited = self.analyzer.visit(ctx.expression(0))
        right_visited = self.analyzer.visit(ctx.expression(1))
        lt = self.variable_manager.get_type(left_visited)
        rt = self.variable_manager.get_type(right_visited)

        self.validator.check_float_equality(op, lt, rt, ctx.start)
        left_val, right_val = self.run_comparison(ctx, op, "Equality")
        result = Evaluator.evaluate_relational(left_val, op, right_val)
        self.record(
            phase="expression",
            title=f"Equality result ({op})",
            description=f"{left_val!r} {op} {right_val!r} → {result!r} (left: {lt.name}, right: {rt.name}).",
            line=ctx.start.line,
            detail=f"left={left_val!r} ({lt.name}), right={right_val!r} ({rt.name}), result={result!r}",
        )
        return result

    def evaluate_relational(self, ctx: EVALParser.RelationalExprContext) -> bool:
        op = ctx.op.text
        self.record(
            phase="expression",
            title=f"Relational expression ({op})",
            description=f"Evaluating '{ctx.expression(0).getText()}' {op} '{ctx.expression(1).getText()}'.",
            line=ctx.start.line,
        )
        left_val, right_val = self.run_comparison(ctx, op, "Relational")
        result = Evaluator.evaluate_relational(left_val, op, right_val)
        self.record(
            phase="expression",
            title=f"Relational result ({op})",
            description=f"{left_val!r} {op} {right_val!r} → {result!r}.",
            line=ctx.start.line,
            detail=f"left={left_val!r}, right={right_val!r}, result={result!r}",
        )
        return result

    def evaluate_additive(self, ctx: EVALParser.AdditiveExprContext) -> Any:
        return self._evaluate_numeric_binary_expr(ctx, "Additive")

    def evaluate_multiplicative(self, ctx: EVALParser.MultiplicativeExprContext) -> Any:
        return self._evaluate_numeric_binary_expr(ctx, "Multiplicative")

    def _evaluate_numeric_binary_expr(self, ctx: Any, label: str) -> Any:
        op = ctx.op.text
        lhs = self.analyzer.visit(ctx.expression(0))
        rhs = self.analyzer.visit(ctx.expression(1))
        lt = self.variable_manager.get_type(lhs)
        rt = self.variable_manager.get_type(rhs)

        self.record(
            phase="expression",
            title=f"{label} expression ({op})",
            description=(
                f"'{ctx.expression(0).getText()}' {op} '{ctx.expression(1).getText()}' — "
                f"left: {VariableManager.unwrap_value(lhs)!r} ({lt.name}), "
                f"right: {VariableManager.unwrap_value(rhs)!r} ({rt.name})."
            ),
            line=ctx.start.line,
            detail=f"op={op}, lt={lt.name}, rt={rt.name}",
        )

        result_type = self.validator.numeric_result(op, lt, rt, ctx.start)
        if label == "Additive" and result_type in TypeHandler.EMPTY:
            msg = f"operator '{op}' cannot be applied to '{lt.name}' and '{rt.name}'"
            self.error(
                phase="expression",
                title=f"Additive type error ({op})",
                token=ctx.start,
                msg=msg,
                line=ctx.start.line,
                detail=f"error: incompatible types {lt.name} {op} {rt.name}",
                description=f"Operator '{op}' cannot be applied to '{lt.name}' and '{rt.name}'.",
            )
            raise ArithmeticError(
                f"additive operator '{op}' cannot be applied to '{lt.name}' and '{rt.name}'"
            )

        if label == "Multiplicative" and result_type == EvalType.UNKNOWN:
            msg = f"Operator '{op}' cannot be applied to '{lt.name}' and '{rt.name}'."
            self.error(
                phase="expression",
                title=f"Multiplicative type error ({op})",
                token=ctx.start,
                msg=msg,
                line=ctx.start.line,
            )
            raise ArithmeticError(
                f"multiplicative operator '{op}' cannot be applied to '{lt.name}' and '{rt.name}'"
            )

        if label == "Multiplicative" and op == "%" and result_type not in TypeHandler.EMPTY:
            self.validator.check_modulo_float(lt, rt, ctx.start)

        try:
            return self.eval_postfix(ctx, label, op, result_type)
        except ZeroDivisionError as exc:
            if label != "Multiplicative":
                raise
            op_name = "division" if op == "/" else "modulo"
            self.error(
                phase="expression",
                title=f"Division by zero ({op})",
                token=ctx.start,
                msg=f"{op_name.capitalize()} by zero.",
                line=ctx.start.line,
            )
            raise ArithmeticError(f"{op_name} by zero") from exc

    def evaluate_unary_minus(self, ctx: EVALParser.UnaryMinusExprContext) -> Any:
        self.record(
            phase="expression",
            title="Unary minus (-)",
            description=f"Evaluating unary minus on: '{ctx.expression().getText()}'.",
            line=ctx.start.line,
        )
        inner = self.analyzer.visit(ctx.expression())
        inner_type = self.variable_manager.get_type(inner)

        if inner_type not in TypeHandler.NUMERIC:
            self.error(
                phase="expression",
                title="Unary minus type error",
                token=ctx.start,
                msg=f"unary '-' requires a numeric operand, got {inner_type.name}",
                line=ctx.start.line,
                description=f"Cannot apply unary '-' to type {inner_type.name} — expected a numeric type.",
                detail=f"error: expected NUMERIC, got {inner_type.name}",
            )
            raise ArithmeticError(f"unary '-' requires a numeric operand, got '{inner_type.name}'")

        expr_string = ExpressionStringBuilder.build(ctx, self.variable_manager, self.analyzer.visit)
        if expr_string is None:
            return None

        result = Postfix.get_result(expr_string)
        self.record(
            phase="expression",
            title="Unary minus result",
            description=f"Unary minus on '{ctx.expression().getText()}' → {result!r}.",
            line=ctx.start.line,
            detail=f"operand_type={inner_type.name}, result={result!r}",
        )
        return result

    def evaluate_unary_not(self, ctx: EVALParser.UnaryNotExprContext) -> bool | None:
        self.record(
            phase="expression",
            title="Unary NOT (!)",
            description=f"Evaluating logical NOT on: '{ctx.expression().getText()}'.",
            line=ctx.start.line,
        )
        inner = self.analyzer.visit(ctx.expression())
        inner_type = self.variable_manager.get_type(inner)

        if inner_type != EvalType.BOOL:
            self.error(
                phase="expression",
                title="Unary NOT type error",
                token=ctx.start,
                msg=f"'!' requires a bool operand, got '{inner_type.name}'",
                line=ctx.start.line,
                description=f"'!' applied to non-bool type {inner_type.name} — expected BOOL.",
                detail=f"error: expected BOOL, got {inner_type.name}",
            )
            raise TypeError(f"'!' requires a bool operand, got '{inner_type.name}'")

        val = VariableManager.unwrap_value(inner)
        if isinstance(val, bool):
            result = not val
            self.record(
                phase="expression",
                title="Unary NOT result",
                description=f"!{val!r} → {result!r}.",
                line=ctx.start.line,
                detail=f"operand={val!r}, result={result!r}",
            )
            return result

        self.record(
            phase="expression",
            title="Unary NOT result (indeterminate)",
            description="Operand value not statically known — result is indeterminate.",
            line=ctx.start.line,
        )
        return None

    def evaluate_parenthesized(self, ctx: EVALParser.ParenExprContext) -> Any:
        result = self.analyzer.visit(ctx.expression())
        raw = VariableManager.unwrap_value(result)
        self.record(
            phase="expression",
            title="Parenthesised expression result",
            description=f"'({ctx.expression().getText()})' → {raw!r}.",
            line=ctx.start.line,
            detail=f"result={raw!r}",
        )
        return result

    def evaluate_identifier(self, ctx: EVALParser.IdentExprContext) -> Variable | None:
        tok = ctx.IDENTIFIER().getSymbol()
        name = tok.text
        self.record(
            phase="expression",
            title=f"Identifier lookup: {name}",
            description=f"Resolving identifier '{name}' in scope.",
            line=tok.line,
        )
        try:
            var = self.variable_manager.get_variable(name)
            self.record(
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
        except EVALNameException as exc:
            self.error(
                phase="expression",
                title=f"Undeclared identifier: {name}",
                token=ctx.start,
                msg=str(exc),
                line=tok.line,
                description=f"'{name}' is not declared in any accessible scope.",
                detail=f"error: {exc}",
            )
            return None

    def evaluate_int_literal(self, ctx) -> int:
        value = int(ctx.INTEGER().getText())
        self.record(
            phase="expression",
            title=f"Integer literal: {value}",
            description=f"Integer literal {value} evaluated.",
            line=ctx.start.line,
            detail=f"value={value}, type=INT",
        )
        return value

    def evaluate_real_literal(self, ctx) -> float:
        value = float(ctx.REAL().getText())
        self.record(
            phase="expression",
            title=f"Float literal: {value}",
            description=f"Float literal {value} evaluated.",
            line=ctx.start.line,
            detail=f"value={value}, type=FLOAT",
        )
        return value

    def evaluate_string_literal(self, ctx) -> str:
        value = ctx.STRING().getText()
        self.record(
            phase="expression",
            title="String literal",
            description=f"String literal {value!r} evaluated.",
            line=ctx.start.line,
            detail=f"value={value!r}, type=STRING",
        )
        return value

    def evaluate_true_literal(self, ctx) -> bool:
        self.record(
            phase="expression",
            title="Boolean literal: true",
            description="Literal 'true' evaluated.",
            line=ctx.start.line,
            detail="value=True, type=BOOL",
        )
        return True

    def evaluate_false_literal(self, ctx) -> bool:
        self.record(
            phase="expression",
            title="Boolean literal: false",
            description="Literal 'false' evaluated.",
            line=ctx.start.line,
            detail="value=False, type=BOOL",
        )
        return False

    def evaluate_null_literal(self, ctx) -> None:
        self.record(
            phase="expression",
            title="Null literal",
            description="Literal 'null' evaluated.",
            line=ctx.start.line,
            detail="value=None, type=NULL",
        )
        return None

    def evaluate_cast_call(self, ctx) -> Any:
        expression = ctx.expression()
        target_text = ctx.type_().getText()
        target_type = TypeHandler.get_eval_type(target_text)

        self.record(
            phase="expression",
            title=f"cast() — target: {target_text}",
            description=f"Evaluating cast({expression.getText()}, {target_text}).",
            line=ctx.start.line,
        )

        visited_val = self.analyzer.visit(expression)
        if target_type in self._INVALID_CAST_TARGETS:
            msg = f"invalid cast target type '{target_text}': cannot cast to '{target_type.value}'"
            self.error(
                phase="expression",
                title="cast() invalid target",
                token=ctx.type_().start,
                msg=msg,
                line=ctx.start.line,
            )
            raise CastException(msg)

        if visited_val is None:
            msg = "cast argument could not be resolved"
            self.error(
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
            self.error(
                phase="expression",
                title="cast() unsupported argument type",
                token=expression.start,
                msg=msg,
                line=ctx.start.line,
            )
            raise CastException(msg)

        if val is None:
            msg = "cast argument evaluates to null and cannot be cast"
            self.error(
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
            self.error(
                phase="expression",
                title="cast() conversion failed",
                token=expression.start,
                msg=msg,
                line=ctx.start.line,
            )
            raise CastException(msg)

        self.record(
            phase="expression",
            title="cast() result",
            description=f"cast({val!r}, {target_text}) → {result!r}.",
            line=ctx.start.line,
            detail=f"input={val!r}, target={target_text}, result={result!r}",
        )
        return result

    def evaluate_pow_call(self, ctx: EVALParser.PowCallContext) -> Any:
        left_expr = ctx.expression(0)
        right_expr = ctx.expression(1)
        self.record(
            phase="expression",
            title="pow()",
            description=f"Evaluating pow({left_expr.getText()}, {right_expr.getText()}).",
            line=ctx.start.line,
        )

        try:
            result = self.evaluate_binary_numeric_call(ctx, pow, "pow")
            if result is None:
                raise PowException("pow: result could not be resolved")
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            msg = (
                f"pow() failed for operands "
                f"'{self.analyzer.visit(left_expr)!r}' and '{self.analyzer.visit(right_expr)!r}': {exc}"
            )
            self.error(
                phase="expression",
                title="pow() computation failed",
                token=left_expr.start,
                msg=msg,
                line=ctx.start.line,
            )
            raise PowException(msg) from exc

        return result

    def evaluate_sqrt_call(self, ctx: EVALParser.SqrtCallContext) -> Any:
        self.record(
            phase="expression",
            title="sqrt()",
            description=f"Evaluating sqrt({ctx.expression().getText()}).",
            line=ctx.start.line,
        )
        return self.evaluate_unary_numeric_call(ctx, sqrt, "sqrt")

    def evaluate_min_call(self, ctx: EVALParser.MinCallContext) -> Any:
        self.record(
            phase="expression",
            title="min()",
            description=f"Evaluating min({ctx.expression(0).getText()}, {ctx.expression(1).getText()}).",
            line=ctx.start.line,
        )
        return self.evaluate_binary_numeric_call(ctx, min, "min")

    def evaluate_max_call(self, ctx: EVALParser.MaxCallContext) -> Any:
        self.record(
            phase="expression",
            title="max()",
            description=f"Evaluating max({ctx.expression(0).getText()}, {ctx.expression(1).getText()}).",
            line=ctx.start.line,
        )
        return self.evaluate_binary_numeric_call(ctx, max, "max")

    def evaluate_round_call(self, ctx: EVALParser.RoundCallContext) -> Any:
        self.record(
            phase="expression",
            title="round()",
            description=f"Evaluating round({ctx.expression().getText()}).",
            line=ctx.start.line,
        )
        return self.evaluate_unary_numeric_call(ctx, round, "round")

    def evaluate_abs_call(self, ctx: EVALParser.AbsCallContext) -> Any:
        self.record(
            phase="expression",
            title="abs()",
            description=f"Evaluating abs({ctx.expression().getText()}).",
            line=ctx.start.line,
        )
        return self.evaluate_unary_numeric_call(ctx, abs, "abs")

    def evaluate_macro_value(self, ctx: EVALParser.MacroValueContext) -> Any:
        key = ctx.getText()
        macro_info = MacroValue.get_macro_info(key)
        if macro_info:
            self.record(
                phase="expression",
                title=macro_info.title,
                description=macro_info.description,
                line=ctx.start.line,
                detail=f"value={macro_info.value}",
            )
            return macro_info.value

        self.record(
            phase="expression",
            title="Macro: unknown",
            description="Encountered an unrecognised macro — returning None.",
            line=ctx.start.line,
        )
        return None

    def run_comparison(self, ctx: Any, op: str, label: str) -> tuple[Any, Any]:
        handler = ComparisonHandler(
            left_expr=ctx.expression(0),
            right_expr=ctx.expression(1),
            visitor=self.analyzer,
        )
        try:
            return handler.check()
        except ValueError as exc:
            self.validator.push_error(ctx.op, str(exc))
            self.record(
                phase="expression",
                title=f"{label} check failed ({op})",
                description=f"Comparison handler raised an error: {exc}",
                line=ctx.start.line,
                detail=f"error: {exc}",
            )
            raise

    def eval_postfix(self, ctx: Any, label: str, op: str, result_type) -> Any:
        expr_string = ExpressionStringBuilder.build(ctx, self.variable_manager, self.analyzer.visit)
        if expr_string is None:
            return None
        result = Postfix.get_result(expr_string)
        self.record(
            phase="expression",
            title=f"{label} result ({op})",
            description=f"Expression '{expr_string}' evaluated to {result!r} (type: {result_type.name}).",
            line=ctx.start.line,
            detail=f"expr={expr_string!r}, result={result!r}",
        )
        return result

    def evaluate_unary_numeric_call(self, ctx, fn, fn_name: str) -> Any:
        expression = ctx.expression()
        value = self.analyzer.visit(expression)
        value_type = self.variable_manager.get_type(value)
        checked_type = self.validator.require_numeric(value_type, expression, f"{fn_name}() argument")

        if checked_type == EvalType.UNKNOWN:
            self.record(
                phase="expression",
                title=f"{fn_name}() type error",
                description=f"{fn_name}() requires a numeric argument, got {value_type.name}.",
                line=ctx.start.line,
                detail=f"error: expected NUMERIC, got {value_type.name}",
            )
            return None

        raw_value = VariableManager.unwrap_value(value)
        result = fn(raw_value)
        self.record(
            phase="expression",
            title=f"{fn_name}() result",
            description=f"{fn_name}({raw_value!r}) → {result!r}.",
            line=ctx.start.line,
            detail=f"input={raw_value!r}, result={result!r}",
        )
        return result

    def evaluate_binary_numeric_call(self, ctx, fn, fn_name: str) -> Any:
        first_val = self.analyzer.visit(ctx.expression(0))
        second_val = self.analyzer.visit(ctx.expression(1))
        first_type = self.variable_manager.get_type(first_val)
        second_type = self.variable_manager.get_type(second_val)

        checked_type1 = self.validator.require_numeric(first_type, ctx.expression(0), f"{fn_name}() first argument")
        checked_type2 = self.validator.require_numeric(second_type, ctx.expression(1), f"{fn_name}() second argument")

        if checked_type1 == EvalType.UNKNOWN or checked_type2 == EvalType.UNKNOWN:
            self.record(
                phase="expression",
                title=f"{fn_name}() type error",
                description=f"{fn_name}() requires numeric arguments — got {first_type.name} and {second_type.name}.",
                line=ctx.start.line,
                detail=f"error: types={first_type.name}, {second_type.name}",
            )
            return None

        first_value = VariableManager.unwrap_value(first_val)
        second_value = VariableManager.unwrap_value(second_val)
        result = fn(first_value, second_value)
        self.record(
            phase="expression",
            title=f"{fn_name}() result",
            description=f"{fn_name}({first_value!r}, {second_value!r}) → {result!r}.",
            line=ctx.start.line,
            detail=f"a={first_value!r}, b={second_value!r}, result={result!r}",
        )
        return result
