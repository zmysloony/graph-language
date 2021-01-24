import pytest

from src.utils import UnexpectedToken, ParserSyntaxException
from . import types, exceptions
from ..tools import gparse


def parse_assert_value(code, value, v_type=None):
	v = gparse('a={};'.format(code))
	v.variables.assert_variable('a', value, v_type)


def test_color_assignment():
	parse_assert_value('#123458', '#123458', types.COLOR)
	parse_assert_value('#abcdef', '#abcdef', types.COLOR)
	parse_assert_value('#ff1230', '#ff1230', types.COLOR)
	with pytest.raises(exceptions.IncorrectType):
		gparse('a = 15; #a = #ff0000;')
	with pytest.raises(exceptions.IdentifierNotDefined):
		gparse('#a = #ff0000;')


def test_number_assignment():
	parse_assert_value('15', 15, types.NUMBER)
	parse_assert_value('-1', -1, types.NUMBER)
	parse_assert_value('0', 0, types.NUMBER)
	parse_assert_value('15.1', 15.1, types.NUMBER)
	parse_assert_value('0.0952', 0.0952, types.NUMBER)
	with pytest.raises(ParserSyntaxException):
		gparse('a=0,0952;')


def test_logical_expressions():
	parse_assert_value('1 > true;', False, types.BOOLEAN)
	parse_assert_value('125 > false', True, types.BOOLEAN)
	parse_assert_value('125 > 90 & 90 > 125 | !(125 > 90 & 90 > 125)', True, types.BOOLEAN)

	v = gparse('a = 125 > 90; b = 90 > 125; c = 125 > 90 & 90 > 125;')
	v.variables.assert_variable('a', True)
	v.variables.assert_variable('b', False)
	v.variables.assert_variable('c', False)

	parse_assert_value('(1 == true) & (0 == false) & (1 != 0) & (1 >= true) & (1 <= true)', True, types.BOOLEAN)


def test_math_expressions():
	parse_assert_value('1+1', 2, types.NUMBER)
	parse_assert_value('2-2', 0, types.NUMBER)
	parse_assert_value('3*3', 9, types.NUMBER)
	parse_assert_value('4/4', 1, types.NUMBER)
	parse_assert_value('12.1 + 0.909 + 11 - 2', 22.009, types.NUMBER)
	parse_assert_value('121/11', 11, types.NUMBER)
	parse_assert_value('121/-11', -11, types.NUMBER)
	parse_assert_value('-121/11', -11, types.NUMBER)
	parse_assert_value('123/15', 8.2, types.NUMBER)
	parse_assert_value('-5*(12-2)*0.21', -10.5, types.NUMBER)


def test_string_assignment():
	parse_assert_value('""', '', types.STRING)
	parse_assert_value('"b"', 'b', types.STRING)
	parse_assert_value('"test"', 'test', types.STRING)
	parse_assert_value('\'test\'', 'test', types.STRING)
	parse_assert_value('"a4AFh8a9sf09;FAU()[]\'{}-=)()(!&@$;"', 'a4AFh8a9sf09;FAU()[]\'{}-=)()(!&@$;', types.STRING)
	parse_assert_value('\'\'+1', '1', types.STRING)
	parse_assert_value('"abc"+123', 'abc123', types.STRING)
	parse_assert_value('"abc"+123*0.5+1', 'abc62.5', types.STRING)
	with pytest.raises(ParserSyntaxException):
		gparse('a="te"st";')


def test_data_points_and_named_values():
	v = gparse('a = <1,-1.01>; #a = #ff0000; b = <"test", -15, #ff0000>; #b = #00ff00;')
	assert v.variables.variables['a'].value.x.value == 1
	assert v.variables.variables['a'].value.x.type == types.NUMBER
	assert v.variables.variables['a'].value.y.value == -1.01
	assert v.variables.variables['a'].value.y.type == types.NUMBER
	assert v.variables.variables['a'].value.color.value == '#ff0000'
	assert v.variables.variables['a'].value.color.type == types.COLOR

	assert v.variables.variables['b'].value.label.value == 'test'
	assert v.variables.variables['b'].value.label.type == types.STRING
	assert v.variables.variables['b'].value.value.value == -15
	assert v.variables.variables['b'].value.value.type == types.NUMBER
	assert v.variables.variables['b'].value.color.value == '#00ff00'
	assert v.variables.variables['b'].value.color.type == types.COLOR


def test_property_access():
	with pytest.raises(exceptions.AttributeNotDefined):
		gparse('a = 12; b = a.color;')
	v = gparse('a = <1,-1,#ff0000>; b = a.color;')
	v.variables.assert_variable('b', '#ff0000', types.COLOR)


def test_array_access():
	v = gparse('a = [0,1,2,"test",3]; b = a[3];')
	v.variables.assert_variable('b', 'test')
	v = gparse('a = [0,1]; b = a[0 + 1];')
	v.variables.assert_variable('b', 1)
	v = gparse('a = [0,1]; b = a[a[0] + 1];')
	v.variables.assert_variable('b', 1)


