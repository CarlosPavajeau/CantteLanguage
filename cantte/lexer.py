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
            ident_literal: str = self._read_identifier()
            token_type = lookup_token_type(ident_literal)
            token = Token(token_type, ident_literal)
        elif self._is_number(self._character):
            num_literal: str = self._read_number()
            token = Token(TokenType.INT, num_literal)
        else:
            token_type = self._get_token_type()
            if token_type == TokenType.EQUAL or token_type == TokenType.NOT_EQUAL:
                token = self._make_two_character_token(token_type)
            elif token_type == TokenType.STRING:
                literal = self._read_string()

                token = Token(token_type, literal)
            else:
                token = Token(token_type, self._character)
            self._read_character()

        return token

    def _get_token_type(self):
        if match(r'^=$', self._character):
            if self._peek_character() == '=':
                token_type = TokenType.EQUAL
            else:
                token_type = TokenType.ASSIGN
        elif match(r'^\+$', self._character):
            token_type = TokenType.PLUS
        elif match(r'^-$', self._character):
            token_type = TokenType.MINUS
        elif match(r'^\*$', self._character):
            token_type = TokenType.MULTIPLICATION
        elif match(r'^/$', self._character):
            token_type = TokenType.DIVISION
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
        elif match(r'^<$', self._character):
            token_type = TokenType.LESS_THAN
        elif match(r'^>$', self._character):
            token_type = TokenType.GREATER_THAN
        elif match(r'^!$', self._character):
            if self._peek_character() == '=':
                token_type = TokenType.NOT_EQUAL
            else:
                token_type = TokenType.NEGATION
        elif match(r"^\"|'$", self._character):
            token_type = TokenType.STRING
        else:
            token_type = TokenType.ILLEGAL

        return token_type

    @staticmethod
    def _is_letter(character: str) -> bool:
        return bool(match(r'^[a-zA-ZñÑ_]$', character))

    @staticmethod
    def _is_number(character: str) -> bool:
        return bool(match(r'^\d$', character))

    def _make_two_character_token(self, token_type: TokenType) -> Token:
        prefix = self._character
        self._read_character()
        suffix = self._character

        return Token(token_type, f'{prefix}{suffix}')

    def _peek_character(self) -> str:
        if self._read_position >= len(self._source):
            return ''
        return self._source[self._read_position]

    def _read_identifier(self) -> str:
        initial_position = self._position

        while self._is_letter(self._character) or self._is_number(self._character):
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

    def _read_string(self) -> str:
        quote_type = self._character

        self._read_character()

        initial_position = self._position
        while (self._character != quote_type) \
                and self._read_position <= len(self._source):
            self._read_character()

        string = self._source[initial_position:self._position]

        return string

    def _skip_whitespace(self) -> None:
        while match(r'^\s$', self._character):
            self._read_character()
