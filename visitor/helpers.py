import collections
import typing
from antlr4 import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

from visitor import exceptions, types


class Var:
	def __init__(self, value, value_type):
		self.value = value
		self.type = value_type

	def __str__(self):
		return 'value: {}, type: {}'.format(self.value, self.type)


class VarTree:
	def __init__(self, context: ParserRuleContext, parent=None):
		self.parent = parent
		self.context = context
		self.variables: typing.Dict[str, Var] = {}

	def enter(self, context: ParserRuleContext):
		return VarTree(context, parent=self)

	def exit(self):
		return self.parent

	def declare(self, identifier) -> Var:
		"""Resets the variable if it exists, if not - creates an empty one."""
		return self.set(identifier, None, None)

	def get(self, identifier, expected_types=None, raw_text_identifier=False) -> Var:
		node, var = self, None
		id_text = identifier if raw_text_identifier else identifier.symbol.text
		while node:
			var = node.variables.get(id_text)
			if var:
				break
			node = node.exit()
		if not var:
			raise exceptions.IdentifierNotDefined(identifier)
		if expected_types and var.type not in expected_types:
			raise exceptions.IncorrectType(identifier, var.type, expected_types)
		return var

	def get_or_declare(self, identifier) -> Var:
		try:
			return self.get(identifier)
		except exceptions.ParsingException:
			return self.declare(identifier)

	def set(self, identifier, value, value_type) -> Var:
		node = self
		while node:		# try to find the value in parent nodes
			if node.variables.get(identifier.symbol.text):
				break
			node = node.exit()
		node = node if node else self
		node.variables[identifier.symbol.text] = Var(value, value_type)
		return node.variables[identifier.symbol.text]

	def assert_variable(self, identifier, value=None, value_type=None):
		var = self.get(identifier, raw_text_identifier=True)
		if value is not None:
			assert var.value == value
		if value_type is not None:
			assert var.type == value_type


class DataPoint:
	def __init__(self, x, y, color=None):
		self.x, self.y, self.color = x, y, color if color else Var(None, types.COLOR)

	def __str__(self):
		return '<{}, {}, {}>'.format(self.x.value, self.y.value, self.color.value)


class NamedValue:
	def __init__(self, label, value, color=None):
		self.label, self.value, self.color = label, value, color if color else Var(None, types.COLOR)

	def __str__(self):
		return '<{}, {}, {}>'.format(self.label.value, self.value.value, self.color.value)


def to_number_or_int(node: TerminalNodeImpl):
	try:
		return int(node.symbol.text)
	except ValueError:
		try:
			return float(node.symbol.text)
		except ValueError:
			raise exceptions.ParsingException(node)
