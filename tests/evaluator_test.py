from typing import cast, List, Tuple, Any
from unittest import TestCase

from cantte.ast import Program
from cantte.evaluator import evaluate, NULL
from cantte.lexer import Lexer
from cantte.object import Integer, Object, Boolean, Error, Environment
from cantte.parser import Parser


class EvaluatorTest(TestCase):

    def test_integer_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('5', 5),
            ('10', 10),
            ('-5', -5),
            ('-10', -10),
            ('5 + 5', 10),
            ('5 - 10', -5),
            ('2 * 2 * 2 * 2', 16),
            ('2 * 5 - 3', 7),
            ('(2 + 7) / 3', 3)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_boolean_evaluation(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('true', True),
            ('false', False),
            ('1 < 2', True),
            ('1 > 2', False),
            ('1 < 1', False),
            ('1 > 1', False),
            ('1 == 1', True),
            ('1 != 1', False),
            ('1 != 2', True),
            ('true == true', True),
            ('true == false', False),
            ('false == false', True),
            ('false == true', False),
            ('(1 < 2) == true', True),
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

    def test_if_else_evaluation(self) -> None:
        tests: List[Tuple[str, Any]] = [
            ('if (true) { 10 }', 10),
            ('if (false) { 10 }', None),
            ('if (1) { 10 }', 10),
            ('if (1 < 2) { 10 }', 10),
            ('if (1 < 2) { 10 } else { 20 }', 10),
            ('if (1 > 2) { 10 } else { 20 }', 20),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            if type(expected) == int:
                self._test_integer_object(evaluated, expected)
            else:
                self._test_null_object(evaluated)

    def test_return_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('return 10;', 10),
            ('return 10; 9;', 10),
            ('return 2 * 5; 9;', 10),
            ('9; return 3 * 6; 9;', 18),
            ('''
                if (10 > 1) {
                    if (20 > 10) {
                        return 1;
                    }
                    
                    return 0;
                }
            ''', 1),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_error_handling(self) -> None:
        tests: List[Tuple[str, str]] = [
            ('5 + true', 'Type mismatch: INTEGER + BOOLEAN'),
            ('5 + true; 9;', 'Type mismatch: INTEGER + BOOLEAN'),
            ('-true', 'Unknown operator: -BOOLEAN'),
            ('false + true', 'Unknown operator: BOOLEAN + BOOLEAN'),
            ('false - true; 10;', 'Unknown operator: BOOLEAN - BOOLEAN'),
            ('''
                if (10 > 7) {
                    return true + false;
                }
            ''', 'Unknown operator: BOOLEAN + BOOLEAN'),
            ('''
                if (10 > 7) {
                    return true * false;
                }
            ''', 'Unknown operator: BOOLEAN * BOOLEAN'),
            ('''
                if (10 > 7) {
                    return true / false;
                }
            ''', 'Unknown operator: BOOLEAN /'
                 ' BOOLEAN'),
            ('foobar;', 'Unknown identifier: foobar')
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            self.assertIsInstance(evaluated, Error)

            evaluated = cast(Error, evaluated)

            self.assertEqual(evaluated.message, expected)

    def test_assigment_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('let a = 5; a;', 5),
            ('let a = 5 * 5; a;', 25),
            ('let a = 5; let b = a; b;', 5),
            ('let a = 5; let b = a; let c = a + b + 5; c;', 15),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def _test_null_object(self, evaluated: Object) -> None:
        self.assertEqual(evaluated, NULL)

    @staticmethod
    def _evaluate_tests(source: str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()
        env: Environment = Environment()

        evaluated = evaluate(program, env)

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
