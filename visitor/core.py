import collections

from antlr4 import ParserRuleContext

from gen.glangParser import glangParser
from gen.glangVisitor import glangVisitor
from visitor import helpers, types, exceptions
from visitor.helpers import VarTree, to_number_or_int

Var = collections.namedtuple('Var', 'value type context')


class GVisitor(glangVisitor):
	def __init__(self):
		super(glangVisitor, self).__init__()
		self.variables: VarTree = VarTree(ParserRuleContext())

	def enter_context(self, context: ParserRuleContext):
		self.variables = self.variables.enter(context)

	def exit_context(self):
		self.variables = self.variables.exit()

	def visitScript(self, ctx:glangParser.ScriptContext):
		self.variables = VarTree(ctx)
		self.visitChildren(ctx)

	def visitGenericIdentifier(self, ctx:glangParser.GenericIdentifierContext, create=False):
		if create:
			return self.variables.get_or_declare(ctx.IDENTIFIER())
		else:
			return self.variables.get(ctx.IDENTIFIER())

	def visitPropertyAccess(self, ctx:glangParser.PropertyAccessContext):
		try:
			return getattr(self.visit(ctx.identifier_ext()), ctx.IDENTIFIER())
		except AttributeError:
			raise exceptions.AttributeNotDefined(ctx.identifier_ext(), ctx.IDENTIFIER())

	def visitArrayAccess(self, ctx:glangParser.ArrayAccessContext):
		var = self.visit(ctx.identifier_ext())
		if var.type != types.LIST:
			raise exceptions.IncorrectType(ctx.identifier_ext(), var.type, types.LIST)
		number = to_number_or_int(ctx.NUMBER())
		if not isinstance(number, int):
			raise exceptions.IncorrectType(number, expected_types=types.INTEGER)
		try:
			return var.value[number]
		except IndexError:
			raise exceptions.ListIndexError(ctx.identifier_ext(), number, len(var.value))

	def visitL_value(self, ctx:glangParser.L_valueContext):
		identifier = ctx.identifier_ext()
		if isinstance(identifier, glangParser.GenericIdentifierContext):
			var = self.visitGenericIdentifier(identifier, True)
		else:
			var = self.visit(identifier)

		if ctx.COLOR_SIGN():
			if var.type in [types.DATA_POINT, types.NAMED_VALUE]:
				return var
			else:
				raise exceptions.IncorrectType(identifier, var.type, (types.DATA_POINT, types.NAMED_VALUE))
		return var

	def visitData_point(self, ctx:glangParser.Data_pointContext):
		return helpers.DataPoint(ctx.NUMBER(0), ctx.NUMBER(1))

	def visitData_point_colored(self, ctx:glangParser.Data_point_coloredContext):
		color = ctx.COLOR()
		if color:
			return helpers.DataPoint(ctx.NUMBER(0), ctx.NUMBER(1), color)
		return helpers.DataPoint(ctx.NUMBER(0), ctx.NUMBER(1), self.variables.get(ctx.IDENTIFIER()).value)

	def visitNamed_value(self, ctx:glangParser.Named_valueContext):
		return helpers.NamedValue(ctx.STRING(), ctx.NUMBER())

	def visitNamed_value_colored(self, ctx:glangParser.Named_value_coloredContext):
		color = ctx.COLOR()
		if color:
			return helpers.DataPoint(ctx.STRING(), ctx.NUMBER(), color)
		return helpers.DataPoint(ctx.STRING(), ctx.NUMBER(), self.variables.get(ctx.IDENTIFIER()).value)

	def visitAssignment(self, ctx:glangParser.AssignmentContext):
		self.visit(ctx.l_value()).value = self.visit(ctx.r_value())
