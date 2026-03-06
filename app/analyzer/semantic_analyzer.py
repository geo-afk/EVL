from antlr4.Token import CommonToken

from generated.EVALParserVisitor import EVALParserVisitor
from generated.EVALParser import EVALParser
from datetime import datetime
from math import pi, sqrt, pow

class SemanticAnalyzer(EVALParserVisitor):

    def __init__(self):
        pass

    def visitProgram(self, ctx: EVALParser.ProgramContext):

        for statement in ctx.statement():
            self.visit(statement)
            print(statement)
            ...

    def visitBlock(self, ctx:EVALParser.BlockContext):

        for statement in ctx.statement():
            self.visit(statement)
            # print("Block: ",statement)

    def visitVariableDeclaration(self, ctx:EVALParser.VariableDeclarationContext):

        variable_type = self.visit(ctx.type_())
        variable_name = ctx.IDENTIFIER().getText()

        expression = self.visit(ctx.expression())

        print(variable_type, variable_name, expression)


    def visitConstDeclaration(self, ctx:EVALParser.ConstDeclarationContext):

        type = ctx.CONST()
        variable_declaration = self.visit(ctx.variableDeclaration())

        print(type, variable_declaration)


    def visitAssignment(self, ctx:EVALParser.AssignmentContext):

        variable_name = ctx.IDENTIFIER()

        assignment = self.visit(ctx.assignOp())
        expression = self.visit(ctx.expression())

        print(variable_name, assignment, expression)


    def visitAssignOp(self, ctx:EVALParser.AssignOpContext):
        _type = ctx.getText()
        return _type


    def visitType(self, ctx:EVALParser.TypeContext):
        _type = ctx.getText()
        return _type


    def visitBuiltinExpr(self, ctx:EVALParser.BuiltinExprContext):
        return self.visit(ctx.builtinFunc())


    def visitBuiltinFunc(self, ctx:EVALParser.BuiltinFuncContext):
        return self.visitChildren(ctx)


    def visitEqualityExpr(self, ctx:EVALParser.EqualityExprContext):

        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        print(left, ctx.getChild(0), right)




    def visitRelationalExpr(self, ctx:EVALParser.RelationalExprContext):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        print(left,ctx.getChild(0), right)



    def visitAdditiveExpr(self, ctx:EVALParser.AdditiveExprContext):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        print("Add: ",left, right)

        # if ctx.PLUS():
        #     return left + right
        # if ctx.MINUS():
        #     return left - right

        return None


    def visitUnaryMinusExpr(self, ctx:EVALParser.UnaryMinusExprContext):

        minus_expression = ctx.MINUS()
        expression = self.visit(ctx.expression())
        print(minus_expression, " ", expression)


    def visitParenExpr(self, ctx:EVALParser.ParenExprContext):

        left_param = ctx.LPAREN()
        expression = self.visit(ctx.expression())
        right_param = self.visit(ctx.RPAREN())

        print(left_param, " ", expression, " ", right_param)

    def visitCastCall(self, ctx:EVALParser.CastCallContext):

        expression = self.visit(ctx.expression())
        cast_type = self.visit(ctx.type_())
        print("Cast Call: ", expression, "Type: ", cast_type)

        if ctx.type_() == EVALParser.INT:
            return int(0)
        if ctx.type_() == EVALParser.REAL:
            return float(0)

        if ctx.type_() == EVALParser.BOOL:
            return bool(0)

        if ctx.type_() == EVALParser.STRING:
            return str(0)

        return None


    def visitPowCall(self, ctx:EVALParser.PowCallContext):

        left_expression = self.visit(ctx.expression(0))
        right_expression = self.visit(ctx.expression(1))
        print(left_expression, right_expression)

        # return pow(left_expression, right_expression)
        return None


    def visitSqrtCall(self, ctx:EVALParser.SqrtCallContext):

        sqrt_expression = self.visit(ctx.expression())
        print(sqrt_expression)

        # return sqrt(sqrt_expression)
        return None


    def visitMinCall(self, ctx:EVALParser.MinCallContext):
        left_min = self.visit(ctx.expression(0))
        right_min = self.visit(ctx.expression(1))

        print(left_min, " ", right_min)

        # return min(left_min, right_min)
        return None

    def visitMaxCall(self, ctx:EVALParser.MaxCallContext):

        left_expression = self.visit(ctx.expression(0))
        right_expression = self.visit(ctx.expression(1))
        print(left_expression, " ", right_expression)
    #     return max(left_expression, right_expression)
        return None


    def visitRoundCall(self, ctx:EVALParser.RoundCallContext):

        round_expression = self.visit(ctx.expression())

        print(round_expression)
        return None


    def visitAbsCall(self, ctx:EVALParser.AbsCallContext):
        expression = self.visit(ctx.exception(0))

        print(expression)
        return None

        # return abs(20)




    def visitMultiplicativeExpr(self, ctx:EVALParser.MultiplicativeExprContext):

        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        token: CommonToken = ctx.op
        print("op: ", left, token.text, right)



    def visitMacroValue(self, ctx:EVALParser.MacroValueContext):

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



    def visitIdentExpr(self, ctx:EVALParser.IdentExprContext):
        return ctx.IDENTIFIER()


    def visitIntLiteral(self, ctx:EVALParser.IntLiteralContext) -> int:
        integer = ctx.INTEGER()
        return int(str(integer).strip())


    def visitRealLiteral(self, ctx:EVALParser.RealLiteralContext) -> float:
        real = ctx.REAL()
        return float(str(real).strip())

    def visitStringLiteral(self, ctx:EVALParser.StringLiteralContext) -> str:
        return ctx.STRING()

    def visitTrueLiteral(self, ctx:EVALParser.TrueLiteralContext) -> bool:
        return True

    def visitFalseLiteral(self, ctx:EVALParser.FalseLiteralContext) -> bool:
        return False
















