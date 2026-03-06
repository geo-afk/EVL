from generated.EVALParserVisitor import EVALParserVisitor
from generated.EVALParser import EVALParser
from datetime import datetime
from math import pi

class SemanticAnalyzer(EVALParserVisitor):



    def __init__(self):
        pass

    def visitProgram(self, ctx: EVALParser.ProgramContext):

        for statement in ctx.statement():
            self.visit(statement)
            print(statement)
            ...

    def visitVariableDeclaration(self, ctx:EVALParser.VariableDeclarationContext):

        variable_type = self.visit(ctx.type_())
        variable_name = ctx.IDENTIFIER().getText()
        # print(variable_type)
        # print(variable_name)




    def visitType(self, ctx:EVALParser.TypeContext):
        _type = ctx.getText()
        return _type

    def visitEqualityExpr(self, ctx:EVALParser.EqualityExprContext):
        print(ctx.getText())



    def visitMultiplicativeExpr(self, ctx:EVALParser.MultiplicativeExprContext):

        value = self.visitChildren(ctx)
        token = ctx.op
        print("token: ", token)

        # print("Operator", token.getText())

        print("Value: ", ctx.getText())



    def visitMacroValue(self, ctx:EVALParser.MacroValueContext):

        value: str = ctx.getChild(0).getText().strip()

        if value == "PI":
            return pi

        if value == "DAYS_IN_WEEK":
            today = datetime.today()
            return today.weekday()

        now = datetime.now()

        if value == "HOURS_IN_DAY":
            return  now.hour

        if value == "YEAR":
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
















