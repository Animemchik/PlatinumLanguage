from typing import List, Literal

from . import Token, TokenType, Position
from ..errors import *

OPERATORS = "+-*/%<>&|^?!()[]{}=;:"
KEYWORDS = {
    "is": TokenType.IS,
    "not": TokenType.NOT,

    "and": TokenType.AND,
    "xor": TokenType.XOR,
    "or": TokenType.OR,

    "True": TokenType.BOOL,
    "False": TokenType.BOOL,
    "null": TokenType.NULL,
}


def is_number(s: str) -> bool:
    """
    Checks that the character is a number
    :param s: A character
    :return: True if character is a number
    """
    return s in "0123456789"


def is_identifier_part(s: str) -> bool:
    """
    Checks that the character is an identifier part
    :param s: A character
    :return: True if character is an identifier part
    """
    return s.isidentifier() or s in "0123456789"


class LexerOutput:
    """
    Output class for Lexer
    It is returned after using Lexer.tokenize()
    """
    tokens: List[Token]
    errors: List[PPLError]

    def __init__(self, tokens: List[Token], errors: List[PPLError]):
        self.tokens = tokens
        self.errors = errors

    def check_errors(self) -> bool:
        return self.errors != []

    def get_tokens(self) -> List[Token]:
        return self.tokens

    def get_errors(self) -> List[PPLError]:
        return self.errors


