import collections
import typing
from antlr4 import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

from visitor import exceptions


class Var:
	def __init__(self, value, value_type):
		self.value = value
		self.type = value_type


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

	def get(self, identifier, expected_types=None) -> Var:
		node, var = self, None
		while node:
			var = node.variables.get(identifier.symbol.text)
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


class DataPoint:
	def __init__(self, x, y, color=None):
		self.x, self.y, color = x, y, color


class NamedValue:
	def __init__(self, name, value, color=None):
		self.name, self.value, self.color = name, value, color


def to_number_or_int(node: TerminalNodeImpl):
	try:
		return int(node.symbol.text)
	except ValueError:
		try:
			return float(node.symbol.text)
		except ValueError:
			raise exceptions.ParsingException(node)
