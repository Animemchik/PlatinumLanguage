from typing import List

from .. import Token, TokenType, Position
from . import Expression, ValueExpression, ValueType, PPLErrorExpression, ErrorType

from bytecode import Instr, Compare


class ConditionalExpression(Expression):
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
            match (self.expr1.vtype, self.expr2.vtype):
                case (ValueType.Integer, ValueType.Integer) | \
                     (ValueType.Float, ValueType.Float) | \
                     (ValueType.Integer, ValueType.Float) | \
                     (ValueType.Float, ValueType.Integer):
                    match self.optype:
                        case TokenType.GT:
                            return ValueExpression(
                                Token(
                                    TokenType.BOOL,
                                    str(float(self.expr1.value.value) > float(self.expr2.value.value)),
                                    self.expr1.value.lexeme + ' > ' + self.expr2.value.lexeme,
                                    Position(
                                        self.expr1.value.position.start_pos,
                                        self.expr2.value.position.end_pos,
                                        self.expr1.value.position.line,
                                        self.expr1.value.position.col
                                    )
                                )
                            )
                        case TokenType.GTEQ:
                            return ValueExpression(
                                Token(
                                    TokenType.BOOL,
                                    str(float(self.expr1.value.value) >= float(self.expr2.value.value)),
                                    self.expr1.value.lexeme + ' >= ' + self.expr2.value.lexeme,
                                    Position(
                                        self.expr1.value.position.start_pos,
                                        self.expr2.value.position.end_pos,
                                        self.expr1.value.position.line,
                                        self.expr1.value.position.col
                                    )
                                )
                            )
                        case TokenType.LT:
                            return ValueExpression(
                                Token(
                                    TokenType.BOOL,
                                    str(float(self.expr1.value.value) < float(self.expr2.value.value)),
                                    self.expr1.value.lexeme + ' < ' + self.expr2.value.lexeme,
                                    Position(
                                        self.expr1.value.position.start_pos,
                                        self.expr2.value.position.end_pos,
                                        self.expr1.value.position.line,
                                        self.expr1.value.position.col
                                    )
                                )
                            )
                        case TokenType.LTEQ:
                            return ValueExpression(
                                Token(
                                    TokenType.BOOL,
                                    str(float(self.expr1.value.value) <= float(self.expr2.value.value)),
                                    self.expr1.value.lexeme + ' <= ' + self.expr2.value.lexeme,
                                    Position(
                                        self.expr1.value.position.start_pos,
                                        self.expr2.value.position.end_pos,
                                        self.expr1.value.position.line,
                                        self.expr1.value.position.col
                                    )
                                )
                            )
                    return PPLErrorExpression(
                        ErrorType.ParserException,
                        f"There is no implementation of {self.optype.get_name()} operator with Number",
                        Position(
                            self.expr1.value.position.start_pos,
                            self.expr2.value.position.end_pos,
                            self.expr1.value.position.line,
                            self.expr1.value.position.col
                        )
                    )
            return PPLErrorExpression(
                ErrorType.ParserException,
                f"Can't use {self.expr1.vtype.name} {self.optype.get_name()} {self.expr2.vtype.name}",
                Position(
                    self.expr1.value.position.start_pos,
                    self.expr2.value.position.end_pos,
                    self.expr1.value.position.line,
                    self.expr1.value.position.col
                )
            )

        return self

    def compile(self) -> List[Instr]:
        result: List[Instr] = []
        result += self.expr1.compile()
        result += self.expr2.compile()

        match self.optype:
            case TokenType.GT:
                result.append(Instr("COMPARE_OP", Compare.GT))
            case TokenType.GTEQ:
                result.append(Instr("COMPARE_OP", Compare.GE))
            case TokenType.LT:
                result.append(Instr("COMPARE_OP", Compare.LT))
            case TokenType.LTEQ:
                result.append(Instr("COMPARE_OP", Compare.LE))

        return result

    def check_error(self) -> Expression | None:
        expr1_error = self.expr1.check_error()
        return expr1_error if expr1_error else self.expr2.check_error()

    def output(self) -> str:
        return f"({self.expr1.output()} {self.optype.get_name()} {self.expr2.output()})"
