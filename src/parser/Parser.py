from typing import List

from . import Token, TokenType, Position
from .AST import *
from ..errors import PPLError, PPLParseException


class ParserOutput:
    """
    Output class for Parser
    It is returned after using Parser.parse()
    """
    result_statement: Statement
    errors: List[PPLError]

    def __init__(self, result_statement: Statement, errors: List[PPLError]):
        self.result_statement = result_statement
        self.errors = errors

    def check_errors(self) -> bool:
        return self.errors != []

    def get_result_statement(self) -> Statement:
        return self.result_statement

    def get_errors(self) -> List[PPLError]:
        return self.errors


class Parser:
    result_statement: BlockStatement
    errors: List[PPLError]
    tokens: List[Token]
    tokens_len: int
    pos: int

    def __init__(self, tokens: List[Token]):
        self.result_statement = BlockStatement()
        self.tokens = tokens
        self.tokens_len = len(tokens)
        self.pos = 0

        self.errors = []

    def parse(self) -> ParserOutput:
        while not self.is_at_end() and self.errors == []:
            statement = self.parse_statement()

            if self.errors:
                break

            statement = statement.optimize()
            statement_error = statement.check_error()

            if isinstance(statement_error, PPLErrorExpression):
                self.errors.append(statement_error.to_exception())

            self.result_statement.add(statement)

        return ParserOutput(self.result_statement, self.errors)

    def parse_statement(self) -> Statement:
        # if self.match(TokenType.PRINT):
        #     return self.print_statement(self.expression())

        # if self.match(TokenType.PRINTLN):
        #     return self.println_statement(self.expression())

        # if self.match(TokenType.IF):
        #     return self.if_else_statement()

        # if self.match(TokenType.WHILE):
        #     return self.while_statement()

        # if self.match(TokenType.FOR):
        #     return self.for_statement()

        # if self.match(TokenType.BREAK):
        #     return self.break_statement()

        # if self.match(TokenType.CONTINUE):
        #     return self.continue_statement()

        # if self.match(TokenType.FUNC):
        #     return self.function_define_statement()

        # if self.match(TokenType.RETURN):
        #     return self.return_statement(self.expression())

        # if self.look_match(TokenType.WORD) and self.look_match(TokenType.LPAREN, 1):
        #     return self.expr_statement(functionChain(qualifiedName()))

        # if self.match(TokenType.SWITCH):
        #     return self.match_statement()

        # if self.match(TokenType.CLASS):
        #     return self.class_declaration_statement()

        # if self.match(TokenType.ENUM):
        #     return self.enum_statement()

        # if self.match(TokenType.USING):
        #     return self.using_statement(self.expression())

        # if self.match(TokenType.TRY):
        #     return self.try_catch_statement()

        # if self.match(TokenType.THROW):
        #     return self.throw_statement()

        # if self.look_match(TokenType.IDENTIFIER) and self.peek().value in self.macros:
        #     return self.macro_usage_statement()

        # if self.match(TokenType.ASSERT):
        #     return self.assert_statement(self.expression())

        # if self.match(TokenType.MACRO):
        #     return self.macro_statement()

        return self.assignment_statement()

    def assignment_statement(self) -> Statement:
        expression = self.expression()
        if expression:
            return ExpressionStatement(expression)
        self.errors.append(PPLParseException("Unknown statement: " + self.peek().ttype.name))

    def expression(self) -> Expression:
        expr = self.assignment()

        if isinstance(expr, PPLErrorExpression):
            self.errors.append(expr.to_exception())

        return expr

    def assignment(self) -> Expression:
        # TODO!
        # assignment: Expression = self.assignment_strict()
        # if assignment:
        #     return assignment

        return self.ternary()

    def ternary(self) -> Expression:
        result = self.null_coalesce()

        while True:
            if self.match(TokenType.QUEST):
                result1 = self.expression()
                if self.match(TokenType.COLON):
                    result = TernaryExpression(result, result1, self.expression())
                else:
                    result = TernaryExpression(result, result1, None)
                continue
            break
        return result

    def null_coalesce(self) -> Expression:
        result = self.logical_or()

        while True:
            if self.match(TokenType.QUESTQUEST):
                result = NullCoalesceExpression(TokenType.QUESTQUEST, result, self.logical_or())
                continue
            break
        return result

    def logical_or(self) -> Expression:
        result = self.logical_xor()

        while True:
            if self.match(TokenType.BARBAR):
                result = LogicalExpression(TokenType.BARBAR, result, self.logical_xor())
                continue
            elif self.match(TokenType.OR):
                result = LogicalExpression(TokenType.AND, result, self.logical_xor())
                continue
            break
        return result

    def logical_xor(self) -> Expression:
        result = self.logical_and()

        while True:
            if self.match(TokenType.XOR):
                result = LogicalExpression(TokenType.XOR, result, self.logical_and())
                continue
            break
        return result

    def logical_and(self) -> Expression:
        result = self.bitwise_or()

        while True:
            if self.match(TokenType.AMPAMP):
                result = LogicalExpression(TokenType.AMPAMP, result, self.bitwise_or())
                continue
            elif self.match(TokenType.AND):
                result = LogicalExpression(TokenType.AND, result, self.bitwise_or())
                continue
            break
        return result

    def bitwise_or(self) -> Expression:
        result = self.bitwise_xor()

        while True:
            if self.match(TokenType.BAR):
                result = BitwiseExpression(TokenType.BAR, result, self.bitwise_xor())
                continue
            break
        return result

    def bitwise_xor(self) -> Expression:
        result = self.bitwise_and()

        while True:
            if self.match(TokenType.CARET):
                result = BitwiseExpression(TokenType.CARET, result, self.bitwise_and())
                continue
            break
        return result

    def bitwise_and(self) -> Expression:
        result = self.equality()

        while True:
            if self.match(TokenType.AMP):
                result = BitwiseExpression(TokenType.AMP, result, self.equality())
                continue
            break
        return result

    def equality(self) -> Expression:
        result = self.conditional()

        while True:
            if self.match(TokenType.EQEQ):
                result = EqualityExpression(TokenType.EQEQ, result, self.conditional())
                continue
            elif self.match(TokenType.NOTEQ):
                result = EqualityExpression(TokenType.NOTEQ, result, self.conditional())
                continue
            elif self.match(TokenType.IS):
                if self.match(TokenType.NOT):
                    result = EqualityExpression(TokenType.NOT, result, self.conditional())
                    continue
                result = EqualityExpression(TokenType.IS, result, self.conditional())
                continue
            break
        return result

    def conditional(self) -> Expression:
        result = self.shift()

        while True:
            if self.match(TokenType.GT):
                result = ConditionalExpression(TokenType.GT, result, self.shift())
                continue
            elif self.match(TokenType.GTEQ):
                result = ConditionalExpression(TokenType.GTEQ, result, self.shift())
                continue
            elif self.match(TokenType.LT):
                result = ConditionalExpression(TokenType.LT, result, self.shift())
                continue
            elif self.match(TokenType.LTEQ):
                result = ConditionalExpression(TokenType.LTEQ, result, self.shift())
                continue
            break
        return result

    def shift(self) -> Expression:
        result = self.additive()

        while True:
            if self.match(TokenType.LTLT):
                result = ShiftExpression(TokenType.LTLT, result, self.additive())
                continue
            elif self.match(TokenType.GTGT):
                result = ShiftExpression(TokenType.GTGT, result, self.additive())
                continue
            break
        return result

    def additive(self) -> Expression:
        result = self.multiplicative()

        while True:
            if self.match(TokenType.PLUS):
                result = AdditiveExpression(TokenType.PLUS, result, self.multiplicative())
                continue
            elif self.match(TokenType.MINUS):
                result = AdditiveExpression(TokenType.MINUS, result, self.multiplicative())
                continue
            break
        return result

    def multiplicative(self) -> Expression:
        result = self.unary()

        while True:
            if self.match(TokenType.STAR):
                result = MultiplicativeExpression(TokenType.STAR, result, self.unary())
                continue
            elif self.match(TokenType.SLASH):
                result = MultiplicativeExpression(TokenType.SLASH, result, self.unary())
                continue
            elif self.match(TokenType.SLASHSLASH):
                result = MultiplicativeExpression(TokenType.SLASHSLASH, result, self.unary())
                continue
            elif self.match(TokenType.PERCENT):
                result = MultiplicativeExpression(TokenType.PERCENT, result, self.unary())
                continue
            elif self.match(TokenType.STARSTAR):
                result = MultiplicativeExpression(TokenType.STARSTAR, result, self.unary())
                continue
            break
        return result

    def unary(self) -> Expression:
        if self.match(TokenType.PLUS):
            return UnaryExpression(self.peek(-1), self.primary())
        elif self.match(TokenType.MINUS):
            return UnaryExpression(self.peek(-1), self.primary())

        return self.primary()

    def primary(self) -> Expression:
        if self.match(TokenType.LPAREN):
            result = self.expression()
            self.consume(TokenType.RPAREN)
            return result

        return self.variable()

    def variable(self) -> Expression:
        # TODO!
        return self.value()

    def value(self) -> Expression:
        token: Token = self.peek()

        if self.match(TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL, TokenType.NULL):
            return ValueExpression(token)

        self.errors.append(PPLParseException(f"Unknown expression: {token.ttype.get_name()}", token.position))

    def consume(self, ttype: TokenType) -> None:
        if self.peek().ttype == ttype:
            self.next()
        else:
            position = self.peek().position
            self.errors.append(
                PPLParseException(
                    f"There should be {ttype.to_article()} {ttype.get_name()}",
                    Position.from3(position.end_pos, position.line, position.col)
                )
            )

    def look_match(self, ttype: TokenType, relative: int = 0) -> bool:
        if self.peek(relative).ttype == ttype:
            return True
        return False

    def match(self, *ttype: TokenType) -> bool:
        if self.peek().ttype in ttype:
            self.next()
            return True
        return False

    def next(self) -> Token:
        self.pos += 1
        return self.peek()

    def peek(self, relative: int = 0) -> Token:
        if self.is_at_end(relative):
            return Token.from3(TokenType.EOF, "EOF", Position(-1, -1, -1, -1))

        return self.tokens[self.pos + relative]

    def is_at_end(self, relative: int = 0) -> bool:
        return self.pos + relative >= self.tokens_len or self.tokens[self.pos + relative].ttype == TokenType.EOF
