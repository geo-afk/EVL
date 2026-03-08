from app.eval.semantic_validation import SemanticValidation
from typing import List

from app.models.CustomError import ErrorResponse, WarningResponse
from app.models.Scope import Scope
from app.models.Symbol import Symbol
from app.models.Types import EvalType, NUMERIC, TYPE_MAP
from generated.EVALParser import EVALParser

# ---------------------------------------------------------------------------
# Lazy imports – generated files may not exist in every environment
# ---------------------------------------------------------------------------

try:
    from generated.EVALParserVisitor import EVALParserVisitor as _BASE
except ImportError:
    from antlr4 import ParseTreeVisitor as _BASE


class SemanticAnalyzer(_BASE):  # type: ignore[misc]
    """
    Walk the parse tree and perform semantic checks.

    After `visit(tree)`:
      • self.errors        – list of error strings
      • self.warnings      – list of warning strings
      • self.symbol_table  – dict snapshot of the global scope
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

    # ── block ──────────────────────────────────────────────────────────────

    def visitBlock(self, ctx) -> None:
        self._push_scope()
        # Scope.
        for stmt in ctx.statement():
            self.visit(stmt)
        self._pop_scope()

    # ── variableDeclaration ────────────────────────────────────────────────

    def visitVariableDeclaration(self, ctx) -> None:
        type_text  = ctx.type_().getText()
        decl_type  = TYPE_MAP.get(type_text, EvalType.UNKNOWN)
        ident_tok  = ctx.IDENTIFIER().getSymbol()
        name       = ident_tok.text
        line, col  = self._tok_line(ident_tok), self._tok_col(ident_tok)

        expr_type = self.visit(ctx.expression())

        # Type-compatibility check
        if expr_type not in (EvalType.UNKNOWN, None):
            if decl_type != EvalType.UNKNOWN:
                compatible = self.validator.types_compatible(decl_type, expr_type)
                if not compatible:
                    self._error(
                        f"cannot assign {expr_type.name} to variable of type {decl_type.name} '{name}'",
                        line, col,
                    )
                elif decl_type == EvalType.FLOAT and expr_type == EvalType.INT:
                    self._warn(
                        f"implicit int→float conversion when assigning to '{name}'",
                        line, col,
                    )

        sym = Symbol(name=name, eval_type=decl_type, is_const=False, line=line, column=col)
        if not self._current_scope.define(sym):
            self._error(f"variable '{name}' already declared in this scope", line, col)

    # ── constDeclaration ───────────────────────────────────────────────────

    def visitConstDeclaration(self, ctx) -> None:
        # Visit the inner variableDeclaration first to register the symbol …
        inner = ctx.variableDeclaration()
        self.visitVariableDeclaration(inner)
        # … then mark the symbol as const.
        name = inner.IDENTIFIER().getSymbol().text
        sym  = self._current_scope.resolve(name)
        if sym:
            sym.is_const = True

    # ── assignment ─────────────────────────────────────────────────────────

    def visitAssignment(self, ctx) -> None:
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name      = ident_tok.text
        line, col = self._tok_line(ident_tok), self._tok_col(ident_tok)

        sym = self._current_scope.resolve(name)
        if sym is None:
            self._error(f"assignment to undeclared variable '{name}'", line, col)
            self.visit(ctx.expression())
            return

        if sym.is_const:
            self._error(f"cannot reassign const variable '{name}'", line, col)

        expr_type = self.visit(ctx.expression())
        op_text   = ctx.assignOp().getText()

        # Compound operators (+=, -= etc.) require numeric operands
        if op_text != "=" and sym.eval_type not in NUMERIC:
            self._error(
                f"compound assignment '{op_text}' requires a numeric variable; '{name}' is {sym.eval_type.name}",
                line, col,
            )

        if expr_type not in (EvalType.UNKNOWN, None):
            if not self.validator.types_compatible(sym.eval_type, expr_type):
                self._error(
                    f"type mismatch: cannot assign {expr_type.name} to '{name}' ({sym.eval_type.name})",
                    line, col,
                )

    # ── incrementDecrement ─────────────────────────────────────────────────

    def visitIncrementDecrement(self, ctx) -> None:
        ident_tok = ctx.IDENTIFIER().getSymbol()
        name      = ident_tok.text
        line, col = self._tok_line(ident_tok), self._tok_col(ident_tok)

        sym = self._current_scope.resolve(name)
        if sym is None:
            self._error(f"use of undeclared variable '{name}'", line, col)
            return
        if sym.is_const:
            op = ctx.INCREMENT() and "++" or "--"
            self._error(f"cannot apply '{op}' to const variable '{name}'", line, col)
        if sym.eval_type not in NUMERIC:
            op = "++" if ctx.INCREMENT() else "--"
            self._error(
                f"'{op}' requires a numeric variable; '{name}' is {sym.eval_type.name}",
                line, col,
            )

    # ── printStatement ─────────────────────────────────────────────────────

    def visitPrintStatement(self, ctx) -> None:
        for arg in ctx.printArg():
            self.visit(arg)

    def visitPrintArg(self, ctx) -> None:
        self.visit(ctx.expression())

    # ── ifStatement ────────────────────────────────────────────────────────

    def visitIfStatement(self, ctx) -> None:
        for expr in ctx.expression():
            cond_type = self.visit(expr)
            line = expr.start.line
            col  = expr.start.column
            if cond_type not in (EvalType.BOOL, EvalType.UNKNOWN, None):
                self._warn(
                    f"condition is of type {cond_type.name}, not bool — may behave unexpectedly",
                    line, col,
                )
        for blk in ctx.block():
            self.visit(blk)

    # ── whileStatement ─────────────────────────────────────────────────────

    def visitWhileStatement(self, ctx) -> None:
        cond_type = self.visit(ctx.expression())
        if cond_type not in (EvalType.BOOL, EvalType.UNKNOWN, None):
            self._warn(
                f"while condition is {cond_type.name}, not bool",
                ctx.expression().start.line,
                ctx.expression().start.column,
            )
        self._loop_depth += 1
        self.visit(ctx.block())
        self._loop_depth -= 1

    # ── tryStatement ───────────────────────────────────────────────────────

    def visitTryStatement(self, ctx) -> None:
        blocks = ctx.block()
        self.visit(blocks[0])   # try block

        # Introduce catch variable into catch scope
        self._push_scope(name="catch")
        ident_tok = ctx.IDENTIFIER().getSymbol()
        catch_sym = Symbol(
            name=ident_tok.text,
            eval_type=EvalType.UNKNOWN,  # exception object — type unknown at static time
            line=self._tok_line(ident_tok),
            column=self._tok_col(ident_tok),
        )
        self._current_scope.define(catch_sym)
        # Visit the catch block body statements directly so we don't double-push scope
        catch_block = blocks[1]
        for stmt in catch_block.statement():
            self.visit(stmt)
        self._pop_scope()

    # ── breakStatement ─────────────────────────────────────────────────────

    def visitBreakStatement(self, ctx) -> None:
        if self._loop_depth == 0:
            self._error(
                "'break' used outside of a loop",
                ctx.start.line, ctx.start.column,
            )

    # ── continueStatement ──────────────────────────────────────────────────

    def visitContinueStatement(self, ctx) -> None:
        if self._loop_depth == 0:
            self._error(
                "'continue' used outside of a loop",
                ctx.start.line, ctx.start.column,
            )

    # ══════════════════════════════════════════════════════════════════════
    #  Expression visitors — all return EvalType
    # ══════════════════════════════════════════════════════════════════════

    def visitLogicalOrExpr(self, ctx) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        self.validator.check_logical_operands("||", lt, rt, ctx.start.line, ctx.start.column)
        return EvalType.BOOL

    def visitLogicalAndExpr(self, ctx) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        self.validator.check_logical_operands("&&", lt, rt, ctx.start.line, ctx.start.column)
        return EvalType.BOOL

    def visitEqualityExpr(self, ctx) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        if (
            lt not in (EvalType.UNKNOWN, None)
            and rt not in (EvalType.UNKNOWN, None)
            and not self.validator.types_compatible(lt, rt)
        ):
            self._warn(
                f"comparing incompatible types {lt.name} and {rt.name}",
                ctx.start.line, ctx.start.column,
            )
        return EvalType.BOOL

    def visitRelationalExpr(self, ctx) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        for t in (lt, rt):
            if t not in (EvalType.UNKNOWN, None) and t not in NUMERIC:
                self._error(
                    f"relational operator requires numeric operands, got {t.name}",
                    ctx.start.line, ctx.start.column,
                )
                return EvalType.UNKNOWN
        return EvalType.BOOL

    def visitAdditiveExpr(self, ctx) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        op = ctx.op.text
        # '+' is also valid for string concatenation
        if op == "+":
            if lt == EvalType.STRING or rt == EvalType.STRING:
                return EvalType.STRING
        return self.validator.numeric_result(op, lt, rt, ctx.start.line, ctx.start.column)

    def visitMultiplicativeExpr(self, ctx) -> EvalType:
        lt = self.visit(ctx.expression(0))
        rt = self.visit(ctx.expression(1))
        op = ctx.op.text

        # Static division-by-zero detection
        if op == "/" and hasattr(ctx.expression(1), "INTEGER"):
            rhs_ctx = ctx.expression(1)
            if hasattr(rhs_ctx, "INTEGER") and rhs_ctx.INTEGER() is not None:
                if int(rhs_ctx.INTEGER().getText()) == 0:
                    self._error("division by zero (static)", ctx.start.line, ctx.start.column)

        return self.validator.numeric_result(op, lt, rt, ctx.start.line, ctx.start.column)

    def visitUnaryMinusExpr(self, ctx) -> EvalType:
        t = self.visit(ctx.expression())
        if t not in (EvalType.UNKNOWN, None) and t not in NUMERIC:
            self._error(f"unary '-' requires a numeric operand, got {t.name}",
                        ctx.start.line, ctx.start.column)
        return t if t in NUMERIC else EvalType.UNKNOWN

    def visitUnaryNotExpr(self, ctx) -> EvalType:
        t = self.visit(ctx.expression())
        if t not in (EvalType.BOOL, EvalType.UNKNOWN, None):
            self._warn(
                f"'!' applied to {t.name} — expected bool",
                ctx.start.line, ctx.start.column,
            )
        return EvalType.BOOL

    def visitParenExpr(self, ctx) -> EvalType:
        return self.visit(ctx.expression())

    def visitBuiltinExpr(self, ctx) -> EvalType:
        return self.visit(ctx.builtinFunc())

    # ── Primaries ──────────────────────────────────────────────────────────

    def visitIdentExpr(self, ctx) -> EvalType:
        tok  = ctx.IDENTIFIER().getSymbol()
        name = tok.text
        sym  = self._current_scope.resolve(name)
        if sym is None:
            self._error(f"use of undeclared variable '{name}'",
                        self._tok_line(tok), self._tok_col(tok))
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

    def visitMacroExpr(self, _ctx) -> EvalType:
        return EvalType.FLOAT   # all built-in macros are numeric (PI, etc.)

    # ── Built-in functions ─────────────────────────────────────────────────

    def visitBuiltinFunc(self, ctx) -> EvalType:
        return self.visitChildren(ctx) or EvalType.UNKNOWN

    def visitCastCall(self, ctx) -> EvalType:
        self.visit(ctx.expression())
        target_text = ctx.type_().getText()
        return TYPE_MAP.get(target_text, EvalType.UNKNOWN)

    def visitPowCall(self, ctx) -> EvalType:
        self.validator.require_numeric(ctx.expression(0), "pow base")
        self.validator.require_numeric(ctx.expression(1), "pow exponent")
        return EvalType.FLOAT

    def visitSqrtCall(self, ctx) -> EvalType:
        self.validator.require_numeric(ctx.expression(), "sqrt argument")
        return EvalType.FLOAT

    def visitMinCall(self, ctx) -> EvalType:
        self.validator.require_numeric(ctx.expression(0), "min first argument")
        self.validator.require_numeric(ctx.expression(1), "min second argument")
        return EvalType.FLOAT

    def visitMaxCall(self, ctx) -> EvalType:
        self.validator.require_numeric(ctx.expression(0), "max first argument")
        self.validator.require_numeric(ctx.expression(1), "max second argument")
        return EvalType.FLOAT

    def visitRoundCall(self, ctx) -> EvalType:
        self.validator.require_numeric(ctx.expression(), "round argument")
        return EvalType.INT

    def visitAbsCall(self, ctx: EVALParser.AbsCallContext) -> EvalType:
        return self.validator.require_numeric(ctx.expression(), "abs argument")

    # ── Macro ──────────────────────────────────────────────────────────────
    def visitMacroValue(self, _ctx) -> EvalType:
        return EvalType.FLOAT

