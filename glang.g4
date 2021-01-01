grammar glang;
// operators
PROP_ACCESS : '.' ;
ASSIGNMENT : '=' ;
PLUS : '+' ;
MINUS : '-' ;
INCREMENT : '++' ;
DECREMENT : '--' ;
DIV : '/' ;
MUL : '*' ;
EQ : '==' ;
NEQ : '!=' ;
LT : '<' ;
LTE : '<=' ;
GT : '>' ;
GTE : '>=' ;
AND : '&' ;
OR : '|' ;


// separators
COMMA : ',' ;
NEWLINE : '\n' | '\r\n' ;
TAB : '\t' ;
COLON : ':' ;
SEMICOLON : ';' ;
L : '(' ;
R : ')' ;
SQ_L : '[' ;
SQ_R : ']' ;
CURLY_L : '{' ;
CURLY_R : '}' ;


// functions and loops
DEF : 'def' ;
RETURN : 'return' ;
IF : 'if' ;
ELSE : 'else' ;
FOR : 'for' ;


// primitive data types
EMPTY_J_OBJECT : CURLY_L CURLY_R ;
NULL : 'null' ;
TRUE : 'true' ;
FALSE : 'false' ;
INTEGER : DIGIT+ ;
NUMBER : ( DIGIT+ '.' DIGIT+ ) | INTEGER ;
STRING : '"' (CHAR | '\'' )+ '"' | '\'' (CHAR | '"')+ '\'' ;
COLOR : '#' HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL ;

IDENTIFIER : (LETTER | '_') (LETTER | DIGIT | '_')* ;

fragment LETTER : [a-z] | [A-Z] ;
fragment DIGIT : [0-9] ;
fragment HEX_SYMBOL : [a-f] | [A-F] | [0-9] ;
fragment SYMBOL : '[' | ']' | '(' | ')' | '{' | '}' | '<' | '>' | '-' | '|' | '.' | ',' | ';' | '=' | '+' | '*' | '&' |
				  '^' | '%' | '$' | '#' | '@' | '!' | '?' | '/' | '~' ;
fragment CHAR : LETTER | DIGIT | '_' | WS | SYMBOL ;
WS : (' ')+ -> skip ;

//DATA_POINT : '<' (STRING | NUMBER) ',' NUMBER '>' ;
//DATA_POINT_W_COLOR : '<' (STRING | NUMBER) ',' NUMBER ',' (COLOR | IDENTIFIER) '>' ;

// json data type
//j_value : j_object | array | STRING | NUMBER | TRUE | FALSE | NULL ;
//j_element :  J_VALUE ;
//j_member : IDENTIFIER SC j_element ;
//j_object : EMPTY_J_OBJECT | ( CURLY_L j_member CURLY_R ) ;

test : IDENTIFIER ;