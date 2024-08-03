from typing import List

from .. import Token, TokenType, Position
from . import Expression, ValueExpression, ValueType, PPLErrorExpression, ErrorType

from bytecode import Instr, Label, Compare


class TernaryExpression(Expression):
    condition_expr: Expression
    true_expr: Expression
    false_expr: Expression

    def __init__(self, condition_expr: Expression, true_expr: Expression, false_expr: Expression) -> None:
        self.condition_expr = condition_expr
        self.true_expr = true_expr
        self.false_expr = false_expr

    def optimize(self) -> Expression:
        self.condition_expr = self.condition_expr.optimize()
        self.true_expr = self.true_expr.optimize()
        if self.false_expr:
            self.false_expr = self.false_expr.optimize()

        if isinstance(self.condition_expr, ValueExpression) and \
           isinstance(self.true_expr, ValueExpression) and \
           isinstance(self.false_expr, ValueExpression):
            if self.condition_expr.vtype != ValueType.Bool:
                return PPLErrorExpression(
                    ErrorType.ParserException,
                    f"condition value should be True or False but got {self.condition_expr.vtype.name}"
                )
            if self.condition_expr.value:
                return self.true_expr
            else:
                if self.false_expr:
                    return self.false_expr
                return ValueExpression(Token(TokenType.NULL, "null", "null", self.true_expr.value.position))

        return self

    def compile(self) -> List[Instr]:
        label_true = Label()
        label_end = Label()

        result: List[Instr] = []
        result += self.condition_expr.compile()

        result.append(Instr("LOAD_CONST", True))
        result.append(Instr("COMPARE_OP", Compare.EQ))
        result.append(Instr("POP_JUMP_IF_TRUE", label_true))

        if self.false_expr:
            result += self.false_expr.compile()
        else:
            result.append(Instr("LOAD_CONST", None))
        result.append(Instr("JUMP_FORWARD", label_end))

        result.append(label_true)
        result += self.true_expr.compile()

        result.append(label_end)

        return result

    def check_error(self) -> Expression | None:
        condition_expr_error = self.condition_expr.check_error()
        true_expr_error = self.true_expr.check_error()
        if self.false_expr:
            false_expr_error = self.false_expr.check_error()
        else:
            false_expr_error = None

        if condition_expr_error:
            return condition_expr_error
        elif true_expr_error:
            return true_expr_error
        else:
            return false_expr_error

    def output(self) -> str:
        return f"({self.condition_expr.output()} ? {self.true_expr.output()} : {self.false_expr.output()})"
