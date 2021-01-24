from unittest import TestCase
from typing import List, cast, Any, Tuple

from cantte.lexer import Lexer
from cantte.parser import Parser
from cantte.ast import (Program, LetStatement, ReturnStatement,
                        ExpressionStatement, Expression, Identifier,
                        Integer, Prefix, Infix, Boolean)


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

    def test_identifier_expression(self) -> None:
        source: str = 'foobar;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None

        self._test_literal_expression(expression_statement.expression, 'foobar')

    def test_integer_expression(self) -> None:
        source: str = '5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None
        self._test_literal_expression(expression_statement.expression, 5)

    def test_prefix_expression(self) -> None:
        source: str = '!5; -15;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program, expected_statements=2)

        for statement, (expected_operator, expected_value) in zip(program.statements, [('!', 5), ('-', 15)]):
            statement = cast(ExpressionStatement, statement)

            self.assertIsInstance(statement.expression, Prefix)

            prefix = cast(Prefix, statement.expression)

            self.assertEqual(prefix.operator, expected_operator)
            assert prefix.right is not None
            self._test_literal_expression(prefix.right, expected_value)

    def test_infix_expression(self) -> None:
        source: str = '''
            5 + 5;
            5 - 5;
            5 * 5;
            5 / 5;
            5 > 5;
            5 < 5;
            5 == 5;
            5 != 5;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program, expected_statements=8)

        expected_operators_and_values: List[Tuple[Any, str, Any]] = [
            (5, '+', 5),
            (5, '-', 5),
            (5, '*', 5),
            (5, '/', 5),
            (5, '>', 5),
            (5, '<', 5),
            (5, '==', 5),
            (5, '!=', 5),
        ]

        for statement, (expected_left, expected_operator, expected_right) in zip(
                program.statements, expected_operators_and_values):
            statement = cast(ExpressionStatement, statement)

            assert statement.expression is not None

            self.assertIsInstance(statement.expression, Infix)
            self._test_infix_expression(statement.expression, expected_left, expected_operator, expected_right)

    def test_boolean_expression(self) -> None:
        source: str = 'true; false;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program, expected_statements=2)

        expected_values: List[bool] = [True, False]

        for statement, expected_value in zip(program.statements, expected_values):
            expression_statement = cast(ExpressionStatement, statement)

            assert expression_statement.expression is not None

            self._test_literal_expression(expression_statement.expression, expected_value)

    def _test_boolean(self, expression: Expression, expected_value: bool) -> None:
        boolean = cast(Boolean, expression)

        self.assertEqual(boolean.value, expected_value)
        self.assertEqual(boolean.token.literal, 'true' if expected_value else 'false')

    def _test_infix_expression(self, expression: Expression, expected_left: Any,
                               expected_operator: str, expected_right: Any):
        infix = cast(Infix, expression)

        assert infix.left is not None
        self._test_literal_expression(infix.left, expected_left)

        self.assertEqual(infix.operator, expected_operator)

        assert infix.right is not None
        self._test_literal_expression(infix.right, expected_right)

    def _test_program_statements(self, parser: Parser, program: Program, expected_statements: int = 1) -> None:
        if parser.errors:
            print(parser.errors)

        self.assertEqual(len(parser.errors), 0)
        self.assertEqual(len(program.statements), expected_statements)
        self.assertIsInstance(program.statements[0], ExpressionStatement)

    def _test_literal_expression(self, expression: Expression, expected_value: Any) -> None:
        value_type = type(expected_value)

        if value_type == str:
            self._test_identifier(expression, expected_value)
        elif value_type == int:
            self._test_integer(expression, expected_value)
        elif value_type == bool:
            self._test_boolean(expression, expected_value)
        else:
            self.fail(f'Unhandled type of expression. Got={value_type}')

    def _test_identifier(self, expression: Expression, expected_value: str) -> None:
        self.assertIsInstance(expression, Identifier)

        identifier = cast(Identifier, expression)
        self.assertEqual(identifier.value, expected_value)
        self.assertEqual(identifier.token.literal, expected_value)

    def _test_integer(self, expression: Expression, expected_value: int) -> None:
        self.assertIsInstance(expression, Integer)

        integer = cast(Integer, expression)

        self.assertEqual(integer.value, expected_value)
        self.assertEqual(integer.token.literal, str(expected_value))
