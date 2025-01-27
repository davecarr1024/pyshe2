from dataclasses import dataclass
from typing import Self, override

from pysh.core.lexer import Lexer, Rule
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary
from pysh.core.regex import Regex
from pysh.core.tokens import Token


@dataclass(frozen=True)
class Head(Parser[Token]):
    rule: Rule

    @override
    def _str(self, depth: int) -> str:
        return str(self.rule)

    @classmethod
    def for_str(cls, name: str, value: None | str | Regex = None) -> Self:
        return cls(Rule.for_str(name, value))

    @override
    def _lexer(self) -> Lexer:
        return Lexer.for_rules(self.rule)

    @override
    def _apply(self, state: State) -> tuple[State, Token]:
        head, tail = self._try(
            lambda: (state.head(), state.tail()),
            f"expected {self} got empty stream",
        )
        if head.type != self.rule.name:
            raise self._error(f"expected {self} got {head}")
        return tail, head

    def value(self) -> "Head.Value":
        return self.Value(self)

    @dataclass(frozen=True)
    class Value(Unary[str, Token]):
        @override
        def _str(self, depth: int) -> str:
            return f"{self.child}.value()"

        @override
        def _apply(self, state: State) -> tuple[State, str]:
            state, child_result = self._apply_child(state)
            return state, child_result.value
