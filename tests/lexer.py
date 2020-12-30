from antlr4 import InputStream

from gen.glangLexer import glangLexer as gl


def assert_tokens(tokens, types):
	for token, t in zip(tokens, types):
		if t is None:
			continue
		if isinstance(t, (tuple, list)):
			assert token.type == t[0]
			assert token.text == t[1]
		else:
			assert token.type == t


def print_tokens(tokens):
	for token in tokens:
		print('{}: "{}"'.format(gl.symbolicNames[token.type], token.text))


def glex(text):
	return gl(InputStream(text)).getAllTokens()


def test_numbers_integers():
	tokens = glex('1234 1234.52 0.55')
	assert_tokens(tokens, (gl.INTEGER, gl.NUMBER, gl.NUMBER))


def test_color_assignment():
	tokens = glex('red = #f01234')
	assert_tokens(tokens, (gl.IDENTIFIER, gl.ASSIGNMENT, gl.COLOR))


def test_color_too_long():
	tokens = glex('#f01234567f')
	assert_tokens(tokens, (gl.COLOR, (gl.INTEGER, '567'), (gl.IDENTIFIER, 'f')))


def test_chart_points_assignment():
	tokens = glex('b = [<\'First value\',20, red>, <\'Bigger value\', 40, blue>]')
	assert_tokens(tokens, (
		gl.IDENTIFIER, gl.ASSIGNMENT, gl.SQ_L, gl.LT, gl.STRING, gl.COMMA, gl.INTEGER, gl.COMMA, gl.IDENTIFIER,
		gl.GT, gl.COMMA, gl.LT, gl.STRING, gl.COMMA, gl.INTEGER, gl.COMMA, gl.IDENTIFIER, gl.GT, gl.SQ_R
	))


