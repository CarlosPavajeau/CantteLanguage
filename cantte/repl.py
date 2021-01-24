from typing import List

from cantte.ast import Program
from cantte.lexer import Lexer
from cantte.token import Token, TokenType
from cantte.parser import Parser
from cantte.evaluator import evaluate


EOF_TOKEN: Token = Token(TokenType.EOF, '')


def _print_parse_errors(errors: List[str]):
    for error in errors:
        print(error)


def start_repl() -> None:
    while (source := input('>> ')) != 'exit()':
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        if len(parser.errors) > 0:
            _print_parse_errors(parser.errors)
            continue

        evaluated = evaluate(program)

        if evaluated is not None:
            print(evaluated.inspect())
