class ParsingException(Exception):
	def __init__(self, symbol):
		self.line = symbol.line
		self.column = symbol.column

	def error_msg(self, message):
		return '({}, {}): {}'.format(self.line, self.column, message)

	def __str__(self):
		return self.error_msg('Undefined parsing error.')


class IdentifierNotDefinedException(ParsingException):
	def __init__(self, symbol):
		super().__init__(symbol)
		self.name = symbol.text

	def __str__(self):
		return self.error_msg('Identifier \'{}\' not defined.'.format(self.name))


class IncorrectTypeException(ParsingException):
	def __init__(self, symbol, actual_type, expected_type=None):
		super().__init__(symbol)
		self.name = symbol.text
		self.actual = actual_type
		self.expected = expected_type

	def __str__(self):
		if self.expected:
			return self.error_msg('Identifer \'{}\' expected to have type \'{}\', got \'{}\' instead.'.format(
				self.name, self.expected, self.actual
			))
