import re

from antlr4.error.ErrorListener import ErrorListener, ConsoleErrorListener

from generated.glangLexer import glangLexer


def number_th(number):
	n = number % 10
	ths = {1: 'st', 2: 'nd', 3: 'rd'}
	chosen = ths.get(n)
	if chosen:
		return '{}-{}'.format(number, chosen)
	return '{}-th'.format(number)


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
		print('{}: "{}"'.format(glangLexer.symbolicNames[token.type], token.text))


class ParserErrorListener(ConsoleErrorListener):
	INSTANCE = None

	def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
		res = re.search(r"mismatched input '(.+)' expecting {(.+)}", msg)
		if res is not None:
			raise UnexpectedToken(line, column, res.group(1), res.group(2), recognizer)
		raise ParserSyntaxException(line, column, msg)


class LexerSyntaxException(Exception):
	def __init__(self, line, column, msg):
		self.line = line
		self.column = column
		self.msg = msg

	def __str__(self):
		return 'Lexer error ({}, {}): {}'.format(self.line, self.column, self.msg)


class ParserSyntaxException(LexerSyntaxException):
	def __str__(self):

		return 'Parser error ({}, {}): {}'.format(self.line, self.column, self.msg)


class UnexpectedToken(ParserSyntaxException):
	def __init__(self, line, column, token, expected_tokens, recognizer):
		expected_tokens = expected_tokens.split(', ')
		literal_expected_tokens = []
		for t in expected_tokens:
			if t[0] == t[-1] == '\'':
				literal_expected_tokens.append(t[1:-1])
				continue
			name = recognizer.literalNames[getattr(recognizer, t)]
			if name != '<INVALID>':
				literal_expected_tokens.append(name)
		msg = 'Unexpected token \'{}\''.format(token)
		if len(literal_expected_tokens) != 0:
			msg += ', expecting \'{}\''.format(literal_expected_tokens[0])
			for t in literal_expected_tokens[1:]:
				msg += ' or \'{}\''.format(t)
		msg += '.'
		super().__init__(line, column, msg)


class LexerErrorListener(ErrorListener):
	def __init__(self):
		super(LexerErrorListener, self).__init__()

	def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
		raise LexerSyntaxException(line, column, msg)

	def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
		raise Exception("Oh no!!")

	def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
		raise Exception("Oh no!!")

	def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
		raise Exception("Oh no!!")
