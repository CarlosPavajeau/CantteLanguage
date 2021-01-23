from unittest import TestCase
from typing import List

from cantte.lexer import Lexer
from cantte.parser import Parser
from cantte.ast import Program, LetStatement


class ParserTest(TestCase):

    def test_parse_program(self) -> None:
        source: str = 'let x = 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)

    def test_let_statements(self) -> None:
        source: str = '''
            let x = 5;
            let y = 10;
            let foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 3)

        statements: List[LetStatement] = []
        for statement in program.statements:
            self.assertEqual(statement.token_literal(), 'let')
            self.assertIsInstance(statement, LetStatement)
            statements.append(statement)

        self.assertEqual(statements[0].name.value, 'x')
        self.assertEqual(statements[1].name.value, 'y')
        self.assertEqual(statements[2].name.value, 'foo')
