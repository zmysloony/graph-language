import collections
import typing

from gen.glangListener import glangListener
from gen.glangParser import glangParser
from listener import helpers, types, exceptions

Var = collections.namedtuple('Var', 'value type')


class Listener(glangListener):
	def __init__(self):
		super(glangListener, self).__init__()
		self.variables: typing.Dict[str, Var] = {}

	def get_variable(self, identifier, expected_type=None) -> Var:
		var = self.variables.get(identifier)
		if not var:
			raise exceptions.IdentifierNotDefinedException(identifier.symbol)
		if expected_type and var.type != expected_type:
			raise exceptions.IncorrectTypeException(identifier.symbol, var.type[1], expected_type)
		return var

	def enterScript(self, ctx:glangParser.ScriptContext):
		for child in ctx.getChildren():
			dir(child)

	def enterData_point(self, ctx:glangParser.Data_pointContext):
		return helpers.DataPoint(ctx.NUMBER(0), ctx.NUMBER(1))

	def enterData_point_colored(self, ctx:glangParser.Data_point_coloredContext):
		color = ctx.COLOR()
		if color:
			return helpers.DataPoint(ctx.NUMBER(0), ctx.NUMBER(1), color)
		return helpers.DataPoint(ctx.NUMBER(0), ctx.NUMBER(1), self.get_variable(ctx.IDENTIFIER()).value)

	def enterNamed_value(self, ctx:glangParser.Named_valueContext):
		return helpers.NamedValue(ctx.STRING(), ctx.NUMBER())

	def enterNamed_value_colored(self, ctx:glangParser.Named_value_coloredContext):
		color = ctx.COLOR()
		if color:
			return helpers.DataPoint(ctx.STRING(), ctx.NUMBER(), color)
		return helpers.DataPoint(ctx.STRING(), ctx.NUMBER(), self.get_variable(ctx.IDENTIFIER()).value)
