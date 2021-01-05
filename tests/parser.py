import pytest

from utils import gparse
from visitor import types, exceptions


def test_number_assignment():
	v = gparse('a = -1; b = 15; c = 0; d = 15.10; e = 0.992;')
	v.variables.assert_variable('a', -1, types.NUMBER)
	v.variables.assert_variable('b', 15, types.NUMBER)
	v.variables.assert_variable('c', 0, types.NUMBER)
	v.variables.assert_variable('d', 15.1, types.NUMBER)
	v.variables.assert_variable('e', 0.992, types.NUMBER)


def test_string_assignment():
	v = gparse('a = "test"; b = \'test\'; c = "a4AFh8a9sf09;FAU()[]\'{}-=)()(!&@$";')
	v.variables.assert_variable('a', 'test', types.STRING)
	v.variables.assert_variable('b', 'test', types.STRING)
	v.variables.assert_variable('c', 'a4AFh8a9sf09;FAU()[]\'{}-=)()(!&@$', types.STRING)


def test_logical_expressions():
	v = gparse('a = 1 > true;')
	v.variables.assert_variable('a', False, types.BOOLEAN)
	v = gparse('a = 125 > false;')
	v.variables.assert_variable('a', True, types.BOOLEAN)
	v = gparse('a = 125 > 90 & 90 > 125 | !(125 > 90 & 90 > 125);')
	v.variables.assert_variable('a', True, types.BOOLEAN)
	v = gparse('a = (1 == true) & (0 == false) & (1 != 0) & (1 >= true) & (1 <= true);')
	v.variables.assert_variable('a', True, types.BOOLEAN)


def test_math_expressions():
	v = gparse('a = 12.1 + 0.909 + 11 - 2;')
	v.variables.assert_variable('a', 22.009)
	v = gparse('a = 121 / 11;')
	v.variables.assert_variable('a', 11)
	v = gparse('a = 121 / -11;')
	v.variables.assert_variable('a', -11)
	v = gparse('a = 123 / 15;')
	v.variables.assert_variable('a', 8.2)
	v = gparse('a = -5*(12-2)*0.21;')
	v.variables.assert_variable('a', -10.5)


def test_color_assignment_with_new_variable():
	with pytest.raises(exceptions.IncorrectType):
		gparse('#a = #ff0000;')


def test_color_assignment_with_wrong_type_variable():
	with pytest.raises(exceptions.IncorrectType):
		gparse('a = 15; #a = #ff0000;')


def test_correct_color_assignment():
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