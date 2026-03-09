from app.models.CustomError import ErrorResponse, WarningResponse
from app.eval.semantic_validation import SemanticValidation
from app.models.Types import EvalType, NUMERIC, TYPE_MAP, EMPTY
from generated.EVALParser import EVALParser
from app.models.Variable import Variable, Position
from app.models.Scope import Scope
from datetime import datetime
from typing import List, Any
from math import pi

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
        self._global_scope  = Scope(name="global")
        self._current_scope = self._global_scope
        self._loop_depth    = 0       # tracks nesting depth for break/continue

        self.errors:   List[ErrorResponse] = []
        self.warnings: List[WarningResponse] = []

        self.validator = SemanticValidation()


    def visitProgram(self, ctx) -> None:
        self.visitChildren(ctx)


    def visitBlock(self, ctx) -> None:
        self._current_scope = Scope.push_scope(
            self._current_scope
        )


        for stmt in ctx.statement():
            self.visit(stmt)

        self._current_scope = Scope.pop_scope(
            self._current_scope,
            validator=self.validator,
        )

    @staticmethod
    def _tok_line(token) -> int:
        return token.line if token else 0

    @staticmethod
    def _tok_col(token) -> int:
        return token.column if token else 0


    def visitVariableDeclaration(self, ctx: EVALParser.VariableDeclarationContext) -> None:
        type_text  = ctx.type_().getText()
        decl_type  = TYPE_MAP.get(type_text, EvalType.UNKNOWN)
        ident_tok  = ctx.IDENTIFIER().getSymbol()
        name       = ident_tok.text

        expr_type = self.visit(ctx.expression())

        # Type-compatibility check
        if expr_type not in (EvalType.UNKNOWN, None):
            if decl_type != EvalType.UNKNOWN:
                compatible = self.validator.types_compatible(decl_type, expr_type)
                if not compatible:

                    self.validator.push_error(
                        ident_tok,
                        f"cannot assign {expr_type.name} to variable of type {decl_type.name} '{name}'"
                    )
                elif decl_type == EvalType.FLOAT and expr_type == EvalType.INT:

                    self.validator.push_warnings(
                        ident_tok,
                        f"implicit int→float conversion when assigning to '{name}'",
                    )

        column, line = self.validator.tok_col_line(ident_tok)
        variable = Variable(
            name=name,
            type=decl_type,
            value=0,
            position= Position(
                line=line,
                column=column
            )
        )
        print("Symbol: ",variable)
        if not self._current_scope.define(sym):

            self.validator.push_error(
                ident_tok,
                f"variable '{name}' already declared in this scope"
            )


    def visitConstDeclaration(self, ctx: EVALParser.ConstDeclarationContext) -> None:
        # Visit the inner variableDeclaration first to register the symbol …
        variable_declaration = ctx.variableDeclaration()
        self.visit(variable_declaration)
        # … then mark the symbol as const.
        name = variable_declaration.IDENTIFIER().getSymbol().text
        sym  = self._current_scope.resolve(name)
        if sym:
            sym.is_const = True


    def visitAssignment(self, ctx: EVALParser.AssignmentContext) -> None:
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name      = ident_tok.text

        sym = self._current_scope.resolve(name)
        if sym is None:
            self.validator.push_error(
                ident_tok,
                f"assignment to undeclared variable '{name}'"
            )

            self.visit(ctx.expression())
            return

        if sym.is_const:
            self.validator.push_error(
                ident_tok,
                f"cannot reassign const variable '{name}'"
            )

        expr_type = self.visit(ctx.expression())
        op_text   = ctx.assignOp().getText()

        # Compound operators (+=, -= etc.) require numeric operands
        if op_text != "=" and sym.eval_type not in NUMERIC:
            self.validator.push_error(
                ident_tok,

                f"compound assignment '{op_text}' requires a numeric variable; '{name}' is {sym.eval_type.name}",
            )


        if expr_type not in (EvalType.UNKNOWN, None):
            if not self.validator.types_compatible(sym.eval_type, expr_type):
                self.validator.push_error(
                    ident_tok,
                    f"type mismatch: cannot assign {expr_type.name} to '{name}' ({sym.eval_type.name})",
                )



    def visitIncrementDecrement(self, ctx: EVALParser.IncrementDecrementContext) -> None:
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name      = ident_tok.text

        sym = self._current_scope.resolve(name)
        if sym is None:
            self.validator.push_error(
                ident_tok,
                f"use of undeclared variable '{name}'"
            )

            return
        if sym.is_const:
            op = ctx.INCREMENT() and "++" or "--"
            self.validator.push_error(
                ident_tok,
                f"cannot apply '{op}' to const variable '{name}'"
            )

        if sym.eval_type not in NUMERIC:
            op = "++" if ctx.INCREMENT() else "--"
            self.validator.push_error(
                ident_tok,
                f"'{op}' requires a numeric variable; '{name}' is {sym.eval_type.name}",

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

        self._current_scope = Scope.push_scope(
            self._current_scope,
            name="catch"
        )

        ident_tok = ctx.IDENTIFIER().getSymbol()
        catch_sym = Symbol(
            name=ident_tok.text,
            eval_type=EvalType.UNKNOWN,  # exception object — type unknown at static time
            line=self._tok_line(ident_tok),
            column=self._tok_col(ident_tok),
        )
        print("Catch: ", catch_sym)
        self._current_scope.define(catch_sym)
        # Visit the catch block body statements directly so we don't double-push scope
        catch_block = blocks[1]
        for stmt in catch_block.statement():
            self.visit(stmt)

        self._current_scope = Scope.pop_scope(
            self._current_scope,
            self.validator
        )

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
            lt not in EMPTY
            and rt not in EMPTY
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
            if t not in EMPTY and t not in NUMERIC:

                self.validator.push_error(
                    ctx.start,
                    f"relational operator requires numeric operands, got {t.name}",
                )

                return EvalType.UNKNOWN
        return EvalType.BOOL

    def visitAdditiveExpr(self, ctx: EVALParser.AdditiveExprContext) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        op = ctx.op.text
        # '+' is also valid for string concatenation
        if op == "+":
            if lt == EvalType.STRING or rt == EvalType.STRING:
                return EvalType.STRING
        return self.validator.numeric_result(op, lt, rt, ctx.start)

    def visitMultiplicativeExpr(self, ctx: EVALParser.MultiplicativeExprContext) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        op = ctx.op.text

        # Static division-by-zero detection
        if op == "/" and hasattr(ctx.expression(1), "INTEGER"):
            rhs_ctx = ctx.expression(1)
            if hasattr(rhs_ctx, "INTEGER") and rhs_ctx.INTEGER() is not None:
                if int(rhs_ctx.INTEGER().getText()) == 0:
                    self.validator.push_error(
                        ctx.start,
                        "division by zero (static)"
                    )

        return self.validator.numeric_result(op, lt, rt, ctx.start)

    def visitUnaryMinusExpr(self, ctx: EVALParser.UnaryMinusExprContext) -> EvalType:
        t = self.visit(ctx.expression())
        if t not in EMPTY and t not in NUMERIC:

            self.validator.push_error(
                ctx.start,
                f"unary '-' requires a numeric operand, got {t.name}"
            )

        return t if t in NUMERIC else EvalType.UNKNOWN

    def visitUnaryNotExpr(self, ctx: EVALParser.UnaryNotExprContext) -> EvalType:
        t = self.visit(ctx.expression())
        if t not in (EvalType.BOOL, EvalType.UNKNOWN, None):

            self.validator.push_warnings(
                ctx.start,
                f"'!' applied to {t.name} — expected bool",
            )

        return EvalType.BOOL

    def visitParenExpr(self, ctx: EVALParser.ParenExprContext) -> EvalType:
        return self.visit(ctx.expression())

    def visitBuiltinExpr(self, ctx: EVALParser.BuiltinExprContext) -> EvalType:
        return self.visit(ctx.builtinFunc())

    # ── Primaries ──────────────────────────────────────────────────────────

    def visitIdentExpr(self, ctx: EVALParser.IdentExprContext) -> EvalType:
        tok  = ctx.IDENTIFIER().getSymbol()
        name = tok.text
        sym  = self._current_scope.resolve(name)
        if sym is None:
            self.validator.push_error(
                tok,
                f"use of undeclared variable '{name}'"
            )

            return EvalType.UNKNOWN
        return sym.eval_type

    def visitIntLiteral(self, _ctx) -> EvalType:
        return EvalType.INT

    def visitRealLiteral(self, _ctx) -> EvalType:
        return EvalType.FLOAT

    def visitStringLiteral(self, _ctx) -> EvalType:
        return EvalType.STRING

    def visitTrueLiteral(self, _ctx) -> EvalType:
        return EvalType.BOOL

    def visitFalseLiteral(self, _ctx) -> EvalType:
        return EvalType.BOOL

    def visitNullLiteral(self, _ctx) -> EvalType:
        return EvalType.NULL

    def visitMacroExpr(self, ctx: EVALParser.MacroExprContext):
        return self.visit(ctx.macroValue())

    # ── Built-in functions ─────────────────────────────────────────────────

    def visitBuiltinFunc(self, ctx: EVALParser.BuiltinFuncContext) -> EvalType:
        return self.visitChildren(ctx) or EvalType.UNKNOWN

    def visitCastCall(self, ctx) -> EvalType:
        self.visit(ctx.expression())
        target_text = ctx.type_().getText()
        return TYPE_MAP.get(target_text, EvalType.UNKNOWN)


    def visitPowCall(self, ctx: EVALParser.PowCallContext) -> EvalType:

        first_expression = ctx.expression(0)
        second_expression = ctx.expression(1)

        self.validator.require_numeric(
            self.visit(first_expression),
            first_expression,
            "pow base"
        )

        self.validator.require_numeric(
            self.visit(second_expression),
            second_expression,
            "pow exponent"
        )
        return EvalType.FLOAT

    def visitSqrtCall(self, ctx: EVALParser.SqrtCallContext) -> EvalType:

        expression = ctx.expression()

        self.validator.require_numeric(
            self.visit(expression),
            expression,
            "sqrt argument"
        )
        return EvalType.FLOAT

    def visitMinCall(self, ctx: EVALParser.MinCallContext) -> EvalType:

        first_expression = ctx.expression(0)
        second_expression = ctx.expression(1)

        self.validator.require_numeric(
            self.visit(first_expression),
            first_expression,
            "min first argument"
        )

        self.validator.require_numeric(
            self.visit(second_expression),
            second_expression,
            "min second argument"
        )
        return EvalType.FLOAT

    def visitMaxCall(self, ctx: EVALParser.MaxCallContext) -> EvalType:

        first_expression = ctx.expression(0)
        second_expression = ctx.expression(1)
        self.validator.require_numeric(
            self.visit(first_expression),
            first_expression,
            "max first argument"
        )

        self.validator.require_numeric(
            self.visit(second_expression),
            second_expression,
            "max second argument"
        )
        return EvalType.FLOAT

    def visitRoundCall(self, ctx: EVALParser.RoundCallContext) -> EvalType:
        expression = ctx.expression()

        self.validator.require_numeric(
            self.visit(expression),
            expression,
            "round argument"
        )
        return EvalType.INT

    def visitAbsCall(self, ctx: EVALParser.AbsCallContext) -> EvalType:
        expression = ctx.expression()

        return self.validator.require_numeric(
            self.visit(expression),
            expression,
            "abs argument"
        )


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

