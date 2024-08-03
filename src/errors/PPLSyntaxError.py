from . import PPLError
from ..parser import Position


class PPLSyntaxError(PPLError):
    text: str
    position: Position

    def __init__(self, text: str, position: Position = None):
        self.text = text
        self.position = position

    def set_position(self, position: Position) -> None:
        self.position = position

    def output(self) -> str:
        return f"SyntaxError: {self.text}"