def test_lists():
	v = gparse('b = 7; a = [<1,-1,#ff00ff>, 15, "test", b]; c = a[0].color;')
	assert v.variables.variables['a'].type == types.LIST
	assert v.variables.variables['a'].value[0].type == types.DATA_POINT
	assert v.variables.variables['a'].value[0].value.x.value == 1
	assert v.variables.variables['a'].value[0].value.x.type == types.NUMBER
	assert v.variables.variables['a'].value[0].value.y.value == -1
	assert v.variables.variables['a'].value[0].value.y.type == types.NUMBER
	assert v.variables.variables['a'].value[1].value == 15
	assert v.variables.variables['a'].value[1].type == types.NUMBER
	assert v.variables.variables['a'].value[2].value == 'test'
	assert v.variables.variables['a'].value[2].type == types.STRING
	assert v.variables.variables['a'].value[3].value == 7
	assert v.variables.variables['a'].value[3].type == types.NUMBER
	v.variables.assert_variable('c', '#ff00ff', types.COLOR)


def test_json_strings():
	gparse('a = {};')
	v = gparse('a = {"a": 12}; b = a.\'a\'; a."a" = 3;')
	assert v.variables.variables['a'].value['a'].value == 3
	assert v.variables.variables['b'].value == 12
	assert v.variables.variables['a'].value['a'].type == types.NUMBER
	v = gparse('a = {"a": [0, 1, 2, "test"]};')
	assert v.variables.variables['a'].value['a'].type == types.LIST
	assert v.variables.variables['a'].value['a'].value[0].value == 0
	assert v.variables.variables['a'].value['a'].value[0].type == types.NUMBER
	assert v.variables.variables['a'].value['a'].value[3].value == 'test'
	assert v.variables.variables['a'].value['a'].value[3].type == types.STRING
	with pytest.raises(UnexpectedToken):
		gparse('a = {test: 5};')


def test_inplace_operators():
	code_a = 'a = 2; a += 2; a -= 3; a *= 4; a /= 0.5;'
	code_b = 'b = "test"; b += "ing";'
	v = gparse(code_a)
	v.variables.assert_variable('a', 8, types.NUMBER)
	v = gparse(code_b)
	v.variables.assert_variable('b', 'testing', types.STRING)
	v = gparse(code_a + code_b + 'c = []; c += b; c += a + 2;')
	assert v.variables.variables['c'].value[0].value == 'testing'
	assert v.variables.variables['c'].value[0].type == types.STRING
	assert v.variables.variables['c'].value[1].value == 10
	assert v.variables.variables['c'].value[1].type == types.NUMBER
	with pytest.raises(exceptions.IncorrectType):
		gparse('a = ""; a += 2;')
	with pytest.raises(exceptions.IllegalOperator):
		gparse('a = {}; a += 2;')
		gparse('a = "test"; a -= "est";')


def test_if_conditional():
	v = gparse('a = 2; if(1==2){a += 3;}')
	v.variables.assert_variable('a', 2)
	v = gparse('a = 2; if(a==2){a += 3; b = 5; a += b;}')
	v.variables.assert_variable('a', 10)
	with pytest.raises(exceptions.IdentifierNotDefined):
		gparse('a = 2; if(a==2){a += 3; b = 5;} a += b;')


def test_for_loop():
	v = gparse('a = -2; for(a=4; a<=4; a+=1) { a = 7; }')
	v.variables.assert_variable('a', 8)
	v = gparse('a = 2; for(i=0; i<3; i+=1) { a *= a+i; }')
	v.variables.assert_variable('a', 2 * 2 * (2 * 2 + 1) * (2 * 2 * (2 * 2 + 1) + 2))
	v = gparse('a = []; for(i=0; i<3; i+=1) { for(j=0; j>-3; j-=1) { a += <i, j, #ff0000>; } }')
	assert v.variables.variables['a'].type == types.LIST
	for i in range(3):
		for j in range(-3):
			assert v.variables.variables['a'].value[i * 3 + j].type == types.DATA_POINT
			assert v.variables.variables['a'].value[i * 3 + j].value.x.value == i
			assert v.variables.variables['a'].value[i * 3 + j].value.y.value == -j
	with pytest.raises(exceptions.IdentifierNotDefined):
		gparse('a = 2; for(i=0; i<3; i+=1) { a *= a+i; } a = i;')


def test_function_definitions():
	# empty function
	v = gparse('def func(){}')
	assert v.functions['func'].arg_names == []

	# redefinition
	v = gparse('def func(){} def func(a,b,c){}')
	assert v.functions['func'].arg_names == ['a', 'b', 'c']

	# built-in function redefinition
	v = gparse('def pie(){ return "b";}')
	assert v.functions['pie']

	# function inside a function - incorrect
	with pytest.raises(ParserSyntaxException):
		gparse('def func(){ def other(){} }')


def test_function_calls():
	v = gparse('a = func(1,2,3); def func(a,b,c){return a+b+c;}')
	v.variables.assert_variable('a', 6)

	v = gparse('a = <-1,1,#ff0000>; func(a); def func(dataPoint){dataPoint.x=dataPoint.y; dataPoint.color=#0000ff;}')
	assert v.variables.variables['a'].value.x.value == 1
	assert v.variables.variables['a'].value.color.value == '#0000ff'

	# built-in function redefinition
	v = gparse('a=pie(); def pie(){ return "b";}')
	v.variables.assert_variable('a', 'b', types.STRING)

	with pytest.raises(exceptions.FunctionNotDefined):
		gparse('a();')


def test_builtins():
	v = gparse('pie([<"one", 1>, <"two", 4>, <"three", 9>], "test_title");')
	assert v.html and v.html is not None and v.html != ''
	v = gparse('bar([<"test", 15, #ff0000>], "test_title");')
	assert v.html and v.html is not None and v.html != ''
