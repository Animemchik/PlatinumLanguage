from . import PPLError
from ..parser import Position


class PPLParseException(PPLError):
    text: str
    position: Position

    def __init__(self, text: str, position: Position = None):
        self.text = text
        self.position = position

    def set_position(self, position: Position) -> None:
        self.position = position

    def __eq__(self, other: 'PPLParseException') -> bool:
        return (self.text, self.position) == (other.text, other.position)

    def output(self) -> str:
        return f"ParseException: {self.text}"
