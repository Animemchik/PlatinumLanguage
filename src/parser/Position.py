class Position:
    """
    This class is used to mark positions of tokens, statements and errors.

    Location "src/parser/Position.py"
    """
    start_pos: int
    end_pos: int
    line: int
    col: int

    @staticmethod
    def from3(pos: int, line: int, col: int):
        return Position(pos, pos, line, col)

    def __init__(self, start_pos: int, end_pos: int, line: int, col: int) -> None:
        """
        :param start_pos: The start position
        :param end_pos: The end position
        :param line: The line
        :param col: The column
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.line = line
        self.col = col

    def __repr__(self) -> str:
        return f"start_pos: {self.start_pos}, end_pos: {self.end_pos}, line: {self.line}, col: {self.col}"

    def __eq__(self, other):
        return self.start_pos == other.start_pos and \
               self.end_pos == other.end_pos and \
               self.line == other.line and \
               self.col == other.col
