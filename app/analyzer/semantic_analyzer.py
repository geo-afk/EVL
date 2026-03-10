from app.eval.variable_evaluator import Evaluator
from app.models.CustomError import ErrorResponse, WarningResponse
from app.eval.semantic_validation import SemanticValidation
from app.models.custom_exceptions import EVALNameException
from app.eval.variable_manager import VariableManager
from app.models.Types import EvalType, TypeHandler
from app.models.Variable import Variable, Position
from generated.EVALParser import EVALParser
from app.eval.postfix import Postfix
from datetime import datetime
from typing import List, Any
from math import pi, sqrt

try:
    from generated.EVALParserVisitor import EVALParserVisitor as BaseVisitor
except ImportError:
    from antlr4 import ParseTreeVisitor as BaseVisitor


class SemanticAnalyzer(BaseVisitor):
    """
    Walk the parse tree and perform semantic checks.

    After `visit(tree)`:
      • self.errors        – list of error strings
      • self.warnings      – list of warning strings
    """

    def __init__(self):
        self._loop_depth = 0

        self.errors:   List[ErrorResponse] = []
        self.warnings: List[WarningResponse] = []

        self.validator = SemanticValidation()

        self.variable_manager = VariableManager(
            validator=self.validator
        )


        self.postfix = Postfix()


    def visitProgram(self, ctx) -> None:
        return self.visitChildren(ctx)


    def visitBlock(self, ctx) -> None:
        self.variable_manager.enter_scope("block")

        for stmt in ctx.statement():
            self.visit(stmt)

        self.variable_manager.exit_scope()


    def visitVariableDeclaration(self, ctx: EVALParser.VariableDeclarationContext) -> None:
        type_text  = ctx.type_().getText()
        decl_type  = TypeHandler.get_eval_type(type_text)
        ident_tok  = ctx.IDENTIFIER().getSymbol()
        name       = ident_tok.text

        try:
            variable = self.variable_manager.get_variable(name)

            if variable:
                self.validator.push_error(
                    ident_tok,
                    f"variable {name} is already defines"
                )

        except EVALNameException:

            var_value = self.visit(ctx.expression())

            column, line = self.validator.tok_col_line(ident_tok)
            variable = Variable(
                name=name,
                type=decl_type,
                value=var_value,
                position= Position(
                    line=line,
                    column=column
                )
            )

            self.variable_manager.define(variable)



    def visitConstDeclaration(self, ctx: EVALParser.ConstDeclarationContext) -> None:

        variable_declaration = ctx.variableDeclaration()
        self.visit(variable_declaration)

        name = variable_declaration.IDENTIFIER().getText()

        try:
            variable = self.variable_manager.get_variable(name)
            if variable:
                variable.constant = True
                self.variable_manager.define(variable)
        except EVALNameException as e :
            self.validator.push_error(
                variable_declaration,
                f"{e} in this scope"
            )
            return




    def visitAssignment(self, ctx: EVALParser.AssignmentContext) -> None:
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name      = ident_tok.text

        try:
            variable = self.variable_manager.get_variable(name)

            if variable is None:
                self.validator.push_error(
                    ident_tok,
                    f"assignment to undeclared variable '{name}'"
                )

                return

            if variable.constant:
                self.validator.push_error(
                    ident_tok,
                    f"cannot reassign const variable '{name}'"
                )
            value = self.visit(ctx.expression())

            variable.value = value
            self.variable_manager.define(variable)

        except EVALNameException as e :
            self.validator.push_error(
                ident_tok,
                f"{e} in this scope"
            )
            return





    def visitIncrementDecrement(self, ctx: EVALParser.IncrementDecrementContext) -> None:
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name      = ident_tok.text


        variable = self.variable_manager.get_variable(name)
        if variable is None:
            self.validator.push_error(
                ident_tok,
                f"use of undeclared variable '{name}'"
            )

            return
        if variable.constant:
            op = ctx.INCREMENT() and "++" or "--"
            self.validator.push_error(
                ident_tok,
                f"cannot apply '{op}' to const variable '{name}'"
            )

        if variable.type not in TypeHandler.NUMERIC:
            op = "++" if ctx.INCREMENT() else "--"
            self.validator.push_error(
                ident_tok,
                f"'{op}' requires a numeric variable; '{name}' is {variable.type}",

            )



    def visitPrintStatement(self, ctx: EVALParser.PrintStatementContext) -> None:
        for arg in ctx.printArg():
            self.visit(arg)

    def visitPrintArg(self, ctx: EVALParser.PrintArgContext) -> None:
        self.visit(ctx.expression())


    def visitIfStatement(self, ctx: EVALParser.IfStatementContext) -> None:
        for expr in ctx.expression():
            cond_type = self.visit(expr)

            if cond_type not in (EvalType.BOOL, EvalType.UNKNOWN, None):

                self.validator.push_error(
                    expr.start,
                    f"condition is of type {cond_type.name}, not bool — may behave unexpectedly",
                )

        for blk in ctx.block():
            self.visit(blk)


    def visitWhileStatement(self, ctx: EVALParser.WhileStatementContext) -> None:
        cond_type = self.visit(ctx.expression())
        if cond_type not in (EvalType.BOOL, EvalType.UNKNOWN, None):

            self.validator.push_warnings(
                ctx.expression().start,
                f"while condition is {cond_type.name}, not bool",
            )

        self._loop_depth += 1
        self.visit(ctx.block())
        self._loop_depth -= 1


    def visitTryStatement(self, ctx: EVALParser.TryStatementContext) -> None:
        blocks = ctx.block()
        self.visit(blocks[0])   # try block

        # Introduce catch variable into catch scope

        self.variable_manager.enter_scope("catch")

        ident_tok = ctx.IDENTIFIER().getSymbol()
        # catch_sym = Symbol(
        #     name=ident_tok.text,
        #     eval_type=EvalType.UNKNOWN,  # exception object — type unknown at static time
        #     line=self._tok_line(ident_tok),
        #     column=self._tok_col(ident_tok),
        # )
        # print("Catch: ", catch_sym)
        # self._current_scope.define(catch_sym)
        # Visit the catch block body statements directly so we don't double-push scope
        catch_block = blocks[1]
        for stmt in catch_block.statement():
            self.visit(stmt)

        self.variable_manager.exit_scope()

    # ── breakStatement ─────────────────────────────────────────────────────

    def visitBreakStatement(self, ctx: EVALParser.BreakStatementContext) -> None:
        if self._loop_depth == 0:

            self.validator.push_error(
                ctx.start,
                "'break' used outside of a loop",
            )



    def visitContinueStatement(self, ctx: EVALParser.ContinueStatementContext) -> None:
        if self._loop_depth == 0:

            self.validator.push_error(
                ctx.start,
                "'continue' used outside of a loop",
            )



    def visitLogicalOrExpr(self, ctx: EVALParser.LogicalOrExprContext) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))

        self.validator.check_logical_operands("||", lt, rt, ctx.start)
        return EvalType.BOOL

    def visitLogicalAndExpr(self, ctx: EVALParser.LogicalAndExprContext) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        self.validator.check_logical_operands("&&", lt, rt, ctx.start)
        return EvalType.BOOL

    def visitEqualityExpr(self, ctx: EVALParser.EqualityExprContext) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
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

    def visitRelationalExpr(self, ctx: EVALParser.RelationalExprContext) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        for t in (lt, rt):
            if t not in TypeHandler.EMPTY and t not in TypeHandler.NUMERIC:

                self.validator.push_error(
                    ctx.start,
                    f"relational operator requires numeric operands, got {t.name}",
                )

                return EvalType.UNKNOWN
        return EvalType.BOOL

    def visitAdditiveExpr(self, ctx: EVALParser.AdditiveExprContext) -> str:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        op = ctx.op.text

        return f"{lt} {op} {rt}"

    def visitMultiplicativeExpr(self, ctx: EVALParser.MultiplicativeExprContext) -> str:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        op = ctx.op.text

        return f"{lt} {op} {rt}"


    def visitUnaryMinusExpr(self, ctx: EVALParser.UnaryMinusExprContext) -> EvalType:
        t = self.visit(ctx.expression())
        if t not in TypeHandler.EMPTY and t not in TypeHandler.NUMERIC:

            self.validator.push_error(
                ctx.start,
                f"unary '-' requires a numeric operand, got {t.name}"
            )

        return t if t in TypeHandler.NUMERIC else EvalType.UNKNOWN

    # TODO
    def visitUnaryNotExpr(self, ctx: EVALParser.UnaryNotExprContext) -> EvalType:
        t = self.visit(ctx.expression())

        if t not in (EvalType.BOOL, EvalType.UNKNOWN, None):

            self.validator.push_warnings(
                ctx.start,
                f"'!' applied to {t.name} — expected bool",
            )

        # TODO
        return EvalType.BOOL

    def visitParenExpr(self, ctx: EVALParser.ParenExprContext) -> EvalType:
        return self.visit(ctx.expression())

    def visitBuiltinExpr(self, ctx: EVALParser.BuiltinExprContext) -> EvalType:
        return self.visit(ctx.builtinFunc())


    def visitIdentExpr(self, ctx: EVALParser.IdentExprContext) -> Variable | None:
        tok  = ctx.IDENTIFIER().getSymbol()
        name = tok.text


        try:
            variable = self.variable_manager.get_variable(name)
            return variable
        except Exception as e:
            self.validator.push_error(
                ctx.start,
                str(e)
            )
            return None


    def visitIntLiteral(self, ctx) -> int:

        int_literal = ctx.INTEGER().getText()
        return int(int_literal)

    def visitRealLiteral(self, ctx) -> float:
        float_literal = ctx.REAL().getText()
        return float(float_literal)

    def visitStringLiteral(self, ctx) -> str:
        return ctx.STRING().getText()

    def visitTrueLiteral(self, ctx) -> bool:
        bool_literal = ctx.TrueLiteral().getText()
        return bool(bool_literal)

    def visitFalseLiteral(self, ctx) -> bool:
        bool_literal = ctx.TrueLiteral().getText()
        return bool(bool_literal)

    def visitNullLiteral(self, _ctx) -> None:
        return None



    def visitMacroExpr(self, ctx: EVALParser.MacroExprContext):
        return self.visit(ctx.macroValue())



    # ── Built-in functions ─────────────────────────────────────────────────

    def visitBuiltinFunc(self, ctx: EVALParser.BuiltinFuncContext) -> EvalType:
        return self.visitChildren(ctx) or EvalType.UNKNOWN

    def visitCastCall(self, ctx) -> int | float | None:
        expression = ctx.expression()
        value: Variable = self.visit(expression)
        target_text = ctx.type_().getText()


        if not isinstance(value, Variable):
            self.validator.push_error(
                expression,
                f"cast argument should be a variable, got {target_text}"
            )
            return None

        if isinstance(value.value, Variable):
            variable = self.variable_manager.get_variable(value.value.name)
            variable.type = TypeHandler.get_eval_type(target_text)
            self.variable_manager.define(variable)
            return Evaluator.evaluate(variable.value)

        if value.value is None or value.value == 0:
            self.validator.push_warnings(
                expression,
                f"cast argument should be a number, got {target_text}"
            )

        value.type = TypeHandler.get_eval_type(target_text)
        self.variable_manager.define(value)
        return Evaluator.evaluate(value.value)



    def visitPowCall(self, ctx: EVALParser.PowCallContext) -> float | int:

        first_expression = ctx.expression(0)
        first_val = self.visit(first_expression)

        second_expression = ctx.expression(1)
        second_val = self.visit(second_expression)


        if first_val is None or second_val is None:
            self.validator.push_warnings(
                first_expression,
                f"first argument should be a number, got {first_val}"
            )
            self.validator.push_warnings(
                second_expression,
                f"second argument should be a number, got {second_val}"
            )

        if isinstance(first_val, Variable) and isinstance(second_val, Variable):
            ...


        first = 0
        second = 0

        return pow(first, second)


    def visitSqrtCall(self, ctx: EVALParser.SqrtCallContext) -> float | None:

        expression = ctx.expression()
        value = self.visit(expression)

        if value is None :
            self.validator.push_warnings(
                expression,
                f"Invalid Argument -> {value}"
            )


        if isinstance(value, Variable):
            variable = self.variable_manager.get_variable(value.value.name)
            return sqrt(variable.value)


        if type(value) is int or type(value) is float:
            return sqrt(value)


        return None

    def visitMinCall(self, ctx: EVALParser.MinCallContext) -> float | int:

        first_expression = ctx.expression(0)
        self.visit(first_expression)

        second_expression = ctx.expression(1)
        self.visit(second_expression)

        # self.validator.require_numeric(
        #     0,
        #     first_expression,
        #     "min first argument"
        # )
        #
        # self.validator.require_numeric(
        #     0,
        #     second_expression,
        #     "min second argument"
        # )

        # TODO -> check if the variables are the same type...

        # TODO
        return min(0, 0)

    def visitMaxCall(self, ctx: EVALParser.MaxCallContext) -> float | int:

        first_expression = ctx.expression(0)
        self.visit(first_expression)

        second_expression = ctx.expression(1)
        self.visit(second_expression)

        # self.validator.require_numeric(
        #     0,
        #     first_expression,
        #     "max first argument"
        # )

        # self.validator.require_numeric(
        #     0,
        #     second_expression,
        #     "max second argument"
        # )


        #TODO -> check if the variables are the same type...

        # TODO
        return max(0, 0)


    def visitRoundCall(self, ctx: EVALParser.RoundCallContext) -> float:
        expression = ctx.expression()
        self.visit(expression)

        # self.validator.require_numeric(
        #     0,
        #     expression,
        #     "round argument"
        # )

        result = self.postfix.get_result(
            expression=expression
        )
        # TODO
        return round(10.523, 2)

    def visitAbsCall(self, ctx: EVALParser.AbsCallContext) -> float:
        expression = ctx.expression()
        self.visit(expression)

        # self.validator.require_numeric(
        #     0,
        #     expression,
        #     "abs argument"
        # )

        result = self.postfix.get_result(
            expression=expression
        )

        # TODO
        return abs(result)


    def visitMacroValue(self, ctx: EVALParser.MacroValueContext) -> Any:
        if ctx.PI():
            return pi

        if ctx.DAYS_IN_WEEK():
            today = datetime.today()
            return today.weekday()

        now = datetime.now()

        if ctx.HOURS_IN_DAY():
            return  now.hour

        if ctx.YEAR():
            return now.year

        return None