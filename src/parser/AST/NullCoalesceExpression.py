from typing import List

from .. import Token, TokenType, Position
from . import Expression, ValueExpression, ValueType, PPLErrorExpression, ErrorType

from bytecode import Instr, Label, Compare


class NullCoalesceExpression(Expression):
    expr1: Expression
    expr2: Expression
    optype: TokenType

    def __init__(self, optype: TokenType, expr1: Expression, expr2: Expression) -> None:
        self.expr1 = expr1
        self.expr2 = expr2
        self.optype = optype

    def optimize(self) -> Expression:
        self.expr1 = self.expr1.optimize()
        self.expr2 = self.expr2.optimize()

        if isinstance(self.expr1, ValueExpression) and isinstance(self.expr2, ValueExpression):
            if self.expr1.vtype == ValueType.Null:
                return self.expr2
            else:
                return self.expr1

        return self

    def compile(self) -> List[Instr]:
        label_not_none = Label()
        label_end = Label()

        result: List[Instr] = []
        result += self.expr1.compile()

        result.append(Instr("COPY", 1))
        result.append(Instr("LOAD_CONST", None))
        result.append(Instr("COMPARE_OP", Compare.EQ))
        result.append(Instr("POP_JUMP_IF_FALSE", label_not_none))

        result.append(Instr("POP_TOP"))
        result += self.expr2.compile()
        result.append(Instr("JUMP_FORWARD", label_end))

        result.append(label_not_none)

        result.append(label_end)

        return result

    def check_error(self) -> Expression | None:
        expr1_error = self.expr1.check_error()
        return expr1_error if expr1_error else self.expr2.check_error()

    def output(self) -> str:
        return f"({self.expr1.output()} {self.optype.get_name()} {self.expr2.output()})"
