grammar glang;
// *****************************************************************************
// ************************   lexer rules    ***********************************
// *****************************************************************************
// functions, loops and special
DEF: 'def' ;
RETURN: 'return' ;
IF: 'if' ;
ELSE: 'else' ;
FOR: 'for' ;
J_STRING_MARKER: 'j' ;


// primitive data types
EMPTY_J_OBJECT: CURLY_L CURLY_R ;
EMPTY_ARRAY: SQ_L SQ_R ;
NULL: 'null' ;
TRUE: 'true' ;
FALSE: 'false' ;
NUMBER: ( DIGIT+ '.' DIGIT+ ) | INTEGER ;
INTEGER: DIGIT+ ;
STRING: '"' (CHAR | '\'' )+ '"' | '\'' (CHAR | '"')+ '\'' ;
COLOR: '#' HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL ;
IDENTIFIER: (LETTER | '_') (LETTER | DIGIT | '_')* ;


// operators
PLUS_EQ: '+=' ;
PLUS: '+' ;
MINUS_EQ: '--' ;
MINUS: '-' ;
DIV_EQ: '/=' ;
DIV: '/' ;
MUL_EQ: '*=' ;
ASSIGNMENT: '=' ;
MUL: '*' ;
DOT: '.' ;
COLOR_SIGN: '#' ;


// logic
EQ: '==' ;
NEQ: '!=' ;
LT: '<' ;
LTE: '<=' ;
GT: '>' ;
GTE: '>=' ;
AND: '&' ;
OR: '|' ;
NOT: '!' ;

// separators
COMMA: ',' ;
//NEWLINE: '\n' | '\r\n' ;
//TAB: '\t' ;
COLON: ':' ;
SC: ';' ;
L: '(' ;
R: ')' ;
SQ_L: '[' ;
SQ_R: ']' ;
CURLY_L: '{' ;
CURLY_R: '}' ;
DQUOT: '"' ;
QUOT: '\'' ;

fragment LETTER: [a-z] | [A-Z] ;
fragment DIGIT: [0-9] ;
fragment HEX_SYMBOL: [a-f] | [A-F] | [0-9] ;
fragment SYMBOL: '[' | ']' | '(' | ')' | '{' | '}' | '<' | '>' | '-' | '|' | '.' | ',' | ';' | '=' | '+' | '*' | '&' |
				  '^' | '%' | '$' | '#' | '@' | '!' | '?' | '/' | '~' ;
fragment CHAR: LETTER | DIGIT | '_' | WS | SYMBOL ;
WS: [ \r\n\t] + -> skip ;


// *****************************************************************************
// ************************   parser rules    **********************************
// *****************************************************************************
script: (function | sequential_code)* ;
array: EMPTY_ARRAY | (SQ_L (r_value_list | r_value) SQ_R) ;

// data types for charts
data_point: LT NUMBER COMMA NUMBER GT ;
data_point_colored: LT NUMBER COMMA NUMBER COMMA (COLOR | IDENTIFIER) GT ;
named_value: LT STRING COMMA NUMBER GT ;
named_value_colored: LT STRING COMMA NUMBER COMMA (COLOR | IDENTIFIER) GT ;

// json data type
j_value
: (j_object  | STRING | NUMBER | TRUE | FALSE | NULL)	#regularJValue
| (SQ_L j_value (COMMA j_value)* SQ_R)					#arrayJValue
;
j_member: IDENTIFIER SC j_value ;
j_object: EMPTY_J_OBJECT | ( CURLY_L j_member CURLY_R ) ;
j_string: J_STRING_MARKER (QUOT j_value QUOT) | (DQUOT j_value DQUOT) ;

// functions
id_list: (L R) | (L (IDENTIFIER COMMA)* IDENTIFIER R) ;
arg_list: (L R) | (L (r_value | r_value_list) R) ;
function: DEF IDENTIFIER id_list segment ;
function_call: IDENTIFIER arg_list ;

// loops
for_loop: FOR L operation? SC logical_expression SC operation? R segment ;

// conditionals
if_cond: IF L logical_expression R segment ;

// logical
logical_expression
: L logical_expression R											#parenExpression
| NOT logical_expression											#notExpression
| left=logical_expression op=comparator right=logical_expression	#comparatorExpression
| left=logical_expression op=binary right=logical_expression		#binaryExpression
| boolean															#boolExpression
| l_value															#identifierExpression
| NUMBER															#decimalExpression
;
comparator: GT | GTE | LT | LTE | EQ | NEQ;
binary: AND | OR ;
boolean: TRUE | FALSE ;

// math
math_expression
:   L math_expression R												#group
|   MINUS math_expression											#unaryMinus
|   left=math_expression op=(MUL | DIV)  right=math_expression		#mulDiv
|   left=math_expression op=(PLUS | MINUS) right=math_expression	#addSub
|   (NUMBER | IDENTIFIER)                           				#element
;

// r-value and l-value
// TODO add array access by integer identifier
identifier_ext
:	identifier_ext DOT IDENTIFIER			#propertyAccess
|	identifier_ext SQ_L NUMBER SQ_R			#arrayAccess
| 	IDENTIFIER								#genericIdentifier
;
l_value: COLOR_SIGN? identifier_ext ;
r_value_list: (r_value COMMA)+ r_value ;
r_value: IDENTIFIER | STRING | NUMBER | array | data_point | data_point_colored | named_value | named_value_colored
		  | logical_expression | math_expression | function_call | j_string | TRUE | FALSE | NULL | COLOR;

// operations
assignment: l_value ASSIGNMENT r_value ;
inplace_math_op: l_value op=(MINUS_EQ | PLUS_EQ | DIV_EQ | MUL_EQ) r_value ;
return_statement: RETURN r_value ;
operation: assignment | function_call | return_statement | inplace_math_op;
line_operation: operation SC ;
sequential_code: (line_operation | for_loop | if_cond)+ ;
segment: CURLY_L sequential_code? CURLY_R ;