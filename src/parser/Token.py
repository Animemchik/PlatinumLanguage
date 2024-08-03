from typing import Optional, Dict, List
from enum import Enum

from . import Position


class TokenType(Enum):
    INT = 0
    FLOAT = 1
    STRING = 2
    IDENTIFIER = 3
    BOOL = 4
    NULL = 5

    PLUS = 10        # +
    MINUS = 11       # -
    STAR = 12        # *
    SLASH = 13       # /
    PERCENT = 14     # %
    EQ = 15          # =

    PLUSPLUS = 20    # ++
    MINUSMINUS = 21  # --
    STARSTAR = 22    # **
    SLASHSLASH = 23  # //

    GT = 31          # >
    LT = 32          # <
    GTGT = 33        # >>
    LTLT = 34        # <<
    AMP = 35         # &
    BAR = 36         # |
    CARET = 37       # ^

    AMPAMP = 41      # &&
    BARBAR = 42      # ||
    EQEQ = 43        # ==
    NOTEQ = 44       # !=
    GTEQ = 45        # >=
    LTEQ = 46        # <=
    EXCL = 47        # !

    QUEST = 48       # ?
    QUESTQUEST = 49  # ??
    COLON = 50       # :
    SEMICOLON = 50   # ;

    LPAREN = 60      # (
    RPAREN = 61      # )
    LBRACE = 62      # [
    RBRACE = 63      # ]
    LCURBRACE = 64   # {
    RCURBRACE = 65   # }

    IS = 100
    NOT = 101

    AND = 102
    XOR = 103
    OR = 104

    EOF = -1

    def to_article(self) -> str:
        article_map: Dict[str, List['TokenType']] = {
            "an": [
                self.INT, self.IDENTIFIER,
                self.PLUSPLUS,
                self.AMP,
                self.AMPAMP, self.BARBAR, self.EQEQ, self.EXCL,
                self.IS,
                self.AND, self.OR,
                self.EOF
            ],
            "a": [
                self.FLOAT, self.STRING, self.BOOL, self.NULL,
                self.PLUS, self.MINUS, self.STAR, self.SLASH, self.PERCENT,
                self.MINUSMINUS, self.STARSTAR, self.SLASHSLASH,
                self.GT, self.LT, self.GTGT, self.LTLT, self.BAR, self.CARET,
                self.NOTEQ, self.GTEQ, self.LTEQ,
                self.QUEST, self.QUESTQUEST,
                self.LPAREN, self.RPAREN, self.LBRACE, self.RBRACE, self.LCURBRACE, self.RCURBRACE,
                self.NOT,
                self.XOR,
            ]
        }
        for article, tokens in article_map.items():
            if self in tokens:
                return article

    def get_name(self) -> str:
        token_map = {
            self.INT: "integer",
            self.FLOAT: "float",
            self.STRING: "string",
            self.IDENTIFIER: "identifier",
            self.BOOL: "bool",
            self.NULL: "null",

            self.PLUS: "plus",
            self.MINUS: "minus",
            self.STAR: "star",
            self.SLASH: "slash",
            self.PERCENT: "percent",

            self.PLUSPLUS: "increment",
            self.MINUSMINUS: "decrement",
            self.STARSTAR: "power",
            self.SLASHSLASH: "floor divide",

            self.GT: "greater than",
            self.LT: "lower than",
            self.GTGT: "right shift",
            self.LTLT: "left shift",
            self.AMP: "ampersand",
            self.BAR: "bar",
            self.CARET: "caret",

            self.AMPAMP: "and operator",
            self.BARBAR: "or operator",
            self.EQEQ: "equal operator",
            self.NOTEQ: "not equal operator",
            self.GTEQ: "greater equal",
            self.LTEQ: "lower equal",
            self.EXCL: "exclamation mark",

            self.QUEST: "question mark",
            self.QUESTQUEST: "null coalesce operator",

            self.LPAREN: "left paren",
            self.RPAREN: "right paren",
            self.LBRACE: "left brace",
            self.RBRACE: "right brace",
            self.LCURBRACE: "left curly brace",
            self.RCURBRACE: "right curly brace",

            self.IS: "is operator",
            self.NOT: "not operator",
            self.AND: "and word operator",
            self.XOR: "xor word operator",
            self.OR: "or word operator",

            self.EOF: "end of file"
        }
        return token_map[self]


class Token:
    """
    Token class represents a lexeme that will be converted to statement in Parser
    """
    ttype: TokenType
    value: Optional[str]
    lexeme: str
    position: Position

    @staticmethod
    def from3(ttype: TokenType, lexeme: str, position: Position) -> 'Token':
        """
        :param ttype: Token type
        :param lexeme: Lexeme
        :param position: Position of Token in code
        """
        return Token(ttype, None, lexeme, position)

    def __init__(self, ttype: TokenType, value: str, lexeme: str, position: Position) -> None:
        """
        :param ttype: Token type
        :param value: The value of Token
        :param lexeme: Lexeme
        :param position: Position of Token in code
        """
        self.ttype = ttype
        self.value = value
        self.lexeme = lexeme
        self.position = position

    def __repr__(self) -> str:
        """
        This is a debug function
        """
        return f"{self.ttype.name}"
