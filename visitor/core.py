import collections

from antlr4 import ParserRuleContext

from gen.glangParser import glangParser
from gen.glangVisitor import glangVisitor
from visitor import helpers, types, exceptions
from visitor.helpers import VarTree, to_number_or_int, Var


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

	def visitFunction(self, ctx:glangParser.FunctionContext):
		#TODO
		pass

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

	def visitL_value(self, ctx:glangParser.L_valueContext, create=False):
		identifier = ctx.identifier_ext()
		if isinstance(identifier, glangParser.GenericIdentifierContext):
			var = self.visitGenericIdentifier(identifier, create)
		else:
			var = self.visit(identifier)

		if ctx.COLOR_SIGN():
			if var.type in [types.DATA_POINT, types.NAMED_VALUE]:
				return var.value.color
			else:
				raise exceptions.IncorrectType(identifier, var.type, (types.DATA_POINT, types.NAMED_VALUE))
		return var

	def visitData_point(self, ctx:glangParser.Data_pointContext):
		return Var(helpers.DataPoint(self.visit(ctx.x), self.visit(ctx.y)), types.DATA_POINT)

	def visitData_point_colored(self, ctx:glangParser.Data_point_coloredContext):
		if ctx.color():
			var = helpers.DataPoint(self.visit(ctx.x), self.visit(ctx.y), self.visit(ctx.color()))
		else:
			var = helpers.DataPoint(self.visit(ctx.x), self.visit(ctx.y), self.visit(ctx.identifier_ext()))
		return Var(var, types.DATA_POINT)

	def visitNamed_value(self, ctx:glangParser.Named_valueContext):
		return Var(helpers.NamedValue(self.visit(ctx.label), self.visit(ctx.value)), types.NAMED_VALUE)

	def visitNamed_value_colored(self, ctx:glangParser.Named_value_coloredContext):
		if ctx.color():
			var = helpers.NamedValue(self.visit(ctx.label), self.visit(ctx.value), self.visit(ctx.color()))
		else:
			var = helpers.NamedValue(self.visit(ctx.label), self.visit(ctx.value), self.visit(ctx.identifier_ext()))
		return Var(var, types.NAMED_VALUE)

	def visitAssignment(self, ctx:glangParser.AssignmentContext):
		l_var = self.visitL_value(ctx.l_value(), True)
		r_var = self.visit(ctx.r_value())
		l_var.value = r_var.value
		l_var.type = r_var.type

	def visitBoolean(self, ctx:glangParser.BooleanContext):
		if ctx.TRUE():
			return 'True'
		return 'False'

	def visitString(self, ctx:glangParser.StringContext):
		return Var(ctx.STRING().getText()[1:-1], types.STRING)

	def visitColor(self, ctx:glangParser.ColorContext):
		return Var(ctx.COLOR().getText(), types.COLOR)

	def visitNumber(self, ctx:glangParser.NumberContext):
		return Var(to_number_or_int(ctx.NUMBER()), types.NUMBER)

	def visitDecimalLExpression(self, ctx:glangParser.DecimalLExpressionContext):
		return ctx.getText()

	def visitIdentifierLExpression(self, ctx:glangParser.IdentifierLExpressionContext):
		var = self.visitL_value(ctx.l_value(), False)
		if var.type in (types.BOOLEAN, types.NUMBER):
			return var.value
		raise exceptions.IncorrectType(ctx.l_value(), var.type, (types.BOOLEAN, types.NUMBER))

	def visitBinary(self, ctx:glangParser.BinaryContext):
		return ctx.getText()

	def visitBinaryLExpression(self, ctx:glangParser.BinaryLExpressionContext):
		return '{}{}{}'.format(self.visit(ctx.left), self.visit(ctx.op), self.visit(ctx.right))

	def visitComparator(self, ctx:glangParser.ComparatorContext):
		return ctx.getText()

	def visitComparatorLExpression(self, ctx:glangParser.ComparatorLExpressionContext):
		return '{}{}{}'.format(self.visit(ctx.left), self.visit(ctx.op), self.visit(ctx.right))

	def visitParenLExpression(self, ctx:glangParser.ParenLExpressionContext):
		return '({})'.format(self.visit(ctx.logical_expression()))

	def visitNotLExpression(self, ctx:glangParser.NotLExpressionContext):
		return '~' + self.visit(ctx.logical_expression())

	def visitNullRValue(self, ctx:glangParser.NullRValueContext):
		return Var(None, None)

	def visitEvalRValue(self, ctx:glangParser.EvalRValueContext):
		expr = self.visit(ctx.logical_expression()) if ctx.logical_expression() else self.visit(ctx.math_expression())
		expr_type = types.BOOLEAN if ctx.logical_expression() else types.NUMBER
		return Var(eval(expr), expr_type)

	def visitFunctionRValue(self, ctx:glangParser.FunctionRValueContext):
		# TODO
		pass

	def visitIdentifierRValue(self, ctx:glangParser.IdentifierRValueContext):
		var = self.visit(ctx.identifier_ext())
		if var.type != types.COLOR:
			raise exceptions.IncorrectType(ctx.identifier_ext(), var.type, types.COLOR)

	def visitVarRValue(self, ctx:glangParser.VarRValueContext):
		z = self.visit(ctx.getChild(0))
		return z
