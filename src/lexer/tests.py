from generated.src.glangLexer import glangLexer as gl
from src.utils import SyntaxException, assert_tokens
from src.tools import glex


def test_basic_math_ops():
	tokens = glex('100 + 12.12 - 00.23')
	assert_tokens(tokens, (gl.NUMBER, gl.PLUS, gl.NUMBER, gl.MINUS, gl.NUMBER))
	tokens = glex('(1234+4321) / 4')
	assert_tokens(tokens, (gl.L, gl.NUMBER, gl.PLUS, gl.NUMBER, gl.R, gl.DIV, gl.NUMBER))


def test_color_assignment():
	# color correct
	tokens = glex('red = #f01234')
	assert_tokens(tokens, (gl.IDENTIFIER, gl.ASSIGNMENT, gl.COLOR))
	# color too long
	tokens = glex('#f01234567f')
	assert_tokens(tokens, (gl.COLOR, (gl.NUMBER, '567'), (gl.IDENTIFIER, 'f')))


def test_chart_points_assignment():
	tokens = glex('b = [<\'First value\',20, red>, <\'Bigger value\', 40, blue>]')
	assert_tokens(tokens, (
		gl.IDENTIFIER, gl.ASSIGNMENT, gl.SQ_L, gl.LT, gl.STRING, gl.COMMA, gl.NUMBER, gl.COMMA, gl.IDENTIFIER,
		gl.GT, gl.COMMA, gl.LT, gl.STRING, gl.COMMA, gl.NUMBER, gl.COMMA, gl.IDENTIFIER, gl.GT, gl.SQ_R
	))


def test_unrecognized():
	try:
		tokens = glex('`')
	except SyntaxException:
		assert True
		return
	assert False
