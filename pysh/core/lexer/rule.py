from dataclasses import dataclass
from typing import override

from pysh.core.errors import Errorable
from pysh.core.regex import Regex, State
from pysh.core.tokens import Token


@dataclass(frozen=True)
class Rule(Errorable):
    name: str
    regex: Regex
    include: bool = True

    @override
    def __str__(self) -> str:
        def apply_include(s: str) -> str:
            return s if self.include else f"~{s}"

        if self.name == str(self.regex):
            return apply_include(self.name)
        else:
            return apply_include(f"{self.name}({self.regex})")

    @staticmethod
    def for_str(
        name: str,
        value: None | str | Regex = None,
        include: bool = True,
    ) -> "Rule":
        match value:
            case None:
                return Rule(name, Regex.for_str(name), include)
            case str():
                return Rule(name, Regex.for_str(value), include)
            case Regex():
                return Rule(name, value, include)

    def __call__(self, state: str | State) -> tuple[State, Token, bool]:
        state, result = self._try(
            lambda: self.regex(state),
            "failed to apply regex",
        )
        value, position = self._try(
            lambda: (result.value(), result.position()),
            f"failed to extract token data from regex result {result}",
        )
        return state, Token(self.name, value, position), self.include
