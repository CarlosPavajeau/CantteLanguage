from re import match
from cantte.token import TokenType, Token


class Lexer:
    def __init__(self, source: str) -> None:
        self._source: str = source
        self._character: str = ''
        self._read_position: int = 0
        self._position: int = 0

        self._read_character()

    def next_token(self) -> Token:
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
        elif match(r'^\{$', self._character):
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

    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ''
        else:
            self._character = self._source[self._read_position]

        self._position = self._read_position
        self._read_position += 1
