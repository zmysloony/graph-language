# Generated from glang.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .glangParser import glangParser
else:
    from glangParser import glangParser

# This class defines a complete generic visitor for a parse tree produced by glangParser.

class glangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by glangParser#script.
    def visitScript(self, ctx:glangParser.ScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#emptyArray.
    def visitEmptyArray(self, ctx:glangParser.EmptyArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#filledArray.
    def visitFilledArray(self, ctx:glangParser.FilledArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#string.
    def visitString(self, ctx:glangParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#color.
    def visitColor(self, ctx:glangParser.ColorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#data_point.
    def visitData_point(self, ctx:glangParser.Data_pointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#data_point_colored.
    def visitData_point_colored(self, ctx:glangParser.Data_point_coloredContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#named_value.
    def visitNamed_value(self, ctx:glangParser.Named_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#named_value_colored.
    def visitNamed_value_colored(self, ctx:glangParser.Named_value_coloredContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#objectJValue.
    def visitObjectJValue(self, ctx:glangParser.ObjectJValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#regularJValue.
    def visitRegularJValue(self, ctx:glangParser.RegularJValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#arrayJValue.
    def visitArrayJValue(self, ctx:glangParser.ArrayJValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#emptyArrayJValue.
    def visitEmptyArrayJValue(self, ctx:glangParser.EmptyArrayJValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#j_member.
    def visitJ_member(self, ctx:glangParser.J_memberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#j_object.
    def visitJ_object(self, ctx:glangParser.J_objectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#id_list.
    def visitId_list(self, ctx:glangParser.Id_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#arg_list.
    def visitArg_list(self, ctx:glangParser.Arg_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#function.
    def visitFunction(self, ctx:glangParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#function_call.
    def visitFunction_call(self, ctx:glangParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#for_loop.
    def visitFor_loop(self, ctx:glangParser.For_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#if_cond.
    def visitIf_cond(self, ctx:glangParser.If_condContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#number.
    def visitNumber(self, ctx:glangParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#numberMExpression.
    def visitNumberMExpression(self, ctx:glangParser.NumberMExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#addSubMExpression.
    def visitAddSubMExpression(self, ctx:glangParser.AddSubMExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#groupMExpression.
    def visitGroupMExpression(self, ctx:glangParser.GroupMExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#mulDivMExpression.
    def visitMulDivMExpression(self, ctx:glangParser.MulDivMExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#minusMExpression.
    def visitMinusMExpression(self, ctx:glangParser.MinusMExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#identifierMExpression.
    def visitIdentifierMExpression(self, ctx:glangParser.IdentifierMExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#plus_minus.
    def visitPlus_minus(self, ctx:glangParser.Plus_minusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#mul_div.
    def visitMul_div(self, ctx:glangParser.Mul_divContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#propertyAccess.
    def visitPropertyAccess(self, ctx:glangParser.PropertyAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#arrayAccess.
    def visitArrayAccess(self, ctx:glangParser.ArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#genericIdentifier.
    def visitGenericIdentifier(self, ctx:glangParser.GenericIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#jsonAccess.
    def visitJsonAccess(self, ctx:glangParser.JsonAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#l_value.
    def visitL_value(self, ctx:glangParser.L_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#r_value_list.
    def visitR_value_list(self, ctx:glangParser.R_value_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#varRValue.
    def visitVarRValue(self, ctx:glangParser.VarRValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#identifierRValue.
    def visitIdentifierRValue(self, ctx:glangParser.IdentifierRValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#functionRValue.
    def visitFunctionRValue(self, ctx:glangParser.FunctionRValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#evalRValue.
    def visitEvalRValue(self, ctx:glangParser.EvalRValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#nullRValue.
    def visitNullRValue(self, ctx:glangParser.NullRValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#boolLExpression.
    def visitBoolLExpression(self, ctx:glangParser.BoolLExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#identifierLExpression.
    def visitIdentifierLExpression(self, ctx:glangParser.IdentifierLExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#parenLExpression.
    def visitParenLExpression(self, ctx:glangParser.ParenLExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#notLExpression.
    def visitNotLExpression(self, ctx:glangParser.NotLExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#comparatorLExpression.
    def visitComparatorLExpression(self, ctx:glangParser.ComparatorLExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#binaryLExpression.
    def visitBinaryLExpression(self, ctx:glangParser.BinaryLExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#mathLExpression.
    def visitMathLExpression(self, ctx:glangParser.MathLExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#comparator.
    def visitComparator(self, ctx:glangParser.ComparatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#binary.
    def visitBinary(self, ctx:glangParser.BinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#boolean.
    def visitBoolean(self, ctx:glangParser.BooleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#assignment.
    def visitAssignment(self, ctx:glangParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#inplace_math_op.
    def visitInplace_math_op(self, ctx:glangParser.Inplace_math_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#return_statement.
    def visitReturn_statement(self, ctx:glangParser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#operation.
    def visitOperation(self, ctx:glangParser.OperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#line_operation.
    def visitLine_operation(self, ctx:glangParser.Line_operationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#sequential_code.
    def visitSequential_code(self, ctx:glangParser.Sequential_codeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by glangParser#segment.
    def visitSegment(self, ctx:glangParser.SegmentContext):
        return self.visitChildren(ctx)



del glangParser