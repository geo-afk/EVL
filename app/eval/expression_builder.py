from app.eval.variable_manager import VariableManager
from app.models.custom_exceptions import EVALNameException
from generated.EVALParser import EVALParser
from typing import Any, Callable


class ExpressionStringBuilder:

    @staticmethod
    def build(
        ctx:              Any,
        variable_manager: VariableManager,
        visit:            Callable[[Any], Any],
    ) -> str | None:


        # ── Literal leaves ─────────────────────────────────────────────────
        if isinstance(ctx, EVALParser.IntLiteralContext):
            token = ctx.INTEGER().getText()
            return token

        if isinstance(ctx, EVALParser.RealLiteralContext):
            token = ctx.REAL().getText()
            return token

        # ── Variable reference ─────────────────────────────────────────────
        if isinstance(ctx, EVALParser.IdentExprContext):
            name = ctx.IDENTIFIER().getText()
            try:
                var = variable_manager.get_variable(name)
                val = VariableManager.unwrap_value(var)
                if isinstance(val, (int, float)):
                    return str(val)
                return None
            except EVALNameException:
                return None

        # ── Parenthesised sub-expression ───────────────────────────────────
        if isinstance(ctx, EVALParser.ParenExprContext):
            inner = ExpressionStringBuilder.build(ctx.expression(), variable_manager, visit)
            if inner is None:
                return None
            result = f"( {inner} )"
            return result

        # ── Binary additive  (+ -) ─────────────────────────────────────────
        if isinstance(ctx, EVALParser.AdditiveExprContext):
            return ExpressionStringBuilder._build_binary_expr(
                ctx,
                ctx.expression(0),
                ctx.expression(1),
                'op',
                'AdditiveExpr',
                variable_manager,
                visit
            )

        if isinstance(ctx, EVALParser.MultiplicativeExprContext):
            return ExpressionStringBuilder._build_binary_expr(
                ctx,
                ctx.expression(0),
                ctx.expression(1),
                'op',
                'MultiplicativeExpr',
                variable_manager,
                visit
            )

        # ── Unary minus  -x  →  represented as ( 0 - x ) ─────────────────
        # Explicit (0 - x) form keeps the string free of leading minus signs
        # so Postfix never receives a bare negative literal as a first token.
        if isinstance(ctx, EVALParser.UnaryMinusExprContext):
            inner = ExpressionStringBuilder.build(ctx.expression(), variable_manager, visit)
            if inner is None:
                return None
            result = f"( 0 - {inner} )"
            return result

        # ── Builtin / macro — delegate to visitor ─────────────────────────
        # These nodes (sqrt, pow, min, max, PI, …) are opaque to string
        # building; visit() evaluates them and the numeric result is embedded.
        if isinstance(ctx, (EVALParser.BuiltinExprContext, EVALParser.MacroExprContext)):
            raw = VariableManager.unwrap_value(visit(ctx))
            if isinstance(raw, (int, float)):
                return str(raw)
            return None

        # ── Fallback — visit and embed if numeric ──────────────────────────
        raw = VariableManager.unwrap_value(visit(ctx))
        if isinstance(raw, (int, float)):
            return str(raw)

        return None

    @staticmethod
    def _build_binary_expr(ctx, left_ctx, right_ctx, op_attr, expr_name, variable_manager, visit):
        """Helper method to build binary expressions"""
        left = ExpressionStringBuilder.build(left_ctx, variable_manager, visit)
        right = ExpressionStringBuilder.build(right_ctx, variable_manager, visit)

        if left is None or right is None:
            return None

        op = getattr(ctx, op_attr)
        if hasattr(op, 'text'):
            op_text = op.text
        else:
            op_text = str(op)

        result = f"{left} {op_text} {right}"
        return result