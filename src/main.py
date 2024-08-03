from parser import Lexer

code = ("+ -   \n "        
        "+-+-")

lexer = Lexer(code)
print(lexer.tokenize().check_errors())
print(lexer.tokenize().get_tokens())
print(lexer.tokenize().get_errors())
