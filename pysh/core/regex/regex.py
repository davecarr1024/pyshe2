from abc import ABC, abstractmethod
import string
from typing import Iterable, Optional, Sequence, final, overload, override
from pysh.core.errors import Error, Errorable
from pysh.core.regex.result import Result
from pysh.core.regex.state import State


class Regex(ABC, Errorable):
    class ParseError(Error): ...

    @staticmethod
    def for_str(input: str) -> "Regex":
        from pysh.core.parser import Parser
        from pysh.core.regex import And, Literal

        operators: Sequence[str] = "()[]^*+?\\"

        def literal() -> Parser[Literal]:
            return (
                Parser.head("literal", Regex.class_(operators, "operators").not_())
                .value()
                .transform(Literal)
            )

        def regex() -> Parser[Regex]:
            def to_and(children: Sequence[Regex]) -> Regex:
                match len(children):
                    case 0:
                        raise Regex.ParseError(msg=f"empty regex from {repr(input)}")
                    case 1:
                        return children[0]
                    case _:
                        return And.for_children(*children)

            return literal().until_empty().transform(to_and)

        try:
            _, result = regex()(input)
        except Parser.Error as error:
            raise Regex.ParseError(
                msg=f"failed to parse regex {repr(input)}",
                children=[error],
            ) from error
        return result

    @abstractmethod
    def _apply(self, state: State) -> tuple[State, Result]: ...

    @override
    @final
    def __str__(self) -> str:
        return self._str(0)

    @abstractmethod
    def _str(self, depth: int) -> str: ...

    def __call__(self, state: str | State) -> tuple[State, Result]:
        match state:
            case State():
                return self._apply(state)
            case str():
                return self._apply(State.for_str(state))

    @staticmethod
    def literal(value: str) -> "literal.Literal":
        return literal.Literal(value)

    @staticmethod
    def any() -> "any.Any":
        return any.Any()

    @staticmethod
    def class_(
        values: Iterable[str],
        display: Optional[str] = None,
    ) -> "class_.Class":
        return class_.Class(frozenset(values), display)

    @staticmethod
    def digits() -> "class_.Class":
        return Regex.class_(string.digits, r"\d")

    @staticmethod
    def whitespace() -> "class_.Class":
        return Regex.class_(string.whitespace, r"\w")

    @staticmethod
    def range(min: str, max: str) -> "range.Range":
        return range.Range(min, max)

    def zero_or_more(self) -> "Regex":
        from pysh.core.regex.zero_or_more import ZeroOrMore

        return ZeroOrMore(self)

    def one_or_more(self) -> "Regex":
        from pysh.core.regex.one_or_more import OneOrMore

        return OneOrMore(self)

    def zero_or_one(self) -> "Regex":
        from pysh.core.regex.zero_or_one import ZeroOrOne

        return ZeroOrOne(self)

    def __and__(self, rhs: "Regex") -> "Regex":
        from pysh.core.regex.and_ import And

        match rhs:
            case And():
                return And.for_children(self, *rhs)
            case Regex():
                return And.for_children(self, rhs)

    def __or__(self, rhs: "Regex") -> "Regex":
        from pysh.core.regex.or_ import Or

        match rhs:
            case Or():
                return Or.for_children(self, *rhs)
            case Regex():
                return Or.for_children(self, rhs)


from . import literal, any, class_, range
