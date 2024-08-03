from typing import List

from . import Statement, Expression

from bytecode import Instr


class BlockStatement(Statement):
    statements: List[Statement]

    def __init__(self, statements: List[Statement] = None):
        if not statements:
            statements = []
        self.statements = statements

    def add(self, statement: Statement):
        self.statements.append(statement)

    def optimize(self) -> Statement:
        for i, _ in enumerate(self.statements):
            self.statements[i] = self.statements[i].optimize()
        return self

    def compile(self) -> List[Instr]:
        result: List[Instr] = []

        for statement in self.statements:
            result += statement.compile()

        return result

    def check_error(self) -> Expression | None:
        expr_error = None
        for statement in self.statements:
            expr_error = statement.check_error()
            if expr_error:
                return expr_error
        return None

    def output(self) -> str:
        result = "[\n"
        for statement in self.statements:
            result += statement.output() + '\n'
        result += ']'
        return result
