from typing import List

from .. import Token, TokenType, Position
from . import Expression, ValueExpression, ValueType, PPLErrorExpression, ErrorType

from bytecode import Instr, BinaryOp


class UnaryExpression(Expression):
    expr: Expression
    optype: Token

    def __init__(self, optype: Token, expr: Expression) -> None:
        self.expr = expr
        self.optype = optype

    def optimize(self) -> Expression:
        self.expr = self.expr.optimize()

        if isinstance(self.expr, ValueExpression):
            match self.expr.vtype:
                case ValueType.Integer:
                    match self.optype.ttype:
                        case TokenType.PLUS:
                            return ValueExpression(
                                Token(
                                    TokenType.INT,
                                    str(+int(self.expr.value.value)),
                                    '+' + self.expr.value.lexeme,
                                    Position(
                                        self.optype.position.start_pos,
                                        self.expr.value.position.end_pos,
                                        self.expr.value.position.line,
                                        self.expr.value.position.col
                                    )
                                )
                            )
                        case TokenType.MINUS:
                            return ValueExpression(
                                Token(
                                    TokenType.INT,
                                    str(-int(self.expr.value.value)),
                                    '-' + self.expr.value.lexeme,
                                    Position(
                                        self.optype.position.start_pos,
                                        self.expr.value.position.end_pos,
                                        self.expr.value.position.line,
                                        self.expr.value.position.col
                                    )
                                )
                            )
                    return PPLErrorExpression(
                        ErrorType.ParserException,
                        f"There is no implementation of {self.optype.ttype.get_name()} operator for Number",
                        Position(
                            self.optype.position.start_pos,
                            self.expr.value.position.end_pos,
                            self.expr.value.position.line,
                            self.expr.value.position.col
                        )
                    )
                case (ValueType.Float, ValueType.Float) | \
                     (ValueType.Integer, ValueType.Float) | \
                     (ValueType.Float, ValueType.Integer):
                    match self.optype:
                        case TokenType.PLUS:
                            return ValueExpression(
                                Token(
                                    TokenType.FLOAT,
                                    str(+float(self.expr.value.value)),
                                    '+' + self.expr.value.lexeme,
                                    Position(
                                        self.optype.position.start_pos,
                                        self.expr.value.position.end_pos,
                                        self.expr.value.position.line,
                                        self.expr.value.position.col
                                    )
                                )
                            )
                        case TokenType.MINUS:
                            return ValueExpression(
                                Token(
                                    TokenType.FLOAT,
                                    str(-float(self.expr.value.value)),
                                    '-' + self.expr.value.lexeme,
                                    Position(
                                        self.optype.position.start_pos,
                                        self.expr.value.position.end_pos,
                                        self.expr.value.position.line,
                                        self.expr.value.position.col
                                    )
                                )
                            )
                    return PPLErrorExpression(
                        ErrorType.ParserException,
                        f"There is no implementation of {self.optype.ttype.get_name()} operator for Number",
                        Position(
                            self.optype.position.start_pos,
                            self.expr.value.position.end_pos,
                            self.expr.value.position.line,
                            self.expr.value.position.col
                        )
                    )
            return PPLErrorExpression(
                ErrorType.ParserException,
                f"Can't use {self.optype.ttype.get_name()} {self.expr.vtype.name}",
                Position(
                    self.optype.position.start_pos,
                    self.expr.value.position.end_pos,
                    self.expr.value.position.line,
                    self.expr.value.position.col
                )
            )
        return self

    def compile(self) -> List[Instr]:
        result: List[Instr] = []
        result += self.expr.compile()

        match self.optype.ttype:
            case TokenType.MINUS:
                result.append(Instr("UNARY_NEGATIVE"))

        return result

    def check_error(self) -> Expression | None:
        return self.expr.check_error()

    def output(self) -> str:
        return f"({self.expr1.output()} {self.optype.get_name()} {self.expr2.output()})"
