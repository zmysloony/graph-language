from antlr4.error.ErrorListener import ErrorListener


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