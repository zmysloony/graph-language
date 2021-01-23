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


// primitive data types
EMPTY_ARRAY: SQ_L SQ_R ;
NULL: 'null' ;
TRUE: 'true' ;
FALSE: 'false' ;
NUMBER: ( DIGIT+ '.' DIGIT+ ) | INTEGER ;
INTEGER: DIGIT+ ;
STRING: QUOT (CHAR | DQUOT)*? QUOT;
DQUOT_STRING: DQUOT (CHAR | QUOT)*? DQUOT;
COLOR: '#' HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL HEX_SYMBOL ;
IDENTIFIER: (LETTER | '_') (LETTER | DIGIT | '_')* ;


// operators
PLUS_EQ: '+=' ;
PLUS: '+' ;
MINUS_EQ: '-=' ;
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
				  '^' | '%' | '$' | '#' | '@' | '!' | '?' | '/' | '~' | '"' ;
fragment CHAR: LETTER | DIGIT | '_' | WS | SYMBOL ;
WS: [ \r\n\t] + -> skip ;


// *****************************************************************************
// ************************   parser rules    **********************************
// *****************************************************************************
script: (function | sequential_code)* ;
array
: EMPTY_ARRAY	#emptyArray
| (SQ_L (r_value_list | r_value) SQ_R) #filledArray
;

// basic data types
string
: (STRING | DQUOT_STRING)												#regularString
| ((STRING PLUS math_expression) | (DQUOT_STRING PLUS math_expression))	#stringifiedMathExp
;
color: COLOR ;

// data types for charts
data_point: LT x=number COMMA y=number GT ;
data_point_colored: LT x=number COMMA y=number COMMA (color | identifier_ext) GT ;
named_value: LT label=string COMMA value=number GT ;
named_value_colored: LT label=string COMMA value=number COMMA (color | identifier_ext) GT ;

// json data type
j_value
: j_object																	#objectJValue
| (string | number | boolean | NULL)										#regularJValue
| (SQ_L j_value (COMMA j_value)* SQ_R)										#arrayJValue
| EMPTY_ARRAY																#emptyArrayJValue
;
j_member: string COLON j_value ;
j_object: ( CURLY_L (j_member (COMMA j_member)*)? CURLY_R ) ;

// functions
id_list: (L R) | (L (IDENTIFIER COMMA)* IDENTIFIER R) ;
arg_list: (L R) | (L r_value (COMMA r_value)* R) ;
function: DEF IDENTIFIER id_list segment ;
function_call: IDENTIFIER arg_list ;

// loops
for_loop: FOR L before=operation? SC logical_expression SC after=operation? R segment ;

// conditionals
if_cond: IF L logical_expression R segment ;


// math
number: math_expression ;
math_expression
:   L math_expression R												#groupMExpression
|	MINUS math_expression											#minusMExpression
|   left=math_expression op=mul_div right=math_expression			#mulDivMExpression
|   left=math_expression op=plus_minus right=math_expression		#addSubMExpression
|   identifier_ext	        			                   			#identifierMExpression
|	NUMBER															#numberMExpression
;
plus_minus: PLUS | MINUS ;
mul_div: MUL | DIV ;

// r-value and l-value
// TODO add array access by integer identifier
identifier_ext
:	identifier_ext DOT IDENTIFIER			#propertyAccess
|	identifier_ext DOT string				#jsonAccess
|	identifier_ext SQ_L NUMBER SQ_R			#arrayAccess
| 	IDENTIFIER								#genericIdentifier
;
l_value: COLOR_SIGN? identifier_ext ;
r_value_list: (r_value COMMA)+ r_value ; // TODO get rid of r_value_list
r_value
: (array | data_point | data_point_colored | named_value | named_value_colored | j_object | string | color)	#varRValue
| (COLOR_SIGN? identifier_ext)																#identifierRValue
| function_call																				#functionRValue
| (logical_expression | math_expression)													#evalRValue
| NULL																						#nullRValue
;

// logical
// TODO bool like in number->math_expression and use it everywhere

logical_expression
: L logical_expression R											#parenLExpression
| NOT logical_expression											#notLExpression
| left=logical_expression op=comparator right=logical_expression	#comparatorLExpression
| left=logical_expression op=binary right=logical_expression		#binaryLExpression
| boolean															#boolLExpression
| l_value															#identifierLExpression
| math_expression													#mathLExpression
;
comparator: GT | GTE | LT | LTE | EQ | NEQ;
binary: AND | OR ;
boolean: TRUE | FALSE ;

// operations
assignment: l_value ASSIGNMENT r_value ;
inplace_math_op: l_value op=(MINUS_EQ | PLUS_EQ | DIV_EQ | MUL_EQ) r_value ;
return_statement: RETURN r_value ;
operation: assignment | function_call | inplace_math_op;
line_operation: (operation SC) | (return_statement SC);
sequential_code: (line_operation | for_loop | if_cond)+ ;
segment: CURLY_L sequential_code? CURLY_R ;