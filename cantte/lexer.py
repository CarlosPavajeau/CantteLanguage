from re import match
from cantte.token import TokenType, Token, lookup_token_type


class Lexer:
    def __init__(self, source: str) -> None:
        self._source: str = source
        self._character: str = ''
        self._read_position: int = 0
        self._position: int = 0

        self._read_character()

    def next_token(self) -> Token:
        self._skip_whitespace()

        if self._is_letter(self._character):
            literal: str = self._read_identifier()
            token_type = lookup_token_type(literal)
            token = Token(token_type, literal)
        elif self._is_number(self._character):
            literal: str = self._read_number()
            token = Token(TokenType.INT, literal)
        else:
            token_type = self._get_token_type()
            token = Token(token_type, self._character)
            self._read_character()

        return token

    def _get_token_type(self):
        if match(r'^=$', self._character):
            token_type = TokenType.ASSIGN
        elif match(r'^\+$', self._character):
            token_type = TokenType.PLUS
        elif match(r'^$', self._character):
            token_type = TokenType.EOF
        elif match(r'^\($', self._character):
            token_type = TokenType.LPAREN
        elif match(r'^\)$', self._character):
            token_type = TokenType.RPAREN
        elif match(r'^{$', self._character):
            token_type = TokenType.LBRACE
        elif match(r'^}$', self._character):
            token_type = TokenType.RBRACE
        elif match(r'^,$', self._character):
            token_type = TokenType.COMMA
        elif match(r'^;$', self._character):
            token_type = TokenType.SEMICOLON
        else:
            token_type = TokenType.ILLEGAL

        return token_type

    @staticmethod
    def _is_letter(character: str) -> bool:
        return bool(match(r'^[a-zA-ZñÑ_]$', character))

    @staticmethod
    def _is_number(character: str) -> bool:
        return bool(match(r'^\d$', character))

    def _read_identifier(self) -> str:
        initial_position = self._position

        while self._is_letter(self._character):
            self._read_character()

        return self._source[initial_position:self._position]

    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ''
        else:
            self._character = self._source[self._read_position]

        self._position = self._read_position
        self._read_position += 1

    def _read_number(self) -> str:
        initial_position = self._position

        while self._is_number(self._character):
            self._read_character()

        return self._source[initial_position:self._position]

    def _skip_whitespace(self) -> None:
        while match(r'^\s$', self._character):
            self._read_character()
