from unittest import TestCase
from typing import List, cast

from cantte.lexer import Lexer
from cantte.parser import Parser
from cantte.ast import Program, LetStatement, ReturnStatement


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

        names: List[str] = []
        for statement in program.statements:
            statement = cast(LetStatement, statement)

            assert statement.name is not None

            names.append(statement.name.value)

        expected_names: List[str] = ['x', 'y', 'foo']

        self.assertEqual(names, expected_names)

    def test_parse_errors(self) -> None:
        source: str = 'let x 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(parser.errors), 1)

    def test_return_statement(self) -> None:
        source: str = '''
            return 5;
            return foo;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 2)
        for statement in program.statements:
            self.assertEqual(statement.token_literal(), 'return')
            self.assertIsInstance(statement, ReturnStatement)
