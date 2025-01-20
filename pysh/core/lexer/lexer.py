from dataclasses import dataclass, field
from typing import (
    FrozenSet,
    Iterable,
    Iterator,
    MutableSequence,
    Self,
    Sized,
    Union,
    override,
)

from pysh.core.errors import Errorable
from pysh.core.lexer.result import Result
from pysh.core.lexer.rule import Rule
from pysh.core.regex import State
from pysh.core.tokens import Token


@dataclass(frozen=True)
class Lexer(Errorable, Sized, Iterable[Rule]):
    rules: FrozenSet[Rule] = field(default_factory=frozenset)

    @override
    def __len__(self) -> int:
        return len(self.rules)

    @override
    def __iter__(self) -> Iterator[Rule]:
        return iter(self.rules)

    @classmethod
    def for_rules(cls, *rules: Rule) -> Self:
        return cls(frozenset(rules))

    def _apply_any_rule(self, state: str | State) -> tuple[State, Token]:
        errors: MutableSequence[Rule.Error] = []
        for rule in self:
            try:
                return rule(state)
            except Rule.Error as error:
                errors.append(error)
        raise self._error(f"failed to apply any rule to {state}", *errors)

    def __call__(self, state: str | State) -> Result:
        if isinstance(state, str):
            state = State.for_str(state)
        result = Result()
        while not state.empty():
            state, token = self._apply_any_rule(state)
            result += token
        return result

    def _with_rules(self, *rules: Rule) -> Self:
        return self.for_rules(*(frozenset(self) | frozenset(rules)))

    def __or__(self, rhs: Union["Lexer", Rule]) -> "Lexer":
        match rhs:
            case Lexer():
                return self._with_rules(*rhs)
            case Rule():
                return self._with_rules(rhs)

    def __ror__(self, lhs: Rule) -> "Lexer":
        return self.for_rules(lhs)._with_rules(*self)
