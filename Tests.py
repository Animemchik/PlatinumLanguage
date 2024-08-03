import unittest
from typing import List

from src.parser import *
from src.errors import *

from bytecode import Bytecode, Instr


class LexerTest(unittest.TestCase):
    def test_single_operators(self):
        code = "    \n+   \n\n -*/+ \t\r\n -+* \r\t\t\n /"  # in lexer it will look like "+-*/+-+*/"
        lexer: Lexer = Lexer(code)
        output: LexerOutput = lexer.tokenize()

        self.assertEqual(output.check_errors(), False)
        self.assertEqual(output.get_errors(), [])

        tokens: List[Token] = output.get_tokens()
        self.assertEqual(tokens[0].ttype, TokenType.PLUS)
        self.assertEqual(tokens[0].value, None)
        self.assertEqual(tokens[0].lexeme, "+")
        self.assertEqual(tokens[0].position, Position.from3(5, 2, 1))

        self.assertEqual(tokens[1].ttype, TokenType.MINUS)
        self.assertEqual(tokens[1].value, None)
        self.assertEqual(tokens[1].lexeme, "-")
        self.assertEqual(tokens[1].position, Position.from3(12, 4, 2))

        self.assertEqual(tokens[2].ttype, TokenType.STAR)
        self.assertEqual(tokens[2].value, None)
        self.assertEqual(tokens[2].lexeme, "*")
        self.assertEqual(tokens[2].position, Position.from3(12, 4, 2))

        self.assertEqual(tokens[3].ttype, TokenType.SLASH)
        self.assertEqual(tokens[3].value, None)
        self.assertEqual(tokens[3].lexeme, "/")
        self.assertEqual(tokens[3].position, Position.from3(14, 4, 4))

        self.assertEqual(tokens[4].ttype, TokenType.PLUS)
        self.assertEqual(tokens[4].value, None)
        self.assertEqual(tokens[4].lexeme, "+")
        self.assertEqual(tokens[4].position, Position.from3(15, 4, 5))

        self.assertEqual(tokens[5].ttype, TokenType.MINUS)
        self.assertEqual(tokens[5].value, None)
        self.assertEqual(tokens[5].lexeme, "-")
        self.assertEqual(tokens[5].position, Position.from3(21, 5, 2))

        self.assertEqual(tokens[6].ttype, TokenType.PLUS)
        self.assertEqual(tokens[6].value, None)
        self.assertEqual(tokens[6].lexeme, "+")
        self.assertEqual(tokens[6].position, Position.from3(22, 5, 3))

        self.assertEqual(tokens[7].ttype, TokenType.STAR)
        self.assertEqual(tokens[7].value, None)
        self.assertEqual(tokens[7].lexeme, "*")
        self.assertEqual(tokens[7].position, Position.from3(22, 5, 3))

        self.assertEqual(tokens[8].ttype, TokenType.SLASH)
        self.assertEqual(tokens[8].value, None)
        self.assertEqual(tokens[8].lexeme, "/")
        self.assertEqual(tokens[8].position, Position.from3(30, 6, 2))

    def test_various_operators(self):
        code = " ++ -- ** // > < >> << & | ^ && || == != >= <= () [] {}"

        lexer: Lexer = Lexer(code)
        output: LexerOutput = lexer.tokenize()

        self.assertEqual(output.check_errors(), False)
        self.assertEqual(output.get_errors(), [])

        tokens: List[Token] = output.get_tokens()

        self.assertEqual(tokens[0].ttype, TokenType.PLUSPLUS)
        self.assertEqual(tokens[0].value, None)
        self.assertEqual(tokens[0].lexeme, "++")
        self.assertEqual(tokens[0].position, Position(1, 3, 1, 2))

        self.assertEqual(tokens[1].ttype, TokenType.MINUSMINUS)
        self.assertEqual(tokens[1].value, None)
        self.assertEqual(tokens[1].lexeme, "--")
        self.assertEqual(tokens[1].position, Position(4, 6, 1, 5))

        self.assertEqual(tokens[2].ttype, TokenType.STARSTAR)
        self.assertEqual(tokens[2].value, None)
        self.assertEqual(tokens[2].lexeme, "**")
        self.assertEqual(tokens[2].position, Position(7, 9, 1, 8))

        self.assertEqual(tokens[3].ttype, TokenType.SLASHSLASH)
        self.assertEqual(tokens[3].value, None)
        self.assertEqual(tokens[3].lexeme, "//")
        self.assertEqual(tokens[3].position, Position(10, 12, 1, 11))

        self.assertEqual(tokens[4].ttype, TokenType.GT)
        self.assertEqual(tokens[4].value, None)
        self.assertEqual(tokens[4].lexeme, ">")
        self.assertEqual(tokens[4].position, Position.from3(13, 1, 14))

        self.assertEqual(tokens[5].ttype, TokenType.LT)
        self.assertEqual(tokens[5].value, None)
        self.assertEqual(tokens[5].lexeme, "<")
        self.assertEqual(tokens[5].position, Position.from3(15, 1, 16))

        self.assertEqual(tokens[6].ttype, TokenType.GTGT)
        self.assertEqual(tokens[6].value, None)
        self.assertEqual(tokens[6].lexeme, ">>")
        self.assertEqual(tokens[6].position, Position(17, 19, 1, 18))

        self.assertEqual(tokens[7].ttype, TokenType.LTLT)
        self.assertEqual(tokens[7].value, None)
        self.assertEqual(tokens[7].lexeme, "<<")
        self.assertEqual(tokens[7].position, Position(20, 22, 1, 21))

        self.assertEqual(tokens[8].ttype, TokenType.AMP)
        self.assertEqual(tokens[8].value, None)
        self.assertEqual(tokens[8].lexeme, "&")
        self.assertEqual(tokens[8].position, Position.from3(23, 1, 24))

        self.assertEqual(tokens[9].ttype, TokenType.BAR)
        self.assertEqual(tokens[9].value, None)
        self.assertEqual(tokens[9].lexeme, "|")
        self.assertEqual(tokens[9].position, Position.from3(25, 1, 26))

        self.assertEqual(tokens[10].ttype, TokenType.CARET)
        self.assertEqual(tokens[10].value, None)
        self.assertEqual(tokens[10].lexeme, "^")
        self.assertEqual(tokens[10].position, Position.from3(27, 1, 28))

        self.assertEqual(tokens[11].ttype, TokenType.AMPAMP)
        self.assertEqual(tokens[11].value, None)
        self.assertEqual(tokens[11].lexeme, "&&")
        self.assertEqual(tokens[11].position, Position(29, 31, 1, 30))

        self.assertEqual(tokens[12].ttype, TokenType.BARBAR)
        self.assertEqual(tokens[12].value, None)
        self.assertEqual(tokens[12].lexeme, "||")
        self.assertEqual(tokens[12].position, Position(32, 34, 1, 33))

        self.assertEqual(tokens[13].ttype, TokenType.EQEQ)
        self.assertEqual(tokens[13].value, None)
        self.assertEqual(tokens[13].lexeme, "==")
        self.assertEqual(tokens[13].position, Position(35, 37, 1, 36))

        self.assertEqual(tokens[14].ttype, TokenType.NOTEQ)
        self.assertEqual(tokens[14].value, None)
        self.assertEqual(tokens[14].lexeme, "!=")
        self.assertEqual(tokens[14].position, Position(38, 40, 1, 39))

        self.assertEqual(tokens[15].ttype, TokenType.GTEQ)
        self.assertEqual(tokens[15].value, None)
        self.assertEqual(tokens[15].lexeme, ">=")
        self.assertEqual(tokens[15].position, Position(41, 43, 1, 42))

        self.assertEqual(tokens[16].ttype, TokenType.LTEQ)
        self.assertEqual(tokens[16].value, None)
        self.assertEqual(tokens[16].lexeme, "<=")
        self.assertEqual(tokens[16].position, Position(44, 46, 1, 45))

        self.assertEqual(tokens[17].ttype, TokenType.LPAREN)
        self.assertEqual(tokens[17].value, None)
        self.assertEqual(tokens[17].lexeme, "(")
        self.assertEqual(tokens[17].position, Position.from3(47, 1, 48))

        self.assertEqual(tokens[18].ttype, TokenType.RPAREN)
        self.assertEqual(tokens[18].value, None)
        self.assertEqual(tokens[18].lexeme, ")")
        self.assertEqual(tokens[18].position, Position.from3(48, 1, 49))

        self.assertEqual(tokens[19].ttype, TokenType.LBRACE)
        self.assertEqual(tokens[19].value, None)
        self.assertEqual(tokens[19].lexeme, "[")
        self.assertEqual(tokens[19].position, Position.from3(50, 1, 51))

        self.assertEqual(tokens[20].ttype, TokenType.RBRACE)
        self.assertEqual(tokens[20].value, None)
        self.assertEqual(tokens[20].lexeme, "]")
        self.assertEqual(tokens[20].position, Position.from3(51, 1, 52))

        self.assertEqual(tokens[21].ttype, TokenType.LCURBRACE)
        self.assertEqual(tokens[21].value, None)
        self.assertEqual(tokens[21].lexeme, "{")
        self.assertEqual(tokens[21].position, Position.from3(53, 1, 54))

        self.assertEqual(tokens[22].ttype, TokenType.RCURBRACE)
        self.assertEqual(tokens[22].value, None)
        self.assertEqual(tokens[22].lexeme, "}")
        self.assertEqual(tokens[22].position, Position.from3(54, 1, 55))

    def test_numbers(self):
        code = "21312312\t\t\t1231.21\n21_4_1__2"  # in lexer it will look like "21312312   1231.21 21412"
        lexer: Lexer = Lexer(code)
        output: LexerOutput = lexer.tokenize()

        self.assertEqual(output.check_errors(), False)
        self.assertEqual(output.get_errors(), [])

        tokens: List[Token] = output.get_tokens()
        self.assertEqual(tokens[0].ttype, TokenType.INT)
        self.assertEqual(tokens[0].value, "21312312")
        self.assertEqual(tokens[0].lexeme, "21312312")
        self.assertEqual(tokens[0].position, Position(0, 8, 1, 1))

        self.assertEqual(tokens[1].ttype, TokenType.FLOAT)
        self.assertEqual(tokens[1].value, "1231.21")
        self.assertEqual(tokens[1].lexeme, "1231.21")
        self.assertEqual(tokens[1].position, Position(11, 18, 1, 12))

        self.assertEqual(tokens[2].ttype, TokenType.INT)
        self.assertEqual(tokens[2].value, "21412")
        self.assertEqual(tokens[2].lexeme, "21_4_1__2")
        self.assertEqual(tokens[2].position, Position(19, 28, 2, 1))

    def test_operators_after_numbers(self):
        code = "999 + 1512_- 124"  # in lexer it will look like "999 + 1512 - 124"
        lexer: Lexer = Lexer(code)
        output: LexerOutput = lexer.tokenize()

        self.assertEqual(output.check_errors(), False)
        self.assertEqual(output.get_errors(), [])

        tokens: List[Token] = output.get_tokens()

        self.assertEqual(tokens[0].ttype, TokenType.INT)
        self.assertEqual(tokens[0].value, "999")
        self.assertEqual(tokens[0].lexeme, "999")
        self.assertEqual(tokens[0].position, Position(0, 3, 1, 1))

        self.assertEqual(tokens[1].ttype, TokenType.PLUS)
        self.assertEqual(tokens[1].value, None)
        self.assertEqual(tokens[1].lexeme, "+")
        self.assertEqual(tokens[1].position, Position(4, 4, 1, 5))

        self.assertEqual(tokens[2].ttype, TokenType.INT)
        self.assertEqual(tokens[2].value, "1512")
        self.assertEqual(tokens[2].lexeme, "1512_")
        self.assertEqual(tokens[2].position, Position(6, 11, 1, 7))

        self.assertEqual(tokens[3].ttype, TokenType.MINUS)
        self.assertEqual(tokens[3].value, None)
        self.assertEqual(tokens[3].lexeme, "-")
        self.assertEqual(tokens[3].position, Position(11, 11, 1, 12))

        self.assertEqual(tokens[4].ttype, TokenType.INT)
        self.assertEqual(tokens[4].value, "124")
        self.assertEqual(tokens[4].lexeme, "124")
        self.assertEqual(tokens[4].position, Position(13, 16,1, 14))

    def test_numbers_errors(self):
        code = "2131.2.312 217_945.3125.7899.312__552.3086"
        lexer: Lexer = Lexer(code)
        output: LexerOutput = lexer.tokenize()

        errors: List[PPLError] = output.get_errors()
        self.assertEqual(output.check_errors(), True)

        self.assertTrue(isinstance(errors[0], PPLSyntaxError))
        self.assertEqual(errors[0].text, "invalid syntax. Perhaps you forgot a comma?")
        self.assertEqual(errors[0].position, Position(0, 10, 1, 1))

        code = "217_945.3125.7899.312__552.3086"
        lexer: Lexer = Lexer(code)
        output: LexerOutput = lexer.tokenize()

        errors: List[PPLError] = output.get_errors()
        self.assertEqual(output.check_errors(), True)

        self.assertTrue(isinstance(errors[0], PPLSyntaxError))
        self.assertEqual(errors[0].text, "invalid syntax. Perhaps you forgot a comma?")
        self.assertEqual(errors[0].position, Position(0, 31, 1, 1))