class Lexer:
    tokens: List[Token]
    errors: List[PPLError]
    code: str
    code_len: int
    pos: int
    line: int
    col: int

    def __init__(self, code: str, tokens = None) -> None:
        if tokens is None:
            tokens = []
        self.code = code
        self.code_len = len(code)
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = tokens
        self.errors = []

    def tokenize(self) -> LexerOutput:
        while not self.is_at_end() and self.errors == []:
            current: str = self.peek()
            if current in OPERATORS:
                self.tokenize_operators()
            elif is_number(current):
                self.tokenize_digit()
            elif current.isidentifier():
                self.tokenize_identifier()
            else:
                # TODO!!! WARNS
                # if current not in '\n\t\r ':
                #     self.errors.append(
                #         PPLSyntaxError("invalid syntax", Position.from3(start_pos, self.line, start_col))
                #     )
                current = self.next()

        self.add_eof()
        return LexerOutput(self.tokens, self.errors)

    def tokenize_operators(self) -> None:
        start_pos = self.pos
        start_col = self.col
        line = self.line

        if self.match('+'):
            if self.match('+'):
                self.add_token(TokenType.PLUSPLUS, "++", Position(start_pos, self.pos, line, start_col))
            else:
                self.add_token(TokenType.PLUS, "+", Position.from3(start_pos, line, start_col))
        elif self.match('-'):
            if self.match('-'):
                self.add_token(TokenType.MINUSMINUS, "--", Position(start_pos, self.pos, line, start_col))
            else:
                self.add_token(TokenType.MINUS, "-", Position.from3(start_pos, line, start_col))
        elif self.match('='):
            if self.match('='):
                self.add_token(TokenType.EQEQ, "==", Position(start_pos, self.pos, line, start_col))
            else:
                self.add_token(TokenType.EQ, "=", Position.from3(start_pos, line, start_col))
        if self.match('!'):
            if self.match('='):
                self.add_token(TokenType.NOTEQ, "!=", Position(start_pos, self.pos, line, start_col))
            else:
                self.add_token(TokenType.EXCL, "!", Position.from3(start_pos, line, start_col))
        elif self.match('>'):
            if self.match('>'):
                self.add_token(TokenType.GTGT, ">>", Position(start_pos, self.pos, line, start_col))
            elif self.match('='):
                self.add_token(TokenType.GTEQ, ">=", Position(start_pos, self.pos, line, start_col))
            else:
                self.add_token(TokenType.GT, ">", Position.from3(start_pos, line, start_col))
        elif self.match('<'):
            if self.match('<'):
                self.add_token(TokenType.LTLT, "<<", Position(start_pos, self.pos, line, start_col))
            elif self.match('='):
                self.add_token(TokenType.LTEQ, "<=", Position(start_pos, self.pos, line, start_col))
            else:
                self.add_token(TokenType.LT, "<", Position.from3(start_pos, line, start_col))
        elif self.match('*'):
            if self.match('*'):
                self.add_token(TokenType.STARSTAR, "**", Position(start_pos, self.pos, line, start_col))
            else:
                self.add_token(TokenType.STAR, "*", Position.from3(start_pos, line, start_col))
        elif self.match('/'):
            if self.match('/'):
                self.add_token(TokenType.SLASHSLASH, "//", Position(start_pos, self.pos, line, start_col))
            else:
                self.add_token(TokenType.SLASH, "/", Position.from3(start_pos, line, start_col))
        elif self.match('%'):
            self.add_token(TokenType.PERCENT, "%", Position.from3(start_pos, line, start_col))
        elif self.match('&'):
            if self.match('&'):
                self.add_token(TokenType.AMPAMP, "&&", Position(start_pos, self.pos, line, start_col))
            else:
                self.add_token(TokenType.AMP, "&", Position.from3(start_pos, line, start_col))
        elif self.match('|'):
            if self.match('|'):
                self.add_token(TokenType.BARBAR, "||", Position(start_pos, self.pos, line, start_col))
            else:
                self.add_token(TokenType.BAR, "|", Position.from3(start_pos, line, start_col))
        elif self.match('?'):
            if self.match('?'):
                self.add_token(TokenType.QUESTQUEST, "??", Position(start_pos, self.pos, line, start_col))
            else:
                self.add_token(TokenType.QUEST, "?", Position.from3(start_pos, line, start_col))
        elif self.match(':'):
            self.add_token(TokenType.COLON, ":", Position.from3(start_pos, line, start_col))
        elif self.match(';'):
            self.add_token(TokenType.SEMICOLON, ";", Position.from3(start_pos, line, start_col))
        elif self.match('^'):
            self.add_token(TokenType.CARET, "^", Position.from3(start_pos, line, start_col))
        elif self.match('('):
            self.add_token(TokenType.LPAREN, "(", Position.from3(start_pos, line, start_col))
        elif self.match(')'):
            self.add_token(TokenType.RPAREN, ")", Position.from3(start_pos, line, start_col))
        elif self.match('['):
            self.add_token(TokenType.LBRACE, "[", Position.from3(start_pos, line, start_col))
        elif self.match(']'):
            self.add_token(TokenType.RBRACE, "]", Position.from3(start_pos, line, start_col))
        elif self.match('{'):
            self.add_token(TokenType.LCURBRACE, "{", Position.from3(start_pos, line, start_col))
        elif self.match('}'):
            self.add_token(TokenType.RCURBRACE, "}", Position.from3(start_pos, line, start_col))

    def tokenize_digit(self) -> None:
        start_pos = self.pos
        start_col = self.col
        current = self.peek()
        builder = ""
        has_dot = False
        error = None
        while True:
            if current == '.':
                if has_dot:
                    if error is None:
                        error = PPLSyntaxError("invalid syntax. Perhaps you forgot a comma?")
                has_dot = True
            elif current == '_':
                current = self.next()
                continue
            elif not is_number(current):
                break
            builder += current
            current = self.next()

        if error is not None:
            error.set_position(Position(start_pos, self.pos, self.line - self.line_offset(), start_col))
            self.errors.append(error)
        else:
            self.add_full_token(
                TokenType.FLOAT if has_dot else TokenType.INT,
                builder,
                self.code[start_pos:self.pos],
                Position(start_pos, self.pos, self.line - self.line_offset(), start_col)
            )

    def tokenize_identifier(self) -> None:
        start_pos = self.pos
        start_col = self.col
        current = self.peek()
        builder = ""

        while True:
            if is_identifier_part(current):
                builder += current
            else:
                break
            current = self.next()

        self.add_full_token(
            KEYWORDS[builder] if builder in KEYWORDS else TokenType.IDENTIFIER,
            builder,
            self.code[start_pos:self.pos],
            Position(start_pos, self.pos, self.line - self.line_offset(), start_col)
        )

    def line_offset(self) -> Literal[0, 1]:
        """
        Returns an offset if peeked character is a new line char
        :return: Offset 0 or 1
        """
        return 0 if self.peek() != '\n' else 1

    def match(self, char: str) -> bool:
        if self.peek() == char:
            self.next()
            return True
        return False

    def next(self) -> str:
        self.pos += 1
        char: str = self.peek()
        if char == '\n':
            self.line += 1
            self.col = 0
        else:
            self.col += 1
        return char

    def peek(self, relative: int = 0) -> str:
        if self.is_at_end(relative):
            return '\0'

        return self.code[self.pos + relative]

    def is_at_end(self, relative: int = 0) -> bool:
        return self.pos + relative >= self.code_len

    def add_full_token(self, ttype: TokenType, value: str, lexeme: str, position: Position) -> None:
        self.tokens.append(Token(ttype, value, lexeme, position))

    def add_token(self, ttype: TokenType, lexeme: str, position: Position) -> None:
        self.tokens.append(Token.from3(ttype, lexeme, position))

    def add_eof(self) -> None:
        self.tokens.append(Token.from3(TokenType.EOF, "EOF", Position(-1, -1, -1, -1)))
