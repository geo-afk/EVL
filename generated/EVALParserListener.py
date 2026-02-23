# Generated from EVALParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .EVALParser import EVALParser
else:
    from EVALParser import EVALParser

# This class defines a complete listener for a parse tree produced by EVALParser.
class EVALParserListener(ParseTreeListener):

    # Enter a parse tree produced by EVALParser#program.
    def enterProgram(self, ctx:EVALParser.ProgramContext):
        pass

    # Exit a parse tree produced by EVALParser#program.
    def exitProgram(self, ctx:EVALParser.ProgramContext):
        pass


    # Enter a parse tree produced by EVALParser#statement.
    def enterStatement(self, ctx:EVALParser.StatementContext):
        pass

    # Exit a parse tree produced by EVALParser#statement.
    def exitStatement(self, ctx:EVALParser.StatementContext):
        pass


    # Enter a parse tree produced by EVALParser#block.
    def enterBlock(self, ctx:EVALParser.BlockContext):
        pass

    # Exit a parse tree produced by EVALParser#block.
    def exitBlock(self, ctx:EVALParser.BlockContext):
        pass


    # Enter a parse tree produced by EVALParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:EVALParser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by EVALParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx:EVALParser.VariableDeclarationContext):
        pass


    # Enter a parse tree produced by EVALParser#constDeclaration.
    def enterConstDeclaration(self, ctx:EVALParser.ConstDeclarationContext):
        pass

    # Exit a parse tree produced by EVALParser#constDeclaration.
    def exitConstDeclaration(self, ctx:EVALParser.ConstDeclarationContext):
        pass


    # Enter a parse tree produced by EVALParser#assignment.
    def enterAssignment(self, ctx:EVALParser.AssignmentContext):
        pass

    # Exit a parse tree produced by EVALParser#assignment.
    def exitAssignment(self, ctx:EVALParser.AssignmentContext):
        pass


    # Enter a parse tree produced by EVALParser#assignOp.
    def enterAssignOp(self, ctx:EVALParser.AssignOpContext):
        pass

    # Exit a parse tree produced by EVALParser#assignOp.
    def exitAssignOp(self, ctx:EVALParser.AssignOpContext):
        pass


    # Enter a parse tree produced by EVALParser#type.
    def enterType(self, ctx:EVALParser.TypeContext):
        pass

    # Exit a parse tree produced by EVALParser#type.
    def exitType(self, ctx:EVALParser.TypeContext):
        pass


    # Enter a parse tree produced by EVALParser#minExpr.
    def enterMinExpr(self, ctx:EVALParser.MinExprContext):
        pass

    # Exit a parse tree produced by EVALParser#minExpr.
    def exitMinExpr(self, ctx:EVALParser.MinExprContext):
        pass


    # Enter a parse tree produced by EVALParser#castExpr.
    def enterCastExpr(self, ctx:EVALParser.CastExprContext):
        pass

    # Exit a parse tree produced by EVALParser#castExpr.
    def exitCastExpr(self, ctx:EVALParser.CastExprContext):
        pass


    # Enter a parse tree produced by EVALParser#macroExpr.
    def enterMacroExpr(self, ctx:EVALParser.MacroExprContext):
        pass

    # Exit a parse tree produced by EVALParser#macroExpr.
    def exitMacroExpr(self, ctx:EVALParser.MacroExprContext):
        pass


    # Enter a parse tree produced by EVALParser#sqrtExpr.
    def enterSqrtExpr(self, ctx:EVALParser.SqrtExprContext):
        pass

    # Exit a parse tree produced by EVALParser#sqrtExpr.
    def exitSqrtExpr(self, ctx:EVALParser.SqrtExprContext):
        pass


    # Enter a parse tree produced by EVALParser#realLiteral.
    def enterRealLiteral(self, ctx:EVALParser.RealLiteralContext):
        pass

    # Exit a parse tree produced by EVALParser#realLiteral.
    def exitRealLiteral(self, ctx:EVALParser.RealLiteralContext):
        pass


    # Enter a parse tree produced by EVALParser#intLiteral.
    def enterIntLiteral(self, ctx:EVALParser.IntLiteralContext):
        pass

    # Exit a parse tree produced by EVALParser#intLiteral.
    def exitIntLiteral(self, ctx:EVALParser.IntLiteralContext):
        pass


    # Enter a parse tree produced by EVALParser#absExpr.
    def enterAbsExpr(self, ctx:EVALParser.AbsExprContext):
        pass

    # Exit a parse tree produced by EVALParser#absExpr.
    def exitAbsExpr(self, ctx:EVALParser.AbsExprContext):
        pass


    # Enter a parse tree produced by EVALParser#trueLiteral.
    def enterTrueLiteral(self, ctx:EVALParser.TrueLiteralContext):
        pass

    # Exit a parse tree produced by EVALParser#trueLiteral.
    def exitTrueLiteral(self, ctx:EVALParser.TrueLiteralContext):
        pass


    # Enter a parse tree produced by EVALParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:EVALParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by EVALParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:EVALParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by EVALParser#relationalExpr.
    def enterRelationalExpr(self, ctx:EVALParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by EVALParser#relationalExpr.
    def exitRelationalExpr(self, ctx:EVALParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by EVALParser#parenExpr.
    def enterParenExpr(self, ctx:EVALParser.ParenExprContext):
        pass

    # Exit a parse tree produced by EVALParser#parenExpr.
    def exitParenExpr(self, ctx:EVALParser.ParenExprContext):
        pass


    # Enter a parse tree produced by EVALParser#roundExpr.
    def enterRoundExpr(self, ctx:EVALParser.RoundExprContext):
        pass

    # Exit a parse tree produced by EVALParser#roundExpr.
    def exitRoundExpr(self, ctx:EVALParser.RoundExprContext):
        pass


    # Enter a parse tree produced by EVALParser#maxExpr.
    def enterMaxExpr(self, ctx:EVALParser.MaxExprContext):
        pass

    # Exit a parse tree produced by EVALParser#maxExpr.
    def exitMaxExpr(self, ctx:EVALParser.MaxExprContext):
        pass


    # Enter a parse tree produced by EVALParser#identExpr.
    def enterIdentExpr(self, ctx:EVALParser.IdentExprContext):
        pass

    # Exit a parse tree produced by EVALParser#identExpr.
    def exitIdentExpr(self, ctx:EVALParser.IdentExprContext):
        pass


    # Enter a parse tree produced by EVALParser#unaryMinusExpr.
    def enterUnaryMinusExpr(self, ctx:EVALParser.UnaryMinusExprContext):
        pass

    # Exit a parse tree produced by EVALParser#unaryMinusExpr.
    def exitUnaryMinusExpr(self, ctx:EVALParser.UnaryMinusExprContext):
        pass


    # Enter a parse tree produced by EVALParser#falseLiteral.
    def enterFalseLiteral(self, ctx:EVALParser.FalseLiteralContext):
        pass

    # Exit a parse tree produced by EVALParser#falseLiteral.
    def exitFalseLiteral(self, ctx:EVALParser.FalseLiteralContext):
        pass


    # Enter a parse tree produced by EVALParser#stringLiteral.
    def enterStringLiteral(self, ctx:EVALParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by EVALParser#stringLiteral.
    def exitStringLiteral(self, ctx:EVALParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by EVALParser#powExpr.
    def enterPowExpr(self, ctx:EVALParser.PowExprContext):
        pass

    # Exit a parse tree produced by EVALParser#powExpr.
    def exitPowExpr(self, ctx:EVALParser.PowExprContext):
        pass


    # Enter a parse tree produced by EVALParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:EVALParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by EVALParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:EVALParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by EVALParser#equalityExpr.
    def enterEqualityExpr(self, ctx:EVALParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by EVALParser#equalityExpr.
    def exitEqualityExpr(self, ctx:EVALParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by EVALParser#castCall.
    def enterCastCall(self, ctx:EVALParser.CastCallContext):
        pass

    # Exit a parse tree produced by EVALParser#castCall.
    def exitCastCall(self, ctx:EVALParser.CastCallContext):
        pass


    # Enter a parse tree produced by EVALParser#powCall.
    def enterPowCall(self, ctx:EVALParser.PowCallContext):
        pass

    # Exit a parse tree produced by EVALParser#powCall.
    def exitPowCall(self, ctx:EVALParser.PowCallContext):
        pass


    # Enter a parse tree produced by EVALParser#sqrtCall.
    def enterSqrtCall(self, ctx:EVALParser.SqrtCallContext):
        pass

    # Exit a parse tree produced by EVALParser#sqrtCall.
    def exitSqrtCall(self, ctx:EVALParser.SqrtCallContext):
        pass


    # Enter a parse tree produced by EVALParser#minCall.
    def enterMinCall(self, ctx:EVALParser.MinCallContext):
        pass

    # Exit a parse tree produced by EVALParser#minCall.
    def exitMinCall(self, ctx:EVALParser.MinCallContext):
        pass


    # Enter a parse tree produced by EVALParser#maxCall.
    def enterMaxCall(self, ctx:EVALParser.MaxCallContext):
        pass

    # Exit a parse tree produced by EVALParser#maxCall.
    def exitMaxCall(self, ctx:EVALParser.MaxCallContext):
        pass


    # Enter a parse tree produced by EVALParser#roundCall.
    def enterRoundCall(self, ctx:EVALParser.RoundCallContext):
        pass

    # Exit a parse tree produced by EVALParser#roundCall.
    def exitRoundCall(self, ctx:EVALParser.RoundCallContext):
        pass


    # Enter a parse tree produced by EVALParser#absCall.
    def enterAbsCall(self, ctx:EVALParser.AbsCallContext):
        pass

    # Exit a parse tree produced by EVALParser#absCall.
    def exitAbsCall(self, ctx:EVALParser.AbsCallContext):
        pass


    # Enter a parse tree produced by EVALParser#macroValue.
    def enterMacroValue(self, ctx:EVALParser.MacroValueContext):
        pass

    # Exit a parse tree produced by EVALParser#macroValue.
    def exitMacroValue(self, ctx:EVALParser.MacroValueContext):
        pass


    # Enter a parse tree produced by EVALParser#printStatement.
    def enterPrintStatement(self, ctx:EVALParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by EVALParser#printStatement.
    def exitPrintStatement(self, ctx:EVALParser.PrintStatementContext):
        pass


    # Enter a parse tree produced by EVALParser#printArg.
    def enterPrintArg(self, ctx:EVALParser.PrintArgContext):
        pass

    # Exit a parse tree produced by EVALParser#printArg.
    def exitPrintArg(self, ctx:EVALParser.PrintArgContext):
        pass


    # Enter a parse tree produced by EVALParser#ifStatement.
    def enterIfStatement(self, ctx:EVALParser.IfStatementContext):
        pass

    # Exit a parse tree produced by EVALParser#ifStatement.
    def exitIfStatement(self, ctx:EVALParser.IfStatementContext):
        pass


    # Enter a parse tree produced by EVALParser#whileStatement.
    def enterWhileStatement(self, ctx:EVALParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by EVALParser#whileStatement.
    def exitWhileStatement(self, ctx:EVALParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by EVALParser#tryStatement.
    def enterTryStatement(self, ctx:EVALParser.TryStatementContext):
        pass

    # Exit a parse tree produced by EVALParser#tryStatement.
    def exitTryStatement(self, ctx:EVALParser.TryStatementContext):
        pass



del EVALParser