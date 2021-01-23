import os
import typing
from copy import copy
from inspect import signature

from antlr4 import ParserRuleContext

from generated.src.glangParser import glangParser
from generated.src.glangVisitor import glangVisitor
from src.grapher import builtins
from src.grapher.builtins import RESULT_DIR, insert_css
from src.visitor import helpers, types, exceptions
from src.visitor.helpers import VarTree, to_number_or_int, Var, Function, ReturnException


class GVisitor(glangVisitor):
	def __init__(self):
		super(glangVisitor, self).__init__()
		self.stack: typing.List[VarTree] = []
		self.variables: VarTree = VarTree(ParserRuleContext())
		self.builtins: typing.Dict = builtins.FUNCTIONS
		self.functions: typing.Dict[str, Function] = {}
		self.html = ''

	def enter_context(self, context: ParserRuleContext):
		self.variables = self.variables.enter(context)

	def exit_context(self):
		self.variables = self.variables.exit()

	def visitScript(self, ctx:glangParser.ScriptContext):
		self.variables = VarTree(ctx)
		for func in ctx.function():
			self.visitFunction(func)
		for seq in ctx.sequential_code():
			self.visitSequential_code(seq)

	def visitGenericIdentifier(self, ctx:glangParser.GenericIdentifierContext, set_to=None):
		if set_to:
			self.variables.set(ctx.IDENTIFIER(), var=set_to)
		else:
			return self.variables.get(ctx.IDENTIFIER())

	def visitIdentifierExt(self, ctx, set_to=None):
		if isinstance(ctx, glangParser.PropertyAccessContext):
			return self.visitPropertyAccess(ctx, set_to=set_to)
		if isinstance(ctx, glangParser.ArrayAccessContext):
			return self.visitArrayAccess(ctx, set_to=set_to)
		if isinstance(ctx, glangParser.JsonAccessContext):
			return self.visitJsonAccess(ctx, set_to=set_to)

	def visitPropertyAccess(self, ctx:glangParser.PropertyAccessContext, set_to=None):
		try:
			if set_to:
				setattr(self.visit(ctx.identifier_ext()).value, ctx.IDENTIFIER().symbol.text, set_to)
			return getattr(self.visit(ctx.identifier_ext()).value, ctx.IDENTIFIER().symbol.text)
		except AttributeError:
			raise exceptions.AttributeNotDefined(ctx.identifier_ext(), ctx.IDENTIFIER())

	def visitJsonAccess(self, ctx:glangParser.JsonAccessContext, set_to=None):
		var = self.visit(ctx.identifier_ext())
		# var = self.visitIdentifierExt(ctx, set_to=set_to)
		if var.type != types.J_OBJECT:
			raise exceptions.JsonAccessOnNonJsonVariable(ctx.identifier_ext())
		attr_name = self.visit(ctx.string()).value
		if attr_name in var.value:
			if set_to:
				var.value[attr_name] = set_to
			return var.value[attr_name]
		else:
			raise exceptions.AttributeNotDefined(ctx.identifier_ext(), attr_name)

	def visitArrayAccess(self, ctx:glangParser.ArrayAccessContext, set_to=None):
		var = self.visit(ctx.identifier_ext())
		# var = self.visitIdentifierExt(ctx, set_to)
		if var.type != types.LIST:
			raise exceptions.IncorrectType(ctx.identifier_ext(), var.type, types.LIST)
		number = to_number_or_int(ctx.NUMBER())
		if not isinstance(number, int):
			raise exceptions.IncorrectType(number, expected_types=types.INTEGER)
		try:
			if set_to:
				var.value[number] = set_to
			return var.value[number]
		except IndexError:
			raise exceptions.ListIndexError(ctx.identifier_ext(), number, len(var.value))

	def visitL_value(self, ctx:glangParser.L_valueContext, set_to=None):
		identifier = ctx.identifier_ext()
		if ctx.COLOR_SIGN():
			var = self.visit(identifier)
			if var.type not in [types.DATA_POINT, types.NAMED_VALUE]:
				raise exceptions.IncorrectType(identifier, var.type, (types.DATA_POINT, types.NAMED_VALUE))
			if set_to:
				var.value.color = set_to
				return var.value.color
			else:
				return var.value.color

		if isinstance(identifier, glangParser.GenericIdentifierContext):
			var = self.visitGenericIdentifier(identifier, set_to=set_to)
		else:
			var = self.visitIdentifierExt(identifier, set_to=set_to)
		return var

		# if ctx.COLOR_SIGN():
		# 	if var.type in [types.DATA_POINT, types.NAMED_VALUE]:
		# 		return var.value.color
		# 	else:
		# 		raise exceptions.IncorrectType(identifier, var.type, (types.DATA_POINT, types.NAMED_VALUE))
		# return var

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
		# l_var = self.visitL_value(ctx.l_value(), True)
		r_var = self.visit(ctx.r_value())
		self.visitL_value(ctx.l_value(), set_to=Var(r_var.value, r_var.type))
		# l_var.value = r_var.value
		# l_var.type = r_var.type

	def visitBoolean(self, ctx:glangParser.BooleanContext):
		if ctx.TRUE():
			return 'True'
		return 'False'

	def visitRegularString(self, ctx: glangParser.RegularStringContext):
		return Var(ctx.getText()[1:-1], types.STRING)

	def visitStringifiedMathExp(self, ctx:glangParser.StringifiedMathExpContext):
		arithm_result = eval(self.visit(ctx.math_expression()))
		string = ctx.STRING() if ctx.STRING() else ctx.DQUOT_STRING()
		return Var(string.getText()[1:-1] + str(arithm_result), types.STRING)

	def visitString_addition(self, ctx:glangParser.String_additionContext):
		return Var(self.visit(ctx.string_element(0)).value + self.visit(ctx.string_element(1)).value, types.STRING)

	def visitColor(self, ctx:glangParser.ColorContext):
		return Var(ctx.COLOR().getText(), types.COLOR)

	def visitNumber(self, ctx:glangParser.NumberContext):
		return Var(eval(self.visit(ctx.math_expression())), types.NUMBER)

	def visitIdentifierLExpression(self, ctx:glangParser.IdentifierLExpressionContext):
		var = self.visitL_value(ctx.l_value())
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

	def visitMathLExpression(self, ctx:glangParser.MathLExpressionContext):
		return str(eval(self.visit(ctx.math_expression())))

	def visitNumberMExpression(self, ctx:glangParser.NumberMExpressionContext):
		return ctx.NUMBER().getText()

	def visitMinusMExpression(self, ctx:glangParser.MinusMExpressionContext):
		return '-' + self.visit(ctx.math_expression())

	def visitIdentifierMExpression(self, ctx:glangParser.IdentifierMExpressionContext):
		var = self.visit(ctx.identifier_ext())
		if var.type != types.NUMBER:
			raise exceptions.IncorrectType(ctx.identifier_ext(), var.type, types.NUMBER)
		return str(var.value)

	def visitPlus_minus(self, ctx:glangParser.Plus_minusContext):
		return ctx.getText()

	def visitMul_div(self, ctx:glangParser.Mul_divContext):
		return ctx.getText()

	def visitAddSubMExpression(self, ctx:glangParser.AddSubMExpressionContext):
		return '{}{}{}'.format(self.visit(ctx.left), self.visit(ctx.op), self.visit(ctx.right))

	def visitMulDivMExpression(self, ctx:glangParser.MulDivMExpressionContext):
		return '{}{}{}'.format(self.visit(ctx.left), self.visit(ctx.op), self.visit(ctx.right))

	def visitGroupMExpression(self, ctx:glangParser.GroupMExpressionContext):
		return '({})'.format(self.visit(ctx.math_expression()))

	def visitNullRValue(self, ctx:glangParser.NullRValueContext):
		return Var(None, None)

	def visitEvalRValue(self, ctx:glangParser.EvalRValueContext):
		if ctx.logical_expression():
			children = ctx.logical_expression().children
			if len(children) == 1 and isinstance(children[0], glangParser.Math_expressionContext):
				return Var(to_number_or_int(self.visit(ctx.logical_expression()), True), types.NUMBER)
			expr = self.visit(ctx.logical_expression())
			expr_type = types.BOOLEAN
		else:
			expr = self.visit(ctx.math_expression())
			expr_type = types.NUMBER
		return Var(eval(expr), expr_type)

	def visitIdentifierRValue(self, ctx:glangParser.IdentifierRValueContext):
		var = self.visit(ctx.identifier_ext())
		if ctx.COLOR_SIGN():
			if var.type not in [types.DATA_POINT, types.NAMED_VALUE]:
				raise exceptions.IncorrectType(ctx.identifier_ext(), var.type, [types.DATA_POINT, types.NAMED_VALUE])
			return copy(var.value.color)
		else:
			return copy(var)

	def visitR_value_list(self, ctx:glangParser.R_value_listContext):
		array = []
		for r_val in ctx.r_value():
			array.append(self.visit(r_val))
		return array

	def visitEmptyArray(self, ctx:glangParser.EmptyArrayContext):
		return Var([], types.LIST)

	def visitFilledArray(self, ctx:glangParser.FilledArrayContext):
		if ctx.r_value():
			return Var([self.visit(ctx.r_value())], types.LIST)
		else:
			return Var(self.visit(ctx.r_value_list()), types.LIST)

	def visitRegularJValue(self, ctx:glangParser.RegularJValueContext):
		if ctx.boolean():
			return Var(eval(ctx.boolean()), types.BOOLEAN)
		else:
			return self.visitChildren(ctx)

	def visitEmptyArrayJValue(self, ctx:glangParser.EmptyArrayJValueContext):
		return Var([], types.LIST)

	def visitArrayJValue(self, ctx:glangParser.ArrayJValueContext):
		array = []
		for jval in ctx.j_value():
			array.append(self.visit(jval))
		return Var(array, types.LIST)

	def visitJ_member(self, ctx:glangParser.J_memberContext):
		attr_name = self.visit(ctx.string()).value
		if len(attr_name) == 0:
			raise exceptions.IncorrectJsonMemberName(ctx.string())
		return attr_name, self.visit(ctx.j_value())

	def visitJ_object(self, ctx:glangParser.J_objectContext):
		attributes = {}
		for member in ctx.j_member():
			member_calculated = self.visit(member)
			if member_calculated[0] in attributes:
				raise exceptions.AmbigiousJsonMember(member, member_calculated[0])
			attributes[member_calculated[0]] = member_calculated[1]
		return Var(attributes, types.J_OBJECT)

	def visitInplace_math_op(self, ctx:glangParser.Inplace_math_opContext):
		left = self.visit(ctx.l_value())

		def illegal_operator():
			return exceptions.IllegalOperator(ctx.l_value(), left.type, ctx.op)

		if left.type == types.LIST:
			if ctx.PLUS_EQ():
				right = self.visit(ctx.r_value())
				left.value.append(right)
				return
			raise illegal_operator()
		if left.type == types.NUMBER:
			right = self.visit(ctx.r_value())
			if right.type == types.NUMBER:
				left.value = eval('{}{}{}'.format(left.value, ctx.op.text[0], right.value))
				return
			raise illegal_operator()
		if left.type == types.STRING:
			if ctx.PLUS_EQ():
				right = self.visit(ctx.r_value())
				if right.type == types.STRING:
					left.value += right.value
					return
				raise exceptions.IncorrectType(ctx.r_value(), right.type, types.STRING)
			raise illegal_operator()
		raise illegal_operator()

	def visitSegment(self, ctx:glangParser.SegmentContext, new_context=True):
		if new_context:
			self.enter_context(ctx)
		self.visit(ctx.sequential_code())
		if new_context:
			self.exit_context()

	def visitIf_cond(self, ctx:glangParser.If_condContext):
		if eval(self.visit(ctx.logical_expression())):
			self.visit(ctx.segment())

	def visitFor_loop(self, ctx:glangParser.For_loopContext):
		self.enter_context(ctx)
		if ctx.before:
			self.visit(ctx.before)
		while eval(self.visit(ctx.logical_expression())):
			self.visitSegment(ctx.segment(), new_context=False)
			if ctx.after:
				self.visit(ctx.after)
		self.exit_context()

	def visitId_list(self, ctx:glangParser.Id_listContext):
		identifiers = []
		for i in ctx.IDENTIFIER():
			name = i.getText()
			if name in identifiers:
				raise exceptions.DuplicateIdentifier(i)
			identifiers.append(name)
		return identifiers

	def visitFunction(self, ctx:glangParser.FunctionContext):
		identifiers = self.visit(ctx.id_list())
		self.functions[ctx.IDENTIFIER().getText()] = Function(identifiers, ctx.segment())

	def visitArg_list(self, ctx:glangParser.Arg_listContext):
		args = []
		for rval in ctx.r_value():
			args.append(self.visit(rval))
		return args

	def visitReturn_statement(self, ctx:glangParser.Return_statementContext):
		raise ReturnException(self.visit(ctx.r_value()))

	def visitFunction_call(self, ctx:glangParser.Function_callContext):
		name = ctx.IDENTIFIER().getText()
		func = self.functions.get(name)
		args = self.visit(ctx.arg_list())
		if func:
			func.check_args(ctx.IDENTIFIER(), args)
			self.stack.append(self.variables)
			self.variables = func.create_var_tree(ctx, args)
			try:
				self.visitSegment(func.segment, new_context=False)
				self.variables = self.stack.pop()
				return
			except ReturnException as e:
				self.variables = self.stack.pop()
				return e.value
		else:
			func = self.builtins.get(name)
			if func:
				sig = signature(func)
				if len(sig.parameters) == len(args):
					return func(ctx.IDENTIFIER(), *args, visitor=self)
				else:
					raise exceptions.WrongArgumentCount(ctx.IDENTIFIER(), len(args), len(sig.parameters))
		raise exceptions.FunctionNotDefined(ctx.IDENTIFIER())

	def generate_total_html(self):
		open(os.path.join(RESULT_DIR, 'result.html'), 'w+').write(insert_css(self.html))
