# Generated from glang.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .glangParser import glangParser
else:
    from glangParser import glangParser

# This class defines a complete listener for a parse tree produced by glangParser.
class glangListener(ParseTreeListener):

    # Enter a parse tree produced by glangParser#script.
    def enterScript(self, ctx:glangParser.ScriptContext):
        pass

    # Exit a parse tree produced by glangParser#script.
    def exitScript(self, ctx:glangParser.ScriptContext):
        pass


    # Enter a parse tree produced by glangParser#emptyArray.
    def enterEmptyArray(self, ctx:glangParser.EmptyArrayContext):
        pass

    # Exit a parse tree produced by glangParser#emptyArray.
    def exitEmptyArray(self, ctx:glangParser.EmptyArrayContext):
        pass


    # Enter a parse tree produced by glangParser#filledArray.
    def enterFilledArray(self, ctx:glangParser.FilledArrayContext):
        pass

    # Exit a parse tree produced by glangParser#filledArray.
    def exitFilledArray(self, ctx:glangParser.FilledArrayContext):
        pass


    # Enter a parse tree produced by glangParser#string.
    def enterString(self, ctx:glangParser.StringContext):
        pass

    # Exit a parse tree produced by glangParser#string.
    def exitString(self, ctx:glangParser.StringContext):
        pass


    # Enter a parse tree produced by glangParser#color.
    def enterColor(self, ctx:glangParser.ColorContext):
        pass

    # Exit a parse tree produced by glangParser#color.
    def exitColor(self, ctx:glangParser.ColorContext):
        pass


    # Enter a parse tree produced by glangParser#data_point.
    def enterData_point(self, ctx:glangParser.Data_pointContext):
        pass

    # Exit a parse tree produced by glangParser#data_point.
    def exitData_point(self, ctx:glangParser.Data_pointContext):
        pass


    # Enter a parse tree produced by glangParser#data_point_colored.
    def enterData_point_colored(self, ctx:glangParser.Data_point_coloredContext):
        pass

    # Exit a parse tree produced by glangParser#data_point_colored.
    def exitData_point_colored(self, ctx:glangParser.Data_point_coloredContext):
        pass


    # Enter a parse tree produced by glangParser#named_value.
    def enterNamed_value(self, ctx:glangParser.Named_valueContext):
        pass

    # Exit a parse tree produced by glangParser#named_value.
    def exitNamed_value(self, ctx:glangParser.Named_valueContext):
        pass


    # Enter a parse tree produced by glangParser#named_value_colored.
    def enterNamed_value_colored(self, ctx:glangParser.Named_value_coloredContext):
        pass

    # Exit a parse tree produced by glangParser#named_value_colored.
    def exitNamed_value_colored(self, ctx:glangParser.Named_value_coloredContext):
        pass


    # Enter a parse tree produced by glangParser#objectJValue.
    def enterObjectJValue(self, ctx:glangParser.ObjectJValueContext):
        pass

    # Exit a parse tree produced by glangParser#objectJValue.
    def exitObjectJValue(self, ctx:glangParser.ObjectJValueContext):
        pass


    # Enter a parse tree produced by glangParser#regularJValue.
    def enterRegularJValue(self, ctx:glangParser.RegularJValueContext):
        pass

    # Exit a parse tree produced by glangParser#regularJValue.
    def exitRegularJValue(self, ctx:glangParser.RegularJValueContext):
        pass


    # Enter a parse tree produced by glangParser#arrayJValue.
    def enterArrayJValue(self, ctx:glangParser.ArrayJValueContext):
        pass

    # Exit a parse tree produced by glangParser#arrayJValue.
    def exitArrayJValue(self, ctx:glangParser.ArrayJValueContext):
        pass


    # Enter a parse tree produced by glangParser#emptyArrayJValue.
    def enterEmptyArrayJValue(self, ctx:glangParser.EmptyArrayJValueContext):
        pass

    # Exit a parse tree produced by glangParser#emptyArrayJValue.
    def exitEmptyArrayJValue(self, ctx:glangParser.EmptyArrayJValueContext):
        pass


    # Enter a parse tree produced by glangParser#j_member.
    def enterJ_member(self, ctx:glangParser.J_memberContext):
        pass

    # Exit a parse tree produced by glangParser#j_member.
    def exitJ_member(self, ctx:glangParser.J_memberContext):
        pass


    # Enter a parse tree produced by glangParser#j_object.
    def enterJ_object(self, ctx:glangParser.J_objectContext):
        pass

    # Exit a parse tree produced by glangParser#j_object.
    def exitJ_object(self, ctx:glangParser.J_objectContext):
        pass


    # Enter a parse tree produced by glangParser#id_list.
    def enterId_list(self, ctx:glangParser.Id_listContext):
        pass

    # Exit a parse tree produced by glangParser#id_list.
    def exitId_list(self, ctx:glangParser.Id_listContext):
        pass


    # Enter a parse tree produced by glangParser#arg_list.
    def enterArg_list(self, ctx:glangParser.Arg_listContext):
        pass

    # Exit a parse tree produced by glangParser#arg_list.
    def exitArg_list(self, ctx:glangParser.Arg_listContext):
        pass


    # Enter a parse tree produced by glangParser#function.
    def enterFunction(self, ctx:glangParser.FunctionContext):
        pass

    # Exit a parse tree produced by glangParser#function.
    def exitFunction(self, ctx:glangParser.FunctionContext):
        pass


    # Enter a parse tree produced by glangParser#function_call.
    def enterFunction_call(self, ctx:glangParser.Function_callContext):
        pass

    # Exit a parse tree produced by glangParser#function_call.
    def exitFunction_call(self, ctx:glangParser.Function_callContext):
        pass


    # Enter a parse tree produced by glangParser#for_loop.
    def enterFor_loop(self, ctx:glangParser.For_loopContext):
        pass

    # Exit a parse tree produced by glangParser#for_loop.
    def exitFor_loop(self, ctx:glangParser.For_loopContext):
        pass


    # Enter a parse tree produced by glangParser#if_cond.
    def enterIf_cond(self, ctx:glangParser.If_condContext):
        pass

    # Exit a parse tree produced by glangParser#if_cond.
    def exitIf_cond(self, ctx:glangParser.If_condContext):
        pass


    # Enter a parse tree produced by glangParser#number.
    def enterNumber(self, ctx:glangParser.NumberContext):
        pass

    # Exit a parse tree produced by glangParser#number.
    def exitNumber(self, ctx:glangParser.NumberContext):
        pass


    # Enter a parse tree produced by glangParser#numberMExpression.
    def enterNumberMExpression(self, ctx:glangParser.NumberMExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#numberMExpression.
    def exitNumberMExpression(self, ctx:glangParser.NumberMExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#addSubMExpression.
    def enterAddSubMExpression(self, ctx:glangParser.AddSubMExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#addSubMExpression.
    def exitAddSubMExpression(self, ctx:glangParser.AddSubMExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#groupMExpression.
    def enterGroupMExpression(self, ctx:glangParser.GroupMExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#groupMExpression.
    def exitGroupMExpression(self, ctx:glangParser.GroupMExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#mulDivMExpression.
    def enterMulDivMExpression(self, ctx:glangParser.MulDivMExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#mulDivMExpression.
    def exitMulDivMExpression(self, ctx:glangParser.MulDivMExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#minusMExpression.
    def enterMinusMExpression(self, ctx:glangParser.MinusMExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#minusMExpression.
    def exitMinusMExpression(self, ctx:glangParser.MinusMExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#identifierMExpression.
    def enterIdentifierMExpression(self, ctx:glangParser.IdentifierMExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#identifierMExpression.
    def exitIdentifierMExpression(self, ctx:glangParser.IdentifierMExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#plus_minus.
    def enterPlus_minus(self, ctx:glangParser.Plus_minusContext):
        pass

    # Exit a parse tree produced by glangParser#plus_minus.
    def exitPlus_minus(self, ctx:glangParser.Plus_minusContext):
        pass


    # Enter a parse tree produced by glangParser#mul_div.
    def enterMul_div(self, ctx:glangParser.Mul_divContext):
        pass

    # Exit a parse tree produced by glangParser#mul_div.
    def exitMul_div(self, ctx:glangParser.Mul_divContext):
        pass


    # Enter a parse tree produced by glangParser#propertyAccess.
    def enterPropertyAccess(self, ctx:glangParser.PropertyAccessContext):
        pass

    # Exit a parse tree produced by glangParser#propertyAccess.
    def exitPropertyAccess(self, ctx:glangParser.PropertyAccessContext):
        pass


    # Enter a parse tree produced by glangParser#arrayAccess.
    def enterArrayAccess(self, ctx:glangParser.ArrayAccessContext):
        pass

    # Exit a parse tree produced by glangParser#arrayAccess.
    def exitArrayAccess(self, ctx:glangParser.ArrayAccessContext):
        pass


    # Enter a parse tree produced by glangParser#genericIdentifier.
    def enterGenericIdentifier(self, ctx:glangParser.GenericIdentifierContext):
        pass

    # Exit a parse tree produced by glangParser#genericIdentifier.
    def exitGenericIdentifier(self, ctx:glangParser.GenericIdentifierContext):
        pass


    # Enter a parse tree produced by glangParser#jsonAccess.
    def enterJsonAccess(self, ctx:glangParser.JsonAccessContext):
        pass

    # Exit a parse tree produced by glangParser#jsonAccess.
    def exitJsonAccess(self, ctx:glangParser.JsonAccessContext):
        pass


    # Enter a parse tree produced by glangParser#l_value.
    def enterL_value(self, ctx:glangParser.L_valueContext):
        pass

    # Exit a parse tree produced by glangParser#l_value.
    def exitL_value(self, ctx:glangParser.L_valueContext):
        pass


    # Enter a parse tree produced by glangParser#r_value_list.
    def enterR_value_list(self, ctx:glangParser.R_value_listContext):
        pass

    # Exit a parse tree produced by glangParser#r_value_list.
    def exitR_value_list(self, ctx:glangParser.R_value_listContext):
        pass


    # Enter a parse tree produced by glangParser#varRValue.
    def enterVarRValue(self, ctx:glangParser.VarRValueContext):
        pass

    # Exit a parse tree produced by glangParser#varRValue.
    def exitVarRValue(self, ctx:glangParser.VarRValueContext):
        pass


    # Enter a parse tree produced by glangParser#identifierRValue.
    def enterIdentifierRValue(self, ctx:glangParser.IdentifierRValueContext):
        pass

    # Exit a parse tree produced by glangParser#identifierRValue.
    def exitIdentifierRValue(self, ctx:glangParser.IdentifierRValueContext):
        pass


    # Enter a parse tree produced by glangParser#functionRValue.
    def enterFunctionRValue(self, ctx:glangParser.FunctionRValueContext):
        pass

    # Exit a parse tree produced by glangParser#functionRValue.
    def exitFunctionRValue(self, ctx:glangParser.FunctionRValueContext):
        pass


    # Enter a parse tree produced by glangParser#evalRValue.
    def enterEvalRValue(self, ctx:glangParser.EvalRValueContext):
        pass

    # Exit a parse tree produced by glangParser#evalRValue.
    def exitEvalRValue(self, ctx:glangParser.EvalRValueContext):
        pass


    # Enter a parse tree produced by glangParser#nullRValue.
    def enterNullRValue(self, ctx:glangParser.NullRValueContext):
        pass

    # Exit a parse tree produced by glangParser#nullRValue.
    def exitNullRValue(self, ctx:glangParser.NullRValueContext):
        pass


    # Enter a parse tree produced by glangParser#boolLExpression.
    def enterBoolLExpression(self, ctx:glangParser.BoolLExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#boolLExpression.
    def exitBoolLExpression(self, ctx:glangParser.BoolLExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#identifierLExpression.
    def enterIdentifierLExpression(self, ctx:glangParser.IdentifierLExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#identifierLExpression.
    def exitIdentifierLExpression(self, ctx:glangParser.IdentifierLExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#parenLExpression.
    def enterParenLExpression(self, ctx:glangParser.ParenLExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#parenLExpression.
    def exitParenLExpression(self, ctx:glangParser.ParenLExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#notLExpression.
    def enterNotLExpression(self, ctx:glangParser.NotLExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#notLExpression.
    def exitNotLExpression(self, ctx:glangParser.NotLExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#comparatorLExpression.
    def enterComparatorLExpression(self, ctx:glangParser.ComparatorLExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#comparatorLExpression.
    def exitComparatorLExpression(self, ctx:glangParser.ComparatorLExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#binaryLExpression.
    def enterBinaryLExpression(self, ctx:glangParser.BinaryLExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#binaryLExpression.
    def exitBinaryLExpression(self, ctx:glangParser.BinaryLExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#mathLExpression.
    def enterMathLExpression(self, ctx:glangParser.MathLExpressionContext):
        pass

    # Exit a parse tree produced by glangParser#mathLExpression.
    def exitMathLExpression(self, ctx:glangParser.MathLExpressionContext):
        pass


    # Enter a parse tree produced by glangParser#comparator.
    def enterComparator(self, ctx:glangParser.ComparatorContext):
        pass

    # Exit a parse tree produced by glangParser#comparator.
    def exitComparator(self, ctx:glangParser.ComparatorContext):
        pass


    # Enter a parse tree produced by glangParser#binary.
    def enterBinary(self, ctx:glangParser.BinaryContext):
        pass

    # Exit a parse tree produced by glangParser#binary.
    def exitBinary(self, ctx:glangParser.BinaryContext):
        pass


    # Enter a parse tree produced by glangParser#boolean.
    def enterBoolean(self, ctx:glangParser.BooleanContext):
        pass

    # Exit a parse tree produced by glangParser#boolean.
    def exitBoolean(self, ctx:glangParser.BooleanContext):
        pass


    # Enter a parse tree produced by glangParser#assignment.
    def enterAssignment(self, ctx:glangParser.AssignmentContext):
        pass

    # Exit a parse tree produced by glangParser#assignment.
    def exitAssignment(self, ctx:glangParser.AssignmentContext):
        pass


    # Enter a parse tree produced by glangParser#inplace_math_op.
    def enterInplace_math_op(self, ctx:glangParser.Inplace_math_opContext):
        pass

    # Exit a parse tree produced by glangParser#inplace_math_op.
    def exitInplace_math_op(self, ctx:glangParser.Inplace_math_opContext):
        pass


    # Enter a parse tree produced by glangParser#return_statement.
    def enterReturn_statement(self, ctx:glangParser.Return_statementContext):
        pass

    # Exit a parse tree produced by glangParser#return_statement.
    def exitReturn_statement(self, ctx:glangParser.Return_statementContext):
        pass


    # Enter a parse tree produced by glangParser#operation.
    def enterOperation(self, ctx:glangParser.OperationContext):
        pass

    # Exit a parse tree produced by glangParser#operation.
    def exitOperation(self, ctx:glangParser.OperationContext):
        pass


    # Enter a parse tree produced by glangParser#line_operation.
    def enterLine_operation(self, ctx:glangParser.Line_operationContext):
        pass

    # Exit a parse tree produced by glangParser#line_operation.
    def exitLine_operation(self, ctx:glangParser.Line_operationContext):
        pass


    # Enter a parse tree produced by glangParser#sequential_code.
    def enterSequential_code(self, ctx:glangParser.Sequential_codeContext):
        pass

    # Exit a parse tree produced by glangParser#sequential_code.
    def exitSequential_code(self, ctx:glangParser.Sequential_codeContext):
        pass


    # Enter a parse tree produced by glangParser#segment.
    def enterSegment(self, ctx:glangParser.SegmentContext):
        pass

    # Exit a parse tree produced by glangParser#segment.
    def exitSegment(self, ctx:glangParser.SegmentContext):
        pass



del glangParser