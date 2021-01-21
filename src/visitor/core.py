import typing
from inspect import signature, getmembers, isfunction

from antlr4 import ParserRuleContext

from generated.glangParser import glangParser
from generated.glangVisitor import glangVisitor
from src.grapher import builtins as blns
from src.visitor import helpers, types, exceptions
from src.visitor.helpers import VarTree, to_number_or_int, Var, Function, ReturnException


def get_builtins():
	f = {}
	for func in getmembers(blns, isfunction):
		f[func[0]] = func[1]
	return f


class GVisitor(glangVisitor):
	def __init__(self):
		super(glangVisitor, self).__init__()
		self.stack: typing.List[VarTree] = []
		self.variables: VarTree = VarTree(ParserRuleContext())
		self.builtins: typing.Dict = get_builtins()
		self.functions: typing.Dict[str, Function] = {}

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

	def visitGenericIdentifier(self, ctx:glangParser.GenericIdentifierContext, create=False):
		if create:
			return self.variables.get_or_declare(ctx.IDENTIFIER())
		else:
			return self.variables.get(ctx.IDENTIFIER())

	def visitPropertyAccess(self, ctx:glangParser.PropertyAccessContext):
		try:
			return getattr(self.visit(ctx.identifier_ext()).value, ctx.IDENTIFIER().symbol.text)
		except AttributeError:
			raise exceptions.AttributeNotDefined(ctx.identifier_ext(), ctx.IDENTIFIER())

	def visitJsonAccess(self, ctx:glangParser.JsonAccessContext):
		var = self.visit(ctx.identifier_ext())
		if var.type != types.J_OBJECT:
			raise exceptions.JsonAccessOnNonJsonVariable(ctx.identifier_ext())
		attr_name = self.visit(ctx.string()).value
		if attr_name in var.value:
			return var.value[attr_name]
		else:
			raise exceptions.AttributeNotDefined(ctx.identifier_ext(), attr_name)

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

	def visitString(self, ctx: glangParser.StringContext):
		return Var(ctx.getText()[1:-1], types.STRING)

	def visitColor(self, ctx:glangParser.ColorContext):
		return Var(ctx.COLOR().getText(), types.COLOR)

	def visitNumber(self, ctx:glangParser.NumberContext):
		return Var(eval(self.visit(ctx.math_expression())), types.NUMBER)

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
			return var.value.color
		else:
			return var

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
				# check param count (kwargs and default values not allowed)
				sig = signature(func)
				if len(sig.parameters) == len(args):
					return func(*args)
				else:
					raise exceptions.WrongArgumentCount(ctx.IDENTIFIER(), len(args), len(sig.parameters))
		raise exceptions.FunctionNotDefined(ctx.IDENTIFIER())
