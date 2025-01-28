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
    def __str__(self) -> str:
        return f"Lexer({', '.join(str(rule) for rule in self)})"

    @override
    def __len__(self) -> int:
        return len(self.rules)

    @override
    def __iter__(self) -> Iterator[Rule]:
        return iter(self.rules)

    @classmethod
    def for_rules(cls, *rules: Rule) -> Self:
        return cls(frozenset(rules))

    def _apply_any_rule(self, state: str | State) -> tuple[State, Token, bool]:
        errors: MutableSequence[Rule.Error] = []
        results: MutableSequence[tuple[State, Token, bool]] = []
        for rule in self:
            try:
                results.append(rule(state))
            except Rule.Error as error:
                errors.append(error)
        match len(results):
            case 0:
                raise self._error(f"failed to apply any rule to {state}", *errors)
            case 1:
                return results[0]
            case _:
                raise self._error(
                    f"ambiguous lex for {state}: {[token for _, token, _ in results]}"
                )

    def __call__(self, state: str | State) -> Result:
        if isinstance(state, str):
            state = State.for_str(state)
        result = Result()
        while not state.empty():
            state, token, include = self._apply_any_rule(state)
            if include:
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
