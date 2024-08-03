from enum import Enum
from typing import List

from .. import Token, TokenType
from . import Expression

from bytecode import Instr


class ValueType(Enum):
    Integer = 0
    Float = 1
    Bool = 2
    String = 3
    Null = 4


class ValueExpression(Expression):
    value: Token
    vtype: ValueType

    def __init__(self, value: Token) -> None:
        self.value: Token = value
        match value.ttype:
            case TokenType.INT:
                self.vtype = ValueType.Integer
            case TokenType.FLOAT:
                self.vtype = ValueType.Float
            case TokenType.BOOL:
                self.vtype = ValueType.Bool
            case TokenType.STRING:
                self.vtype = ValueType.String
            case TokenType.NULL:
                self.vtype = ValueType.Null

    def optimize(self) -> Expression:
        if self.vtype == ValueType.Float:
            num = float(self.value.value)
            if num == int(num):
                self.vtype = ValueType.Integer
                self.value.value = str(int(num))
                self.value.ttype = TokenType.INT
        return self

    def compile(self) -> List[Instr]:
        match self.vtype:
            case ValueType.Integer: return [Instr("LOAD_CONST", int(self.value.value))]
            case ValueType.Float: return [Instr("LOAD_CONST", float(self.value.value))]
            case ValueType.Bool: return [Instr("LOAD_CONST", True if self.value.value == "True" else False)]
            case ValueType.String: return [Instr("LOAD_CONST", self.value.value)]
            case ValueType.Null: return [Instr("LOAD_CONST", None)]

    def check_error(self) -> Expression | None:
        return None

    def output(self) -> str:
        return f"({self.vtype.name} {self.value.value})"
