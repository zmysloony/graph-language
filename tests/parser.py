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

