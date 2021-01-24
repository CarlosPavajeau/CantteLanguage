from typing import cast, List, Tuple
from unittest import TestCase

from cantte.ast import Program
from cantte.evaluator import evaluate
from cantte.lexer import Lexer
from cantte.object import Integer, Object, Boolean
from cantte.parser import Parser


class EvaluatorTest(TestCase):

    def test_integer_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('5', 5),
            ('10', 10),
            ('-5', -5),
            ('-10', -10)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_boolean_evaluation(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('true', True),
            ('false', False)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_bang_operator(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('!true', False),
            ('!false', True),
            ('!!true', True),
            ('!!false', False),
            ('!5', False),
            ('!!5', True)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)



    @staticmethod
    def _evaluate_tests(source: str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        evaluated = evaluate(program)

        assert evaluated is not None

        return evaluated

    def _test_boolean_object(self, evaluated: Object, expected: bool) -> None:
        self.assertIsInstance(evaluated, Boolean)

        evaluated = cast(Boolean, evaluated)

        self.assertEqual(evaluated.value, expected)

    def _test_integer_object(self, evaluated: Object, expected: int) -> None:
        self.assertIsInstance(evaluated, Integer)

        evaluated = cast(Integer, evaluated)

        self.assertEqual(evaluated.value, expected)

