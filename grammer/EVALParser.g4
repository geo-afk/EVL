parser grammar EVALParser;

options { tokenVocab=EVALLexer; }

program
    : statement* EOF
    ;

// ═══════════════════════════════════════════════════════════════════════════════
//  STATEMENTS
//  A statement is one executable unit.  Adding new constructs here (for, match,
//  return …) only requires adding one alternative rather than touching a dozen
//  rules as before.
// ═══════════════════════════════════════════════════════════════════════════════

statement
    : variableDeclaration           // int x = 10
    | constDeclaration              // const int x = 10
    | assignment                    // x = 20  |  x += 5
    | printStatement                // print("hello", x)
    | ifStatement                   // if (cond) { ... } else { ... }
    | whileStatement                // while (cond) { ... }
    | tryStatement                  // try { ... } catch { ... }
    | block                         // bare { ... }
    ;

// ─── Grouped block ────────────────────────────────────────────────────────────

block
    : LBRACE statement* RBRACE
    ;


variableDeclaration
    : type IDENTIFIER ASSIGN expression
    ;

constDeclaration
    : CONST variableDeclaration
    ;

// ─── Reassignment / compound assignment ───────────────────────────────────────

assignment
    : IDENTIFIER assignOp expression
    ;

assignOp
    : ASSIGN
    | PLUS_ASSIGN
    | MINUS_ASSIGN
    | MULTI_ASSIGN
    | DIV_ASSIGN
    ;

// ─── Type names ───────────────────────────────────────────────────────────────

type
    : INT
    | FLOAT
    | STRING_TYPE
    | BOOL
    ;

// ═══════════════════════════════════════════════════════════════════════════════
//  EXPRESSIONS  (ordered by ascending precedence — ANTLR4 resolves ambiguity
//  by preferring alternatives listed first, so lower-precedence operators
//  appear first here and bind more loosely)
//
//  Precedence levels (lowest → highest):
//    1. Logical OR            ||
//    2. Logical AND           &&
//    3. Equality              ==  !=
//    4. Relational            <  >  <=  >=
//    5. Additive              +  -
//    6. Multiplicative        *  /  %
//    7. Unary                 -  !
//    8. Primary               literal, identifier, macro, function call, (expr)
// ═══════════════════════════════════════════════════════════════════════════════

expression
    // ── Logical ──────────────────────────────────────────────────────────────
    : expression OR  expression                                         # orExpr
    | expression AND expression                                         # andExpr

    // ── Equality ─────────────────────────────────────────────────────────────
    | expression op=(EQ | NEQ) expression                               # equalityExpr

    // ── Relational ───────────────────────────────────────────────────────────
    | expression op=(LT | GT | LTE | GTE) expression                   # relationalExpr

    // ── Additive ─────────────────────────────────────────────────────────────
    | expression op=(PLUS | MINUS) expression                           # additiveExpr

    // ── Multiplicative ───────────────────────────────────────────────────────
    | expression op=(MULTI | DIVIDE | MODULUS) expression               # multiplicativeExpr

    // ── Unary ────────────────────────────────────────────────────────────────
    | MINUS expression                                                   # unaryMinusExpr
    | NOT   expression                                                   # notExpr

    // ── Grouping ─────────────────────────────────────────────────────────────
    | LPAREN expression RPAREN                                          # parenExpr

    // ── Built-in function calls ───────────────────────────────────────────────
    | castCall                                                           # castExpr
    | powCall                                                            # powExpr
    | sqrtCall                                                           # sqrtExpr
    | minCall                                                            # minExpr
    | maxCall                                                            # maxExpr
    | roundCall                                                          # roundExpr
    | absCall                                                            # absExpr

    // ── Primaries ────────────────────────────────────────────────────────────
    | macroValue                                                         # macroExpr
    | IDENTIFIER                                                         # identExpr
    | INTEGER                                                            # intLiteral
    | REAL                                                               # realLiteral
    | STRING                                                             # stringLiteral
    | TRUE                                                               # trueLiteral
    | FALSE                                                              # falseLiteral
    ;

// ═══════════════════════════════════════════════════════════════════════════════
//  BUILT-IN FUNCTION CALLS
//  Arguments accept full expressions, not just bare identifiers — so
//  pow(x + 1, 2) or sqrt(100) are both valid.
// ═══════════════════════════════════════════════════════════════════════════════

castCall
    : CAST LPAREN expression COMMA type RPAREN
    ;

powCall
    : POW LPAREN expression COMMA expression RPAREN
    ;

sqrtCall
    : SQRT LPAREN expression RPAREN
    ;

minCall
    : MIN LPAREN expression COMMA expression RPAREN
    ;

maxCall
    : MAX LPAREN expression COMMA expression RPAREN
    ;

roundCall
    : ROUND LPAREN expression RPAREN
    ;

absCall
    : ABS LPAREN expression RPAREN
    ;

// ═══════════════════════════════════════════════════════════════════════════════
//  MACRO CONSTANTS
// ═══════════════════════════════════════════════════════════════════════════════

macroValue
    : PI
    | DAYS_IN_WEEK
    | HOURS_IN_DAY
    | YEAR
    ;

// ═══════════════════════════════════════════════════════════════════════════════
//  PRINT STATEMENT
// ═══════════════════════════════════════════════════════════════════════════════

printStatement
    : PRINT LPAREN printArg (COMMA printArg)* RPAREN
    ;

// A print argument is either a string literal or any expression
printArg
    : STRING
    | expression
    ;

// ═══════════════════════════════════════════════════════════════════════════════
//  CONTROL FLOW
// ═══════════════════════════════════════════════════════════════════════════════

ifStatement
    : IF LPAREN expression RPAREN block
      (ELSE IF LPAREN expression RPAREN block)*
      (ELSE block)?
    ;

whileStatement
    : WHILE LPAREN expression RPAREN block
    ;

// ─── Try / Catch ──────────────────────────────────────────────────────────────
// The catch block now accepts any number of statements, not just one print.

tryStatement
    : TRY block CATCH block
    ;
