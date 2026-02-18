lexer grammar EVLLEXER;

// Keywords
INT : 'int';
FLOAT : 'float';
PRINT : 'print';
CONST : 'const';
DAYS_IN_WEEK : 'DAYS_IN_WEEK';
HOURS_IN_DAY : 'HOURS_IN_DAY';
YEAR: 'YEAR';
POW: 'pow';
CAST : 'cast';
SQRT: 'sqrt';
MIN: 'min';
MAX: 'max';
ROUND: 'round';
TRY : 'try';
CATCH : 'catch';

ASSIGN : '=' ;

// Operators
PLUS : '+';
MUNUS : '-';
MULTI : '*' ;
DIVIDE : '/' ;
MODULUS : '%';
LPARAN : '(';
RPARAN : ')';



// Delimiters
LBRACE : '{';
RBRACE : '}';



// Numbers
INTEGER : '-'? [0-9]+;
REAL : '-'? [0-9]+ '.' [0-9]+ ;


IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]*;

// Whitespace and comments
WS : [ \t\r\n]+ -> skip;

LINE_COMMENT : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT : '/*' .*? '*/' -> skip;