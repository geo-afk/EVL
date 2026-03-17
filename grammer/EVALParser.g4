parser grammar EVALParser;

options { tokenVocab=EVALLexer; }


program
    : statement* EOF
    ;

// ═══════════════════════════════════════════════════════════════════════════════
//  STATEMENTS
// ═══════════════════════════════════════════════════════════════════════════════

statement
    : variableDeclaration           // int x = 10
    | constDeclaration              // const int x = 10
    | assignment                    // x = 20  |  x += 5
    | ifStatement                   // if (cond) { ... } else { ... }
    | whileStatement                // while (cond) { ... }
    | tryStatement                  // try { ... } catch(e) { ... }
    | breakStatement                // break
    | continueStatement             // continue
    | builtinCallStatement          // standalone built-in call, e.g. print(...)
    | block                         // bare { ... }
    ;

// ─── Grouped block ────────────────────────────────────────────────────────────

block
    : LBRACE statement* RBRACE
    ;

// ─── Variable / Const declarations ───────────────────────────────────────────

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


breakStatement
    : BREAK
    ;

continueStatement
    : CONTINUE
    ;

// ─── Type names ───────────────────────────────────────────────────────────────

type
    : INT
    | FLOAT
    | STRING_TYPE
    | BOOL
    ;

// ═══════════════════════════════════════════════════════════════════════════════
//  EXPRESSIONS  (ordered by ascending precedence)
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
//
//  ANTLR4 resolves left-recursive ambiguity by favouring the earlier alternative
//  so lower-precedence operators appear first.
// ═══════════════════════════════════════════════════════════════════════════════

expression
    // ── Level 1 – Logical OR ─────────────────────────────────────────────────
    : expression OR_OP expression                                        # logicalOrExpr

    // ── Level 2 – Logical AND ────────────────────────────────────────────────
    | expression AND_OP expression                                       # logicalAndExpr

    // ── Level 3 – Equality ───────────────────────────────────────────────────
    | expression op=(EQ | NEQ) expression                               # equalityExpr

    // ── Level 4 – Relational ─────────────────────────────────────────────────
    | expression op=(LT | GT | LTE | GTE) expression                   # relationalExpr

    // ── Level 5 – Additive ───────────────────────────────────────────────────
    | expression op=(PLUS | MINUS) expression                           # additiveExpr

    // ── Level 6 – Multiplicative ─────────────────────────────────────────────
    | expression op=(MULTI | DIVIDE | MODULUS) expression               # multiplicativeExpr

    // ── Level 7 – Unary ──────────────────────────────────────────────────────
    | MINUS expression                                                   # unaryMinusExpr
    | NOT_OP expression                                                  # unaryNotExpr

    // ── Level 8 – Grouping ───────────────────────────────────────────────────
    | LPAREN expression RPAREN                                          # parenExpr

    // ── Built-in function calls ───────────────────────────────────────────────
    | builtinFunc                                                        # builtinExpr

    // ── Primaries ────────────────────────────────────────────────────────────
    | macroValue                                                         # macroExpr
    | IDENTIFIER                                                         # identExpr
    | INTEGER                                                            # intLiteral
    | REAL                                                               # realLiteral
    | STRING                                                             # stringLiteral
    | TRUE                                                               # trueLiteral
    | FALSE                                                              # falseLiteral
    | NULL                                                               # nullLiteral
    ;

// ═══════════════════════════════════════════════════════════════════════════════
//  BUILT-IN FUNCTIONS
//  Separated into builtinFunc (usable inside expressions) and
//  builtinCallStatement (when used as a bare statement so the parser does not
//  need to consider every expression as a potential statement, which would
//  require an expressionStatement rule and risk introducing new ambiguities).
// ═══════════════════════════════════════════════════════════════════════════════

builtinFunc
    : castCall
    | powCall
    | sqrtCall
    | minCall
    | maxCall
    | roundCall
    | absCall
    ;

// builtinCallStatement allows print (and any future void built-ins) to appear
// as a standalone statement WITHOUT making every expression a valid statement.
builtinCallStatement
    : printStatement
    ;

// ─── Individual call rules ────────────────────────────────────────────────────

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
//
//  FIX: The original rule had `STRING | expression` which caused an ambiguity
//  because `expression` already includes a `stringLiteral` alternative.  The
//  STRING-specific alternative has been removed; everything goes through
//  expression, which covers STRING via the stringLiteral labelled alternative.
// ═══════════════════════════════════════════════════════════════════════════════

printStatement
    : PRINT LPAREN printArg (COMMA printArg)* RPAREN
    ;

// FIX: removed standalone STRING alternative — expression already handles it.
printArg
    : expression
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

tryStatement
    : TRY block CATCH LPAREN IDENTIFIER RPAREN block
    ;