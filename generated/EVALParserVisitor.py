# Generated from EVALParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .EVALParser import EVALParser
else:
    from EVALParser import EVALParser

# This class defines a complete generic visitor for a parse tree produced by EVALParser.

class EVALParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by EVALParser#program.
    def visitProgram(self, ctx:EVALParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#statement.
    def visitStatement(self, ctx:EVALParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#block.
    def visitBlock(self, ctx:EVALParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:EVALParser.VariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#constDeclaration.
    def visitConstDeclaration(self, ctx:EVALParser.ConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#assignment.
    def visitAssignment(self, ctx:EVALParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#assignOp.
    def visitAssignOp(self, ctx:EVALParser.AssignOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#incrementDecrement.
    def visitIncrementDecrement(self, ctx:EVALParser.IncrementDecrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#breakStatement.
    def visitBreakStatement(self, ctx:EVALParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#continueStatement.
    def visitContinueStatement(self, ctx:EVALParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#type.
    def visitType(self, ctx:EVALParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#nullLiteral.
    def visitNullLiteral(self, ctx:EVALParser.NullLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#builtinExpr.
    def visitBuiltinExpr(self, ctx:EVALParser.BuiltinExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#logicalAndExpr.
    def visitLogicalAndExpr(self, ctx:EVALParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#macroExpr.
    def visitMacroExpr(self, ctx:EVALParser.MacroExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#realLiteral.
    def visitRealLiteral(self, ctx:EVALParser.RealLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#intLiteral.
    def visitIntLiteral(self, ctx:EVALParser.IntLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#trueLiteral.
    def visitTrueLiteral(self, ctx:EVALParser.TrueLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:EVALParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#relationalExpr.
    def visitRelationalExpr(self, ctx:EVALParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#parenExpr.
    def visitParenExpr(self, ctx:EVALParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#identExpr.
    def visitIdentExpr(self, ctx:EVALParser.IdentExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#logicalOrExpr.
    def visitLogicalOrExpr(self, ctx:EVALParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#unaryMinusExpr.
    def visitUnaryMinusExpr(self, ctx:EVALParser.UnaryMinusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#falseLiteral.
    def visitFalseLiteral(self, ctx:EVALParser.FalseLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#stringLiteral.
    def visitStringLiteral(self, ctx:EVALParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#unaryNotExpr.
    def visitUnaryNotExpr(self, ctx:EVALParser.UnaryNotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:EVALParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#equalityExpr.
    def visitEqualityExpr(self, ctx:EVALParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#builtinFunc.
    def visitBuiltinFunc(self, ctx:EVALParser.BuiltinFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#builtinCallStatement.
    def visitBuiltinCallStatement(self, ctx:EVALParser.BuiltinCallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#castCall.
    def visitCastCall(self, ctx:EVALParser.CastCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#powCall.
    def visitPowCall(self, ctx:EVALParser.PowCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#sqrtCall.
    def visitSqrtCall(self, ctx:EVALParser.SqrtCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#minCall.
    def visitMinCall(self, ctx:EVALParser.MinCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#maxCall.
    def visitMaxCall(self, ctx:EVALParser.MaxCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#roundCall.
    def visitRoundCall(self, ctx:EVALParser.RoundCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#absCall.
    def visitAbsCall(self, ctx:EVALParser.AbsCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#macroValue.
    def visitMacroValue(self, ctx:EVALParser.MacroValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#printStatement.
    def visitPrintStatement(self, ctx:EVALParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#printArg.
    def visitPrintArg(self, ctx:EVALParser.PrintArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#ifStatement.
    def visitIfStatement(self, ctx:EVALParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#whileStatement.
    def visitWhileStatement(self, ctx:EVALParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EVALParser#tryStatement.
    def visitTryStatement(self, ctx:EVALParser.TryStatementContext):
        return self.visitChildren(ctx)



del EVALParser