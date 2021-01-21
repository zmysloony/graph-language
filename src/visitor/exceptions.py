from antlr4 import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl


class ParsingException(Exception):
	def __init__(self, rule):
		if isinstance(rule, TerminalNodeImpl):
			self.line = rule.symbol.line
			self.column = rule.symbol.column
		elif isinstance(rule, ParserRuleContext):
			self.line = rule.stop.line
			self.column = rule.stop.column

		self.text = rule.getText()

	@property
	def name(self):
		return self.text

	def __str__(self):
		return '({}, {}): {}'.format(self.line, self.column, self.error_msg())

	def error_msg(self):
		return 'Undefined parsing error.'


class IdentifierNotDefined(ParsingException):
	def error_msg(self):
		return 'Identifier \'{}\' not defined.'.format(self.text)


class IncorrectType(ParsingException):
	def __init__(self, rule, actual_type=None, expected_types=None):
		super().__init__(rule)
		self.actual = actual_type
		self.expected = expected_types

	def actual_str(self):
		if self.actual:
			return ' ({})'.format(self.actual)
		else:
			return ''

	def expected_str(self):
		if self.expected:
			if isinstance(self.expected, (tuple, dict)):
				expected_str = self.expected[0]
				for item in self.expected[1:]:
					expected_str += ' or \'{}\''.format(item)
			else:
				expected_str = self.expected
			return ', expected to have type ({})'.format(expected_str)

	def error_msg(self):
		return 'Identifier \'{}\' is of incorrect type{}{}.'.format(self.name, self.actual_str(), self.expected_str())


class AttributeNotDefined(ParsingException):
	def __init__(self, rule, attr_name):
		super().__init__(rule)
		self.attr_name = attr_name

	def error_msg(self):
		return '\'{}\' does not contain attribute \'{}\'.'.format(self.name, self.attr_name)


class ListIndexError(ParsingException):
	def __init__(self, rule, index, max_index):
		super().__init__(rule)
		self.index = index
		self.max_index = max_index

	def error_msg(self):
		return 'Trying to access \'{}[{}]\', while it\'s last index is {}.'.format(self.name, self.index, self.max_index)


class AmbigiousJsonMember(ParsingException):
	def __init__(self, rule, member_name):
		super().__init__(rule)
		self.member_name = member_name

	def error_msg(self):
		return 'Ambigious JSON object member named \'{}\'.'.format(self.member_name)


class JsonAccessOnNonJsonVariable(ParsingException):
	def error_msg(self):
		return 'Trying to use JSON access on a non-JSON variable \'{}\'.'.format(self.name)


class IncorrectJsonMemberName(ParsingException):
	def error_msg(self):
		return 'Illegal JSON object member name \'{}\''.format(self.name)


class IllegalOperator(ParsingException):
	def __init__(self, rule, var_type, operator):
		super().__init__(rule)
		self.type = var_type
		self.operator = operator.text

	def error_msg(self):
		return 'Illegal operation \'{}\' on variable \'{}\'({}).'.format(self.operator, self.name, self.type)


class DuplicateIdentifier(ParsingException):
	def error_msg(self):
		return 'Duplicate identifier \'{}\' in a function definition.'.format(self.name)


class WrongArgumentCount(ParsingException):
	def __init__(self, rule, count, expected_count):
		super().__init__(rule)
		self.count = count
		self.expected = expected_count

	def error_msg(self):
		return 'Function \'{}\' expects {} arguments, {} given.'.format(self.name, self.expected, self.count)


class FunctionNotDefined(ParsingException):
	def error_msg(self):
		return 'Function \'{}\' not defined.'.format(self.name)