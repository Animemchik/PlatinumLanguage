import enum
from typing import List

from . import Expression
from .. import Position
from ...errors import PPLParseException, PPLSyntaxWarning

from bytecode import Instr


class ErrorType(enum.Enum):
    SyntaxWarning = 0,
    ParserException = 1


def get_error_class(error_type: ErrorType):
    match error_type:
        case ErrorType.SyntaxWarning: return PPLSyntaxWarning
        case ErrorType.ParserException: return PPLParseException


class PPLErrorExpression(Expression):
    text: str
    position: Position

    def __init__(self, error_type: ErrorType, text: str, position: Position) -> None:
        self.error_type = error_type
        self.text = text
        self.position = position

    def optimize(self) -> Expression:
        return self

    def compile(self) -> List[Instr]:
        return []

    def check_error(self) -> Expression | None:
        return self

    def to_exception(self) -> PPLParseException:
        return get_error_class(self.error_type)(self.text, self.position)

    def output(self) -> str:
        return PPLParseException(self.text, self.position).output()
