lexer grammar EVALLexer;

// ─── Type Keywords ────────────────────────────────────────────────────────────
INT         : 'int';
FLOAT       : 'float';
STRING_TYPE : 'string';
BOOL        : 'bool';
CONST       : 'const';

// ─── Control Flow ─────────────────────────────────────────────────────────────
IF          : 'if';
ELSE        : 'else';
FOR         : 'for';
WHILE       : 'while';
BREAK       : 'break';
CONTINUE    : 'continue';
RETURN      : 'return';
TRY         : 'try';
CATCH       : 'catch';

// ─── Null Literal ─────────────────────────────────────────────────────────────
NULL        : 'null';

// ─── Boolean Literals ─────────────────────────────────────────────────────────
TRUE        : 'true';
FALSE       : 'false';

// ─── Built-in Functions ───────────────────────────────────────────────────────
PRINT       : 'print';
CAST        : 'cast';
POW         : 'pow';
SQRT        : 'sqrt';
MIN         : 'min';
MAX         : 'max';
ROUND       : 'round';
ABS         : 'abs';

// ─── Built-in Macros / Constants ──────────────────────────────────────────────
PI           : 'PI';
DAYS_IN_WEEK : 'DAYS_IN_WEEK';
HOURS_IN_DAY : 'HOURS_IN_DAY';
YEAR         : 'YEAR';

// ─── Logical Operators ────────────────────────────────────────────────────────
// NOTE: AND/OR must come BEFORE their single-char counterparts (&, |) if those
//       are ever added; here they are safe at any position.
AND_OP      : '&&';
OR_OP       : '||';
NOT_OP      : '!';

// ─── Increment / Decrement ────────────────────────────────────────────────────
// NOTE: Must appear BEFORE PLUS and MINUS so '++' is not tokenised as two '+'
INCREMENT   : '++';
DECREMENT   : '--';

// ─── Compound Assignment Operators ────────────────────────────────────────────
// NOTE: Must appear BEFORE ASSIGN ('=') to avoid mis-tokenising '+=' as '+' '='
PLUS_ASSIGN  : '+=';
MINUS_ASSIGN : '-=';
MULTI_ASSIGN : '*=';
DIV_ASSIGN   : '/=';

// ─── Arithmetic Operators ─────────────────────────────────────────────────────
PLUS        : '+';
MINUS       : '-';
MULTI       : '*';
DIVIDE      : '/';
MODULUS     : '%';

// ─── Comparison Operators ─────────────────────────────────────────────────────
// NOTE: Two-char operators must come BEFORE their single-char prefixes
EQ          : '==';
NEQ         : '!=';
LTE         : '<=';
GTE         : '>=';
LT          : '<';
GT          : '>';

// ─── Assignment ───────────────────────────────────────────────────────────────
// NOTE: ASSIGN must come AFTER all compound/equality operators
ASSIGN      : '=';

// ─── Delimiters ───────────────────────────────────────────────────────────────
LBRACE      : '{';
RBRACE      : '}';
LPAREN      : '(';
RPAREN      : ')';
LBRACKET    : '[';
RBRACKET    : ']';
COMMA       : ',';
SEMICOLON   : ';';

// ─── Literals ─────────────────────────────────────────────────────────────────
// NOTE: REAL must come BEFORE INTEGER so '3.14' is not split into '3' '.' '14'
REAL        : [0-9]+ '.' [0-9]+;
INTEGER     : [0-9]+;

// ─── String Literal ───────────────────────────────────────────────────────────
STRING      : '"' ( ~["\\\r\n] | '\\' . )* '"';

// ─── Identifier ───────────────────────────────────────────────────────────────
// Must come AFTER all keywords so keywords are matched first.
fragment LETTER : [a-zA-Z_];
fragment DIGIT  : [0-9];
IDENTIFIER  : LETTER (LETTER | DIGIT)*;

// ─── Ignored Tokens ───────────────────────────────────────────────────────────
WS            : [ \t\r\n]+    -> skip;
LINE_COMMENT  : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT : '/*' .*? '*/' -> skip;