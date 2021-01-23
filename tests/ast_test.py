from unittest import TestCase

from cantte.ast import Identifier, LetStatement, Program, ReturnStatement
from cantte.token import Token, TokenType


class ASTTest(TestCase):

    def test_let_statement(self) -> None:
        program: Program = Program(statements=[
            LetStatement(
                token=Token(TokenType.LET, 'let'),
                name=Identifier(
                    token=Token(TokenType.IDENTIFIER, 'num'),
                    value='num'
                ),
                value=Identifier(
                    token=Token(TokenType.IDENTIFIER, 'other'),
                    value='other'
                )
            )
        ])

        program_str = str(program)

        self.assertEqual(program_str, 'let num = other;')

    def test_return_statement(self) -> None:
        program: Program = Program(statements=[
            ReturnStatement(
                token=Token(TokenType.RETURN, 'return'),
                return_value=Identifier(
                    token=Token(TokenType.RETURN, 'return'),
                    value='num'
                )
            )
        ])

        program_str = str(program)

        self.assertEqual(program_str, 'return num;')
