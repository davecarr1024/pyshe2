from abc import ABC, abstractmethod
from functools import cache
import string
from typing import Iterable, Optional, Sequence, cast, final, overload, override
from pysh.core.errors import Error, Errorable
from pysh.core.regex.result import Result
from pysh.core.regex.state import State


class Regex(ABC, Errorable):
    class ParseError(Error): ...

    @staticmethod
    def for_str(input: str) -> "Regex":
        from pysh.core.parser import Parser
        from pysh.core.lexer import Rule
        from pysh.core.regex import (
            And,
            Literal,
            Range,
            ZeroOrMore,
            OneOrMore,
            ZeroOrOne,
            Or,
        )

        operators: Sequence[str] = "()[-]^*+?\\"
        literal_lexrule: Rule = Rule.for_str(
            "literal", Regex.class_(operators, "operators").not_()
        )

        def literal_str(value: str) -> Rule:
            return Rule.for_str(value, Regex.literal(value))

        def to_and(children: Sequence[Regex]) -> Regex:
            match len(children):
                case 0:
                    raise Regex.ParseError(msg=f"empty regex from {repr(input)}")
                case 1:
                    return children[0]
                case _:
                    return And.for_children(*children)

        @cache
        def literal() -> Parser[Regex]:
            return Parser.head(literal_lexrule).value().transform(Literal)

        @cache
        def range() -> Parser[Regex]:
            return (
                literal_str("[")
                & Parser.head(literal_lexrule).value().param("min")
                & literal_str("-")
                & Parser.head(literal_lexrule).value().param("max")
                & literal_str("]")
            ).object(Range)

        @cache
        def unary_operand() -> Parser[Regex]:
            return literal() | range()

        @cache
        def zero_or_more() -> Parser[Regex]:
            return (unary_operand() & literal_str("*")).transform(ZeroOrMore)

        @cache
        def one_or_more() -> Parser[Regex]:
            return (unary_operand() & literal_str("+")).transform(OneOrMore)

        @cache
        def zero_or_one() -> Parser[Regex]:
            return (unary_operand() & literal_str("?")).transform(ZeroOrOne)

        @cache
        def unary_operation() -> Parser[Regex]:
            return zero_or_more() | one_or_more() | zero_or_one()

        @cache
        def operand() -> Parser[Regex]:
            return unary_operand() | operation()

        @cache
        def and_() -> Parser[Regex]:
            return (
                literal_str("(") & operand().one_or_more() & literal_str(")")
            ).transform(to_and)

        @cache
        def operation() -> Parser[Regex]:
            return unary_operation() | and_()

        @cache
        def regex() -> Parser[Regex]:
            return operand().until_empty().transform(to_and)

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
