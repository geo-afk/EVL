# Generated from EVALParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,52,224,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,1,0,5,0,46,8,0,10,0,12,0,49,9,0,1,0,1,0,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,3,1,61,8,1,1,2,1,2,5,2,65,8,2,10,2,12,2,68,
        9,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,6,
        1,6,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,
        1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,109,8,8,1,8,1,8,1,8,1,8,1,8,
        1,8,1,8,1,8,1,8,1,8,1,8,1,8,5,8,123,8,8,10,8,12,8,126,9,8,1,9,1,
        9,1,9,1,9,1,9,1,9,1,9,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,11,1,
        11,1,11,1,11,1,11,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,13,1,13,1,
        13,1,13,1,13,1,13,1,13,1,14,1,14,1,14,1,14,1,14,1,15,1,15,1,15,1,
        15,1,15,1,16,1,16,1,17,1,17,1,17,1,17,1,17,5,17,178,8,17,10,17,12,
        17,181,9,17,1,17,1,17,1,18,1,18,3,18,187,8,18,1,19,1,19,1,19,1,19,
        1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,5,19,201,8,19,10,19,12,19,
        204,9,19,1,19,1,19,3,19,208,8,19,1,20,1,20,1,20,1,20,1,20,1,20,1,
        21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,0,1,16,22,0,2,4,6,8,10,
        12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,0,7,2,0,30,33,40,
        40,1,0,1,4,1,0,34,35,1,0,36,39,1,0,25,26,1,0,27,29,1,0,21,24,233,
        0,47,1,0,0,0,2,60,1,0,0,0,4,62,1,0,0,0,6,71,1,0,0,0,8,76,1,0,0,0,
        10,79,1,0,0,0,12,83,1,0,0,0,14,85,1,0,0,0,16,108,1,0,0,0,18,127,
        1,0,0,0,20,134,1,0,0,0,22,141,1,0,0,0,24,146,1,0,0,0,26,153,1,0,
        0,0,28,160,1,0,0,0,30,165,1,0,0,0,32,170,1,0,0,0,34,172,1,0,0,0,
        36,186,1,0,0,0,38,188,1,0,0,0,40,209,1,0,0,0,42,215,1,0,0,0,44,46,
        3,2,1,0,45,44,1,0,0,0,46,49,1,0,0,0,47,45,1,0,0,0,47,48,1,0,0,0,
        48,50,1,0,0,0,49,47,1,0,0,0,50,51,5,0,0,1,51,1,1,0,0,0,52,61,3,6,
        3,0,53,61,3,8,4,0,54,61,3,10,5,0,55,61,3,34,17,0,56,61,3,38,19,0,
        57,61,3,40,20,0,58,61,3,42,21,0,59,61,3,4,2,0,60,52,1,0,0,0,60,53,
        1,0,0,0,60,54,1,0,0,0,60,55,1,0,0,0,60,56,1,0,0,0,60,57,1,0,0,0,
        60,58,1,0,0,0,60,59,1,0,0,0,61,3,1,0,0,0,62,66,5,41,0,0,63,65,3,
        2,1,0,64,63,1,0,0,0,65,68,1,0,0,0,66,64,1,0,0,0,66,67,1,0,0,0,67,
        69,1,0,0,0,68,66,1,0,0,0,69,70,5,42,0,0,70,5,1,0,0,0,71,72,3,14,
        7,0,72,73,5,49,0,0,73,74,5,40,0,0,74,75,3,16,8,0,75,7,1,0,0,0,76,
        77,5,5,0,0,77,78,3,6,3,0,78,9,1,0,0,0,79,80,5,49,0,0,80,81,3,12,
        6,0,81,82,3,16,8,0,82,11,1,0,0,0,83,84,7,0,0,0,84,13,1,0,0,0,85,
        86,7,1,0,0,86,15,1,0,0,0,87,88,6,8,-1,0,88,89,5,26,0,0,89,109,3,
        16,8,16,90,91,5,43,0,0,91,92,3,16,8,0,92,93,5,44,0,0,93,109,1,0,
        0,0,94,109,3,18,9,0,95,109,3,20,10,0,96,109,3,22,11,0,97,109,3,24,
        12,0,98,109,3,26,13,0,99,109,3,28,14,0,100,109,3,30,15,0,101,109,
        3,32,16,0,102,109,5,49,0,0,103,109,5,47,0,0,104,109,5,46,0,0,105,
        109,5,48,0,0,106,109,5,11,0,0,107,109,5,12,0,0,108,87,1,0,0,0,108,
        90,1,0,0,0,108,94,1,0,0,0,108,95,1,0,0,0,108,96,1,0,0,0,108,97,1,
        0,0,0,108,98,1,0,0,0,108,99,1,0,0,0,108,100,1,0,0,0,108,101,1,0,
        0,0,108,102,1,0,0,0,108,103,1,0,0,0,108,104,1,0,0,0,108,105,1,0,
        0,0,108,106,1,0,0,0,108,107,1,0,0,0,109,124,1,0,0,0,110,111,10,20,
        0,0,111,112,7,2,0,0,112,123,3,16,8,21,113,114,10,19,0,0,114,115,
        7,3,0,0,115,123,3,16,8,20,116,117,10,18,0,0,117,118,7,4,0,0,118,
        123,3,16,8,19,119,120,10,17,0,0,120,121,7,5,0,0,121,123,3,16,8,18,
        122,110,1,0,0,0,122,113,1,0,0,0,122,116,1,0,0,0,122,119,1,0,0,0,
        123,126,1,0,0,0,124,122,1,0,0,0,124,125,1,0,0,0,125,17,1,0,0,0,126,
        124,1,0,0,0,127,128,5,14,0,0,128,129,5,43,0,0,129,130,3,16,8,0,130,
        131,5,45,0,0,131,132,3,14,7,0,132,133,5,44,0,0,133,19,1,0,0,0,134,
        135,5,15,0,0,135,136,5,43,0,0,136,137,3,16,8,0,137,138,5,45,0,0,
        138,139,3,16,8,0,139,140,5,44,0,0,140,21,1,0,0,0,141,142,5,16,0,
        0,142,143,5,43,0,0,143,144,3,16,8,0,144,145,5,44,0,0,145,23,1,0,
        0,0,146,147,5,17,0,0,147,148,5,43,0,0,148,149,3,16,8,0,149,150,5,
        45,0,0,150,151,3,16,8,0,151,152,5,44,0,0,152,25,1,0,0,0,153,154,
        5,18,0,0,154,155,5,43,0,0,155,156,3,16,8,0,156,157,5,45,0,0,157,
        158,3,16,8,0,158,159,5,44,0,0,159,27,1,0,0,0,160,161,5,19,0,0,161,
        162,5,43,0,0,162,163,3,16,8,0,163,164,5,44,0,0,164,29,1,0,0,0,165,
        166,5,20,0,0,166,167,5,43,0,0,167,168,3,16,8,0,168,169,5,44,0,0,
        169,31,1,0,0,0,170,171,7,6,0,0,171,33,1,0,0,0,172,173,5,13,0,0,173,
        174,5,43,0,0,174,179,3,36,18,0,175,176,5,45,0,0,176,178,3,36,18,
        0,177,175,1,0,0,0,178,181,1,0,0,0,179,177,1,0,0,0,179,180,1,0,0,
        0,180,182,1,0,0,0,181,179,1,0,0,0,182,183,5,44,0,0,183,35,1,0,0,
        0,184,187,5,48,0,0,185,187,3,16,8,0,186,184,1,0,0,0,186,185,1,0,
        0,0,187,37,1,0,0,0,188,189,5,6,0,0,189,190,5,43,0,0,190,191,3,16,
        8,0,191,192,5,44,0,0,192,202,3,4,2,0,193,194,5,7,0,0,194,195,5,6,
        0,0,195,196,5,43,0,0,196,197,3,16,8,0,197,198,5,44,0,0,198,199,3,
        4,2,0,199,201,1,0,0,0,200,193,1,0,0,0,201,204,1,0,0,0,202,200,1,
        0,0,0,202,203,1,0,0,0,203,207,1,0,0,0,204,202,1,0,0,0,205,206,5,
        7,0,0,206,208,3,4,2,0,207,205,1,0,0,0,207,208,1,0,0,0,208,39,1,0,
        0,0,209,210,5,8,0,0,210,211,5,43,0,0,211,212,3,16,8,0,212,213,5,
        44,0,0,213,214,3,4,2,0,214,41,1,0,0,0,215,216,5,9,0,0,216,217,3,
        4,2,0,217,218,5,10,0,0,218,219,5,43,0,0,219,220,5,49,0,0,220,221,
        5,44,0,0,221,222,3,4,2,0,222,43,1,0,0,0,10,47,60,66,108,122,124,
        179,186,202,207
    ]