class ParserTest(unittest.TestCase):
    def test_no_statement(self):
        code = ""

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        self.assertEqual(parser_output.get_result_statement().output(), AST.BlockStatement([]).output())

    def test_value_expression(self):
        code = "2131.2"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        expected = AST.BlockStatement([
            AST.ExpressionStatement(
                AST.ValueExpression(
                    Token(TokenType.FLOAT, "2131.2", "2131.2", Position(0, 6, 1, 1))
                )
            )
        ])
        self.assertEqual(parser_output.get_result_statement().output(), expected.output())
        self.assertEqual(parser_output.get_result_statement().optimize().output(), expected.optimize().output())

    def test_value_expression1(self):
        code = "2131.2+2131.2"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        expected = AST.BlockStatement([
            AST.ExpressionStatement(
                AST.AdditiveExpression(
                    TokenType.PLUS,
                    AST.ValueExpression(
                        Token(TokenType.FLOAT, "2131.2", "2131.2", Position(0, 6, 1, 1))
                    ),
                    AST.ValueExpression(
                        Token(TokenType.FLOAT, "2131.2", "2131.2", Position(7, 13, 1, 8))
                    )
                )
            )
        ])

        self.assertEqual(parser_output.get_result_statement().output(), expected.optimize().output())

    def test_unary_compiler(self):
        code = "-124.0 * 16"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], -124.0 * 16)

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().optimize().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], -124.0 * 16)

    def test_multiplicative_compiler(self):
        code = "124.0 * 16.251 // 1412 % 53 ** 2 * 341 / 125"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 124.0 * 16.251 // 1412 % 53 ** 2 * 341 / 125)

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().optimize().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 124.0 * 16.251 // 1412 % 53 ** 2 * 341 / 125)

    def test_additive_compiler(self):
        code = "124.0+ 864 - 135.12516 + 16.251"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 124.0 + 864 - 135.12516 + 16.251)

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().optimize().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 124.0 + 864 - 135.12516 + 16.251)

    def test_shift_errors(self):
        code = "124.2 >> 16"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), True)
        self.assertEqual(
            parser_output.get_errors()[0],
            PPLParseException(
                "There is no implementation of right shift operator with Float",
                Position(0, 11, 1, 1)
            )
        )

        code = "124.0 >> 16"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 124 >> 16)

    def test_shift_compiler(self):
        code = "124 >> 16"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 124 >> 16)

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().optimize().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 124 >> 16)

    def test_conditional_compiler(self):
        code = "124 >> 16 > 1"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 124 >> 16 > 1)

    def test_equality_compiler(self):
        code = "124 >> 16 == 124 >> 16"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], True)

        code = "124 >> 16 != 124 << 16"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], True)

        code = "124 >> 16 is not 124 << 16"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), True)
        self.assertEqual(
            parser_output.get_errors()[0],
            PPLSyntaxWarning(
                "\"is not\" with 'Integer' literal. Did you mean \"!=\"?",
                Position(0, 26, 1, 1)
            )
        )

        code = "124 >> 16 is 124 >> 16"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), True)
        self.assertEqual(
            parser_output.get_errors()[0],
            PPLSyntaxWarning(
                "\"is\" with 'Integer' literal. Did you mean \"==\"?",
                Position(0, 22, 1, 1)
            )
        )

    def test_bitwise_compiler(self):
        code = "124 & 121 | 12 ^ 21"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 124 & 121 | 12 ^ 21)

    def test_logical_compiler(self):
        code = "True xor False"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], True)

    def test_null_coalesce_compiler(self):
        code = "null ?? (125 ?? 12)"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 125)

        code = "null ?? (null ?? null)"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], None)

    def test_ternary_compiler(self):
        code = "124 << 16 > 1 ? 214"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 214)

    def QQEWRQtest_compiler(self):
        code = "124.0 + (16.251 // 1412 % -53) ** 2 * (+341 - 124) * 125"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 124.0 + (16.251 // 1412 % -53) ** 2 * (+341 - 124) * 125)

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().optimize().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 124.0 + (16.251 // 1412 % -53) ** 2 * (+341 - 124) * 125)

    def test_compiler_errors(self):
        code = "124.0 + 153"

        lexer: Lexer = Lexer(code)
        lexer_output: LexerOutput = lexer.tokenize()

        parser: Parser = Parser(lexer_output.get_tokens())
        parser_output: ParserOutput = parser.parse()

        self.assertEqual(lexer_output.check_errors(), False)
        self.assertEqual(lexer_output.get_errors(), [])

        self.assertEqual(parser_output.check_errors(), False)
        self.assertEqual(parser_output.get_errors(), [])

        bytecode = ([
                       Instr("RESUME", 0)
                   ] + parser_output.get_result_statement().compile() +
                   [
                        Instr("STORE_NAME", "result"),
                        Instr("LOAD_CONST", None),
                        Instr("RETURN_VALUE")
                   ])
        result = {}
        exec(Bytecode(bytecode).to_code(), result)
        self.assertEqual(result["result"], 277)
        self.assertNotEqual(str(result["result"]), str(277.0))


unittest.main(exit = False)
