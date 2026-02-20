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
WHILE       : 'while';
TRY         : 'try';
CATCH       : 'catch';

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
PI          : 'PI';
DAYS_IN_WEEK : 'DAYS_IN_WEEK';
HOURS_IN_DAY : 'HOURS_IN_DAY';
YEAR        : 'YEAR';

// ─── Arithmetic Operators ─────────────────────────────────────────────────────
PLUS        : '+';
MINUS       : '-';
MULTI       : '*';
DIVIDE      : '/';
MODULUS     : '%';

// ─── Compound Assignment Operators ────────────────────────────────────────────
PLUS_ASSIGN  : '+=';
MINUS_ASSIGN : '-=';
MULTI_ASSIGN : '*=';
DIV_ASSIGN   : '/=';

// ─── Comparison Operators ─────────────────────────────────────────────────────
EQ          : '==';
NEQ         : '!=';
LT          : '<';
GT          : '>';
LTE         : '<=';
GTE         : '>=';

// ─── Logical Operators ────────────────────────────────────────────────────────
AND         : '&&';
OR          : '||';
NOT         : '!';

// ─── Assignment ───────────────────────────────────────────────────────────────
// NOTE: ASSIGN must come AFTER compound operators and EQ to avoid mis-tokenising
ASSIGN      : '=';

// ─── Delimiters ───────────────────────────────────────────────────────────────
LBRACE      : '{';
RBRACE      : '}';
LPAREN      : '(';
RPAREN      : ')';
COMMA       : ',';

// ─── Literals ─────────────────────────────────────────────────────────────────
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
WS              : [ \t\r\n]+       -> skip;
LINE_COMMENT    : '//' ~[\r\n]*    -> skip;
BLOCK_COMMENT   : '/*' .*? '*/'   -> skip;