class EVALParser ( Parser ):

    grammarFileName = "EVALParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'int'", "'float'", "'string'", "'bool'", 
                     "'const'", "'if'", "'else'", "'while'", "'try'", "'catch'", 
                     "'true'", "'false'", "'print'", "'cast'", "'pow'", 
                     "'sqrt'", "'min'", "'max'", "'round'", "'abs'", "'PI'", 
                     "'DAYS_IN_WEEK'", "'HOURS_IN_DAY'", "'YEAR'", "'+'", 
                     "'-'", "'*'", "'/'", "'%'", "'+='", "'-='", "'*='", 
                     "'/='", "'=='", "'!='", "'<'", "'>'", "'<='", "'>='", 
                     "'='", "'{'", "'}'", "'('", "')'", "','" ]

    symbolicNames = [ "<INVALID>", "INT", "FLOAT", "STRING_TYPE", "BOOL", 
                      "CONST", "IF", "ELSE", "WHILE", "TRY", "CATCH", "TRUE", 
                      "FALSE", "PRINT", "CAST", "POW", "SQRT", "MIN", "MAX", 
                      "ROUND", "ABS", "PI", "DAYS_IN_WEEK", "HOURS_IN_DAY", 
                      "YEAR", "PLUS", "MINUS", "MULTI", "DIVIDE", "MODULUS", 
                      "PLUS_ASSIGN", "MINUS_ASSIGN", "MULTI_ASSIGN", "DIV_ASSIGN", 
                      "EQ", "NEQ", "LT", "GT", "LTE", "GTE", "ASSIGN", "LBRACE", 
                      "RBRACE", "LPAREN", "RPAREN", "COMMA", "REAL", "INTEGER", 
                      "STRING", "IDENTIFIER", "WS", "LINE_COMMENT", "BLOCK_COMMENT" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_block = 2
    RULE_variableDeclaration = 3
    RULE_constDeclaration = 4
    RULE_assignment = 5
    RULE_assignOp = 6
    RULE_type = 7
    RULE_expression = 8
    RULE_castCall = 9
    RULE_powCall = 10
    RULE_sqrtCall = 11
    RULE_minCall = 12
    RULE_maxCall = 13
    RULE_roundCall = 14
    RULE_absCall = 15
    RULE_macroValue = 16
    RULE_printStatement = 17
    RULE_printArg = 18
    RULE_ifStatement = 19
    RULE_whileStatement = 20
    RULE_tryStatement = 21

    ruleNames =  [ "program", "statement", "block", "variableDeclaration", 
                   "constDeclaration", "assignment", "assignOp", "type", 
                   "expression", "castCall", "powCall", "sqrtCall", "minCall", 
                   "maxCall", "roundCall", "absCall", "macroValue", "printStatement", 
                   "printArg", "ifStatement", "whileStatement", "tryStatement" ]

    EOF = Token.EOF
    INT=1
    FLOAT=2
    STRING_TYPE=3
    BOOL=4
    CONST=5
    IF=6
    ELSE=7
    WHILE=8
    TRY=9
    CATCH=10
    TRUE=11
    FALSE=12
    PRINT=13
    CAST=14
    POW=15
    SQRT=16
    MIN=17
    MAX=18
    ROUND=19
    ABS=20
    PI=21
    DAYS_IN_WEEK=22
    HOURS_IN_DAY=23
    YEAR=24
    PLUS=25
    MINUS=26
    MULTI=27
    DIVIDE=28
    MODULUS=29
    PLUS_ASSIGN=30
    MINUS_ASSIGN=31
    MULTI_ASSIGN=32
    DIV_ASSIGN=33
    EQ=34
    NEQ=35
    LT=36
    GT=37
    LTE=38
    GTE=39
    ASSIGN=40
    LBRACE=41
    RBRACE=42
    LPAREN=43
    RPAREN=44
    COMMA=45
    REAL=46
    INTEGER=47
    STRING=48
    IDENTIFIER=49
    WS=50
    LINE_COMMENT=51
    BLOCK_COMMENT=52

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(EVALParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.StatementContext)
            else:
                return self.getTypedRuleContext(EVALParser.StatementContext,i)


        def getRuleIndex(self):
            return EVALParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = EVALParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 565148976685950) != 0):
                self.state = 44
                self.statement()
                self.state = 49
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 50
            self.match(EVALParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variableDeclaration(self):
            return self.getTypedRuleContext(EVALParser.VariableDeclarationContext,0)


        def constDeclaration(self):
            return self.getTypedRuleContext(EVALParser.ConstDeclarationContext,0)


        def assignment(self):
            return self.getTypedRuleContext(EVALParser.AssignmentContext,0)


        def printStatement(self):
            return self.getTypedRuleContext(EVALParser.PrintStatementContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(EVALParser.IfStatementContext,0)


        def whileStatement(self):
            return self.getTypedRuleContext(EVALParser.WhileStatementContext,0)


        def tryStatement(self):
            return self.getTypedRuleContext(EVALParser.TryStatementContext,0)


        def block(self):
            return self.getTypedRuleContext(EVALParser.BlockContext,0)


        def getRuleIndex(self):
            return EVALParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = EVALParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 60
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 52
                self.variableDeclaration()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 53
                self.constDeclaration()
                pass
            elif token in [49]:
                self.enterOuterAlt(localctx, 3)
                self.state = 54
                self.assignment()
                pass
            elif token in [13]:
                self.enterOuterAlt(localctx, 4)
                self.state = 55
                self.printStatement()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 5)
                self.state = 56
                self.ifStatement()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 6)
                self.state = 57
                self.whileStatement()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 7)
                self.state = 58
                self.tryStatement()
                pass
            elif token in [41]:
                self.enterOuterAlt(localctx, 8)
                self.state = 59
                self.block()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(EVALParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(EVALParser.RBRACE, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.StatementContext)
            else:
                return self.getTypedRuleContext(EVALParser.StatementContext,i)


        def getRuleIndex(self):
            return EVALParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = EVALParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(EVALParser.LBRACE)
            self.state = 66
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 565148976685950) != 0):
                self.state = 63
                self.statement()
                self.state = 68
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 69
            self.match(EVALParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(EVALParser.TypeContext,0)


        def IDENTIFIER(self):
            return self.getToken(EVALParser.IDENTIFIER, 0)

        def ASSIGN(self):
            return self.getToken(EVALParser.ASSIGN, 0)

        def expression(self):
            return self.getTypedRuleContext(EVALParser.ExpressionContext,0)


        def getRuleIndex(self):
            return EVALParser.RULE_variableDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableDeclaration" ):
                listener.enterVariableDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableDeclaration" ):
                listener.exitVariableDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableDeclaration" ):
                return visitor.visitVariableDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def variableDeclaration(self):

        localctx = EVALParser.VariableDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_variableDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self.type_()
            self.state = 72
            self.match(EVALParser.IDENTIFIER)
            self.state = 73
            self.match(EVALParser.ASSIGN)
            self.state = 74
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONST(self):
            return self.getToken(EVALParser.CONST, 0)

        def variableDeclaration(self):
            return self.getTypedRuleContext(EVALParser.VariableDeclarationContext,0)


        def getRuleIndex(self):
            return EVALParser.RULE_constDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstDeclaration" ):
                listener.enterConstDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstDeclaration" ):
                listener.exitConstDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstDeclaration" ):
                return visitor.visitConstDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def constDeclaration(self):

        localctx = EVALParser.ConstDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_constDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(EVALParser.CONST)
            self.state = 77
            self.variableDeclaration()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(EVALParser.IDENTIFIER, 0)

        def assignOp(self):
            return self.getTypedRuleContext(EVALParser.AssignOpContext,0)


        def expression(self):
            return self.getTypedRuleContext(EVALParser.ExpressionContext,0)


        def getRuleIndex(self):
            return EVALParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = EVALParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.match(EVALParser.IDENTIFIER)
            self.state = 80
            self.assignOp()
            self.state = 81
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ASSIGN(self):
            return self.getToken(EVALParser.ASSIGN, 0)

        def PLUS_ASSIGN(self):
            return self.getToken(EVALParser.PLUS_ASSIGN, 0)

        def MINUS_ASSIGN(self):
            return self.getToken(EVALParser.MINUS_ASSIGN, 0)

        def MULTI_ASSIGN(self):
            return self.getToken(EVALParser.MULTI_ASSIGN, 0)

        def DIV_ASSIGN(self):
            return self.getToken(EVALParser.DIV_ASSIGN, 0)

        def getRuleIndex(self):
            return EVALParser.RULE_assignOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignOp" ):
                listener.enterAssignOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignOp" ):
                listener.exitAssignOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignOp" ):
                return visitor.visitAssignOp(self)
            else:
                return visitor.visitChildren(self)




    def assignOp(self):

        localctx = EVALParser.AssignOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_assignOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1115617755136) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(EVALParser.INT, 0)

        def FLOAT(self):
            return self.getToken(EVALParser.FLOAT, 0)

        def STRING_TYPE(self):
            return self.getToken(EVALParser.STRING_TYPE, 0)

        def BOOL(self):
            return self.getToken(EVALParser.BOOL, 0)

        def getRuleIndex(self):
            return EVALParser.RULE_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType" ):
                listener.enterType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType" ):
                listener.exitType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)




    def type_(self):

        localctx = EVALParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 30) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return EVALParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class MinExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def minCall(self):
            return self.getTypedRuleContext(EVALParser.MinCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMinExpr" ):
                listener.enterMinExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMinExpr" ):
                listener.exitMinExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMinExpr" ):
                return visitor.visitMinExpr(self)
            else:
                return visitor.visitChildren(self)


    class CastExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def castCall(self):
            return self.getTypedRuleContext(EVALParser.CastCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCastExpr" ):
                listener.enterCastExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCastExpr" ):
                listener.exitCastExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCastExpr" ):
                return visitor.visitCastExpr(self)
            else:
                return visitor.visitChildren(self)


    class MacroExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def macroValue(self):
            return self.getTypedRuleContext(EVALParser.MacroValueContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMacroExpr" ):
                listener.enterMacroExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMacroExpr" ):
                listener.exitMacroExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacroExpr" ):
                return visitor.visitMacroExpr(self)
            else:
                return visitor.visitChildren(self)


    class SqrtExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def sqrtCall(self):
            return self.getTypedRuleContext(EVALParser.SqrtCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSqrtExpr" ):
                listener.enterSqrtExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSqrtExpr" ):
                listener.exitSqrtExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSqrtExpr" ):
                return visitor.visitSqrtExpr(self)
            else:
                return visitor.visitChildren(self)


    class RealLiteralContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def REAL(self):
            return self.getToken(EVALParser.REAL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRealLiteral" ):
                listener.enterRealLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRealLiteral" ):
                listener.exitRealLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRealLiteral" ):
                return visitor.visitRealLiteral(self)
            else:
                return visitor.visitChildren(self)


    class IntLiteralContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INTEGER(self):
            return self.getToken(EVALParser.INTEGER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntLiteral" ):
                listener.enterIntLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntLiteral" ):
                listener.exitIntLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntLiteral" ):
                return visitor.visitIntLiteral(self)
            else:
                return visitor.visitChildren(self)


    class AbsExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def absCall(self):
            return self.getTypedRuleContext(EVALParser.AbsCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAbsExpr" ):
                listener.enterAbsExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAbsExpr" ):
                listener.exitAbsExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbsExpr" ):
                return visitor.visitAbsExpr(self)
            else:
                return visitor.visitChildren(self)


    class TrueLiteralContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def TRUE(self):
            return self.getToken(EVALParser.TRUE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTrueLiteral" ):
                listener.enterTrueLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTrueLiteral" ):
                listener.exitTrueLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTrueLiteral" ):
                return visitor.visitTrueLiteral(self)
            else:
                return visitor.visitChildren(self)


    class AdditiveExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(EVALParser.ExpressionContext,i)

        def PLUS(self):
            return self.getToken(EVALParser.PLUS, 0)
        def MINUS(self):
            return self.getToken(EVALParser.MINUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveExpr" ):
                listener.enterAdditiveExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveExpr" ):
                listener.exitAdditiveExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpr" ):
                return visitor.visitAdditiveExpr(self)
            else:
                return visitor.visitChildren(self)


    class RelationalExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(EVALParser.ExpressionContext,i)

        def LT(self):
            return self.getToken(EVALParser.LT, 0)
        def GT(self):
            return self.getToken(EVALParser.GT, 0)
        def LTE(self):
            return self.getToken(EVALParser.LTE, 0)
        def GTE(self):
            return self.getToken(EVALParser.GTE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationalExpr" ):
                listener.enterRelationalExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationalExpr" ):
                listener.exitRelationalExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationalExpr" ):
                return visitor.visitRelationalExpr(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(EVALParser.LPAREN, 0)
        def expression(self):
            return self.getTypedRuleContext(EVALParser.ExpressionContext,0)

        def RPAREN(self):
            return self.getToken(EVALParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)


    class RoundExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def roundCall(self):
            return self.getTypedRuleContext(EVALParser.RoundCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoundExpr" ):
                listener.enterRoundExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoundExpr" ):
                listener.exitRoundExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoundExpr" ):
                return visitor.visitRoundExpr(self)
            else:
                return visitor.visitChildren(self)


    class MaxExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def maxCall(self):
            return self.getTypedRuleContext(EVALParser.MaxCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMaxExpr" ):
                listener.enterMaxExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMaxExpr" ):
                listener.exitMaxExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMaxExpr" ):
                return visitor.visitMaxExpr(self)
            else:
                return visitor.visitChildren(self)


    class IdentExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENTIFIER(self):
            return self.getToken(EVALParser.IDENTIFIER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentExpr" ):
                listener.enterIdentExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentExpr" ):
                listener.exitIdentExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentExpr" ):
                return visitor.visitIdentExpr(self)
            else:
                return visitor.visitChildren(self)


    class UnaryMinusExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def MINUS(self):
            return self.getToken(EVALParser.MINUS, 0)
        def expression(self):
            return self.getTypedRuleContext(EVALParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryMinusExpr" ):
                listener.enterUnaryMinusExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryMinusExpr" ):
                listener.exitUnaryMinusExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryMinusExpr" ):
                return visitor.visitUnaryMinusExpr(self)
            else:
                return visitor.visitChildren(self)


    class FalseLiteralContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FALSE(self):
            return self.getToken(EVALParser.FALSE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFalseLiteral" ):
                listener.enterFalseLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFalseLiteral" ):
                listener.exitFalseLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFalseLiteral" ):
                return visitor.visitFalseLiteral(self)
            else:
                return visitor.visitChildren(self)


    class StringLiteralContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(EVALParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringLiteral" ):
                listener.enterStringLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringLiteral" ):
                listener.exitStringLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringLiteral" ):
                return visitor.visitStringLiteral(self)
            else:
                return visitor.visitChildren(self)


    class PowExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def powCall(self):
            return self.getTypedRuleContext(EVALParser.PowCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPowExpr" ):
                listener.enterPowExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPowExpr" ):
                listener.exitPowExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPowExpr" ):
                return visitor.visitPowExpr(self)
            else:
                return visitor.visitChildren(self)


    class MultiplicativeExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(EVALParser.ExpressionContext,i)

        def MULTI(self):
            return self.getToken(EVALParser.MULTI, 0)
        def DIVIDE(self):
            return self.getToken(EVALParser.DIVIDE, 0)
        def MODULUS(self):
            return self.getToken(EVALParser.MODULUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeExpr" ):
                listener.enterMultiplicativeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeExpr" ):
                listener.exitMultiplicativeExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpr" ):
                return visitor.visitMultiplicativeExpr(self)
            else:
                return visitor.visitChildren(self)


    class EqualityExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EVALParser.ExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(EVALParser.ExpressionContext,i)

        def EQ(self):
            return self.getToken(EVALParser.EQ, 0)
        def NEQ(self):
            return self.getToken(EVALParser.NEQ, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEqualityExpr" ):
                listener.enterEqualityExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEqualityExpr" ):
                listener.exitEqualityExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEqualityExpr" ):
                return visitor.visitEqualityExpr(self)
            else:
                return visitor.visitChildren(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = EVALParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 16
        self.enterRecursionRule(localctx, 16, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [26]:
                localctx = EVALParser.UnaryMinusExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 88
                self.match(EVALParser.MINUS)
                self.state = 89
                self.expression(16)
                pass
            elif token in [43]:
                localctx = EVALParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 90
                self.match(EVALParser.LPAREN)
                self.state = 91
                self.expression(0)
                self.state = 92
                self.match(EVALParser.RPAREN)
                pass
            elif token in [14]:
                localctx = EVALParser.CastExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 94
                self.castCall()
                pass
            elif token in [15]:
                localctx = EVALParser.PowExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 95
                self.powCall()
                pass
            elif token in [16]:
                localctx = EVALParser.SqrtExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 96
                self.sqrtCall()
                pass
            elif token in [17]:
                localctx = EVALParser.MinExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 97
                self.minCall()
                pass
            elif token in [18]:
                localctx = EVALParser.MaxExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 98
                self.maxCall()
                pass
            elif token in [19]:
                localctx = EVALParser.RoundExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 99
                self.roundCall()
                pass
            elif token in [20]:
                localctx = EVALParser.AbsExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 100
                self.absCall()
                pass
            elif token in [21, 22, 23, 24]:
                localctx = EVALParser.MacroExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 101
                self.macroValue()
                pass
            elif token in [49]:
                localctx = EVALParser.IdentExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 102
                self.match(EVALParser.IDENTIFIER)
                pass
            elif token in [47]:
                localctx = EVALParser.IntLiteralContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 103
                self.match(EVALParser.INTEGER)
                pass
            elif token in [46]:
                localctx = EVALParser.RealLiteralContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 104
                self.match(EVALParser.REAL)
                pass
            elif token in [48]:
                localctx = EVALParser.StringLiteralContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 105
                self.match(EVALParser.STRING)
                pass
            elif token in [11]:
                localctx = EVALParser.TrueLiteralContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 106
                self.match(EVALParser.TRUE)
                pass
            elif token in [12]:
                localctx = EVALParser.FalseLiteralContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 107
                self.match(EVALParser.FALSE)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 124
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 122
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                    if la_ == 1:
                        localctx = EVALParser.EqualityExprContext(self, EVALParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 110
                        if not self.precpred(self._ctx, 20):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 20)")
                        self.state = 111
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==34 or _la==35):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 112
                        self.expression(21)
                        pass

                    elif la_ == 2:
                        localctx = EVALParser.RelationalExprContext(self, EVALParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 113
                        if not self.precpred(self._ctx, 19):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 19)")
                        self.state = 114
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1030792151040) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 115
                        self.expression(20)
                        pass

                    elif la_ == 3:
                        localctx = EVALParser.AdditiveExprContext(self, EVALParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 116
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 117
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==25 or _la==26):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 118
                        self.expression(19)
                        pass

                    elif la_ == 4:
                        localctx = EVALParser.MultiplicativeExprContext(self, EVALParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 119
                        if not self.precpred(self._ctx, 17):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 17)")
                        self.state = 120
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 939524096) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 121
                        self.expression(18)
                        pass

             
                self.state = 126
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class CastCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CAST(self):
            return self.getToken(EVALParser.CAST, 0)

        def LPAREN(self):
            return self.getToken(EVALParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(EVALParser.ExpressionContext,0)


        def COMMA(self):
            return self.getToken(EVALParser.COMMA, 0)

        def type_(self):
            return self.getTypedRuleContext(EVALParser.TypeContext,0)


        def RPAREN(self):
            return self.getToken(EVALParser.RPAREN, 0)

        def getRuleIndex(self):
            return EVALParser.RULE_castCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCastCall" ):
                listener.enterCastCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCastCall" ):
                listener.exitCastCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCastCall" ):
                return visitor.visitCastCall(self)
            else:
                return visitor.visitChildren(self)




    def castCall(self):

        localctx = EVALParser.CastCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_castCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            self.match(EVALParser.CAST)
            self.state = 128
            self.match(EVALParser.LPAREN)
            self.state = 129
            self.expression(0)
            self.state = 130
            self.match(EVALParser.COMMA)
            self.state = 131
            self.type_()
            self.state = 132
            self.match(EVALParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PowCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def POW(self):
            return self.getToken(EVALParser.POW, 0)

        def LPAREN(self):
            return self.getToken(EVALParser.LPAREN, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(EVALParser.ExpressionContext,i)


        def COMMA(self):
            return self.getToken(EVALParser.COMMA, 0)

        def RPAREN(self):
            return self.getToken(EVALParser.RPAREN, 0)

        def getRuleIndex(self):
            return EVALParser.RULE_powCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPowCall" ):
                listener.enterPowCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPowCall" ):
                listener.exitPowCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPowCall" ):
                return visitor.visitPowCall(self)
            else:
                return visitor.visitChildren(self)




    def powCall(self):

        localctx = EVALParser.PowCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_powCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 134
            self.match(EVALParser.POW)
            self.state = 135
            self.match(EVALParser.LPAREN)
            self.state = 136
            self.expression(0)
            self.state = 137
            self.match(EVALParser.COMMA)
            self.state = 138
            self.expression(0)
            self.state = 139
            self.match(EVALParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SqrtCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SQRT(self):
            return self.getToken(EVALParser.SQRT, 0)

        def LPAREN(self):
            return self.getToken(EVALParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(EVALParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(EVALParser.RPAREN, 0)

        def getRuleIndex(self):
            return EVALParser.RULE_sqrtCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSqrtCall" ):
                listener.enterSqrtCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSqrtCall" ):
                listener.exitSqrtCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSqrtCall" ):
                return visitor.visitSqrtCall(self)
            else:
                return visitor.visitChildren(self)




    def sqrtCall(self):

        localctx = EVALParser.SqrtCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_sqrtCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 141
            self.match(EVALParser.SQRT)
            self.state = 142
            self.match(EVALParser.LPAREN)
            self.state = 143
            self.expression(0)
            self.state = 144
            self.match(EVALParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MinCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MIN(self):
            return self.getToken(EVALParser.MIN, 0)

        def LPAREN(self):
            return self.getToken(EVALParser.LPAREN, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(EVALParser.ExpressionContext,i)


        def COMMA(self):
            return self.getToken(EVALParser.COMMA, 0)

        def RPAREN(self):
            return self.getToken(EVALParser.RPAREN, 0)

        def getRuleIndex(self):
            return EVALParser.RULE_minCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMinCall" ):
                listener.enterMinCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMinCall" ):
                listener.exitMinCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMinCall" ):
                return visitor.visitMinCall(self)
            else:
                return visitor.visitChildren(self)




    def minCall(self):

        localctx = EVALParser.MinCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_minCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 146
            self.match(EVALParser.MIN)
            self.state = 147
            self.match(EVALParser.LPAREN)
            self.state = 148
            self.expression(0)
            self.state = 149
            self.match(EVALParser.COMMA)
            self.state = 150
            self.expression(0)
            self.state = 151
            self.match(EVALParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MaxCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MAX(self):
            return self.getToken(EVALParser.MAX, 0)

        def LPAREN(self):
            return self.getToken(EVALParser.LPAREN, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(EVALParser.ExpressionContext,i)


        def COMMA(self):
            return self.getToken(EVALParser.COMMA, 0)

        def RPAREN(self):
            return self.getToken(EVALParser.RPAREN, 0)

        def getRuleIndex(self):
            return EVALParser.RULE_maxCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMaxCall" ):
                listener.enterMaxCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMaxCall" ):
                listener.exitMaxCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMaxCall" ):
                return visitor.visitMaxCall(self)
            else:
                return visitor.visitChildren(self)




    def maxCall(self):

        localctx = EVALParser.MaxCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_maxCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 153
            self.match(EVALParser.MAX)
            self.state = 154
            self.match(EVALParser.LPAREN)
            self.state = 155
            self.expression(0)
            self.state = 156
            self.match(EVALParser.COMMA)
            self.state = 157
            self.expression(0)
            self.state = 158
            self.match(EVALParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RoundCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ROUND(self):
            return self.getToken(EVALParser.ROUND, 0)

        def LPAREN(self):
            return self.getToken(EVALParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(EVALParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(EVALParser.RPAREN, 0)

        def getRuleIndex(self):
            return EVALParser.RULE_roundCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoundCall" ):
                listener.enterRoundCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoundCall" ):
                listener.exitRoundCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoundCall" ):
                return visitor.visitRoundCall(self)
            else:
                return visitor.visitChildren(self)




    def roundCall(self):

        localctx = EVALParser.RoundCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_roundCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 160
            self.match(EVALParser.ROUND)
            self.state = 161
            self.match(EVALParser.LPAREN)
            self.state = 162
            self.expression(0)
            self.state = 163
            self.match(EVALParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AbsCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ABS(self):
            return self.getToken(EVALParser.ABS, 0)

        def LPAREN(self):
            return self.getToken(EVALParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(EVALParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(EVALParser.RPAREN, 0)

        def getRuleIndex(self):
            return EVALParser.RULE_absCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAbsCall" ):
                listener.enterAbsCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAbsCall" ):
                listener.exitAbsCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbsCall" ):
                return visitor.visitAbsCall(self)
            else:
                return visitor.visitChildren(self)




    def absCall(self):

        localctx = EVALParser.AbsCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_absCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 165
            self.match(EVALParser.ABS)
            self.state = 166
            self.match(EVALParser.LPAREN)
            self.state = 167
            self.expression(0)
            self.state = 168
            self.match(EVALParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MacroValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PI(self):
            return self.getToken(EVALParser.PI, 0)

        def DAYS_IN_WEEK(self):
            return self.getToken(EVALParser.DAYS_IN_WEEK, 0)

        def HOURS_IN_DAY(self):
            return self.getToken(EVALParser.HOURS_IN_DAY, 0)

        def YEAR(self):
            return self.getToken(EVALParser.YEAR, 0)

        def getRuleIndex(self):
            return EVALParser.RULE_macroValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMacroValue" ):
                listener.enterMacroValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMacroValue" ):
                listener.exitMacroValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacroValue" ):
                return visitor.visitMacroValue(self)
            else:
                return visitor.visitChildren(self)




    def macroValue(self):

        localctx = EVALParser.MacroValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_macroValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 31457280) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PRINT(self):
            return self.getToken(EVALParser.PRINT, 0)

        def LPAREN(self):
            return self.getToken(EVALParser.LPAREN, 0)

        def printArg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.PrintArgContext)
            else:
                return self.getTypedRuleContext(EVALParser.PrintArgContext,i)


        def RPAREN(self):
            return self.getToken(EVALParser.RPAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(EVALParser.COMMA)
            else:
                return self.getToken(EVALParser.COMMA, i)

        def getRuleIndex(self):
            return EVALParser.RULE_printStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintStatement" ):
                listener.enterPrintStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintStatement" ):
                listener.exitPrintStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintStatement" ):
                return visitor.visitPrintStatement(self)
            else:
                return visitor.visitChildren(self)




    def printStatement(self):

        localctx = EVALParser.PrintStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_printStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 172
            self.match(EVALParser.PRINT)
            self.state = 173
            self.match(EVALParser.LPAREN)
            self.state = 174
            self.printArg()
            self.state = 179
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==45:
                self.state = 175
                self.match(EVALParser.COMMA)
                self.state = 176
                self.printArg()
                self.state = 181
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 182
            self.match(EVALParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(EVALParser.STRING, 0)

        def expression(self):
            return self.getTypedRuleContext(EVALParser.ExpressionContext,0)


        def getRuleIndex(self):
            return EVALParser.RULE_printArg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintArg" ):
                listener.enterPrintArg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintArg" ):
                listener.exitPrintArg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintArg" ):
                return visitor.visitPrintArg(self)
            else:
                return visitor.visitChildren(self)




    def printArg(self):

        localctx = EVALParser.PrintArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_printArg)
        try:
            self.state = 186
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 184
                self.match(EVALParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 185
                self.expression(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self, i:int=None):
            if i is None:
                return self.getTokens(EVALParser.IF)
            else:
                return self.getToken(EVALParser.IF, i)

        def LPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(EVALParser.LPAREN)
            else:
                return self.getToken(EVALParser.LPAREN, i)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(EVALParser.ExpressionContext,i)


        def RPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(EVALParser.RPAREN)
            else:
                return self.getToken(EVALParser.RPAREN, i)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.BlockContext)
            else:
                return self.getTypedRuleContext(EVALParser.BlockContext,i)


        def ELSE(self, i:int=None):
            if i is None:
                return self.getTokens(EVALParser.ELSE)
            else:
                return self.getToken(EVALParser.ELSE, i)

        def getRuleIndex(self):
            return EVALParser.RULE_ifStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)




    def ifStatement(self):

        localctx = EVALParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_ifStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
            self.match(EVALParser.IF)
            self.state = 189
            self.match(EVALParser.LPAREN)
            self.state = 190
            self.expression(0)
            self.state = 191
            self.match(EVALParser.RPAREN)
            self.state = 192
            self.block()
            self.state = 202
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 193
                    self.match(EVALParser.ELSE)
                    self.state = 194
                    self.match(EVALParser.IF)
                    self.state = 195
                    self.match(EVALParser.LPAREN)
                    self.state = 196
                    self.expression(0)
                    self.state = 197
                    self.match(EVALParser.RPAREN)
                    self.state = 198
                    self.block() 
                self.state = 204
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

            self.state = 207
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 205
                self.match(EVALParser.ELSE)
                self.state = 206
                self.block()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(EVALParser.WHILE, 0)

        def LPAREN(self):
            return self.getToken(EVALParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(EVALParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(EVALParser.RPAREN, 0)

        def block(self):
            return self.getTypedRuleContext(EVALParser.BlockContext,0)


        def getRuleIndex(self):
            return EVALParser.RULE_whileStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStatement" ):
                listener.enterWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStatement" ):
                listener.exitWhileStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStatement" ):
                return visitor.visitWhileStatement(self)
            else:
                return visitor.visitChildren(self)




    def whileStatement(self):

        localctx = EVALParser.WhileStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 209
            self.match(EVALParser.WHILE)
            self.state = 210
            self.match(EVALParser.LPAREN)
            self.state = 211
            self.expression(0)
            self.state = 212
            self.match(EVALParser.RPAREN)
            self.state = 213
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TryStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRY(self):
            return self.getToken(EVALParser.TRY, 0)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EVALParser.BlockContext)
            else:
                return self.getTypedRuleContext(EVALParser.BlockContext,i)


        def CATCH(self):
            return self.getToken(EVALParser.CATCH, 0)

        def LPAREN(self):
            return self.getToken(EVALParser.LPAREN, 0)

        def IDENTIFIER(self):
            return self.getToken(EVALParser.IDENTIFIER, 0)

        def RPAREN(self):
            return self.getToken(EVALParser.RPAREN, 0)

        def getRuleIndex(self):
            return EVALParser.RULE_tryStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTryStatement" ):
                listener.enterTryStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTryStatement" ):
                listener.exitTryStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTryStatement" ):
                return visitor.visitTryStatement(self)
            else:
                return visitor.visitChildren(self)




    def tryStatement(self):

        localctx = EVALParser.TryStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_tryStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 215
            self.match(EVALParser.TRY)
            self.state = 216
            self.block()
            self.state = 217
            self.match(EVALParser.CATCH)
            self.state = 218
            self.match(EVALParser.LPAREN)
            self.state = 219
            self.match(EVALParser.IDENTIFIER)
            self.state = 220
            self.match(EVALParser.RPAREN)
            self.state = 221
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[8] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 20)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 19)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 18)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 17)
         




