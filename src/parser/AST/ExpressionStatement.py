from typing import List

from . import Statement, Expression

from bytecode import Instr


class ExpressionStatement(Statement):
    expression: Expression

    def __init__(self, expression: Expression):
        self.expression = expression

    def optimize(self) -> Statement:
        self.expression = self.expression.optimize()
        return self

    def compile(self) -> List[Instr]:
        return self.expression.compile()

    def check_error(self) -> Expression | None:
        return self.expression.check_error()

    def output(self) -> str:
        result = f"({self.expression.output()})"
        return result
