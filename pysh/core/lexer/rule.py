from dataclasses import dataclass

from pysh.core.errors import Errorable
from pysh.core.regex import Regex, State
from pysh.core.tokens import Token


@dataclass(frozen=True)
class Rule(Errorable):
    name: str
    regex: Regex

    @staticmethod
    def for_str(name: str, value: None | str | Regex = None) -> "Rule":
        match value:
            case None:
                return Rule(name, Regex.for_str(name))
            case str():
                return Rule(name, Regex.for_str(value))
            case Regex():
                return Rule(name, value)

    def __call__(self, state: str | State) -> tuple[State, Token]:
        state, result = self._try(
            lambda: self.regex(state),
            "failed to apply regex",
        )
        value, position = self._try(
            lambda: (result.value(), result.position()),
            f"failed to extract token data from regex result {result}",
        )
        return state, Token(self.name, value, position)
