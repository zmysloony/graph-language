import antlr4
from antlr4 import InputStream
from antlr4.error.ErrorListener import ErrorListener

from gen.glangLexer import glangLexer
from gen.glangParser import glangParser
from visitor.core import GVisitor


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


def glex(text, return_lexer=False):
	lexer = glangLexer(InputStream(text))
	lexer.removeErrorListeners()
	lexer._listeners = [LexerErrorListener()]
	if return_lexer:
		return lexer
	return lexer.getAllTokens()


def gparse(text, return_visitor=True):
	lexer = glex(text, return_lexer=True)
	stream = antlr4.CommonTokenStream(lexer)
	parser = glangParser(stream)
	tree = parser.script()
	visitor = GVisitor()
	visitor.visit(tree)
	if return_visitor:
		return visitor


class LexerSyntaxException(Exception):
	def __init__(self, offending, line, column, msg):
		self.offending = offending
		self.line = line
		self.column = column
		self.msg = msg

	def __str__(self):
		return '({}, {}): {}'.format(self.line, self.column, self.msg)


class LexerErrorListener(ErrorListener):
	def __init__(self):
		super(LexerErrorListener, self).__init__()

	def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
		raise LexerSyntaxException(offendingSymbol, line, column, msg)

	def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
		raise Exception("Oh no!!")

	def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
		raise Exception("Oh no!!")

	def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
		raise Exception("Oh no!!")