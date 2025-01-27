from abc import abstractmethod
from typing import Optional, final, override
from pysh.core.lexer import Lexer
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State


class AbstractAffixable[Result](Parser[Result]):
    def _prefix(self) -> Optional[Parser]: ...

    def _suffix(self) -> Optional[Parser]: ...

    @abstractmethod
    def _apply_in_affixes(self, state: State) -> tuple[State, Result]: ...

    @override
    @final
    def _apply(self, state: State) -> tuple[State, Result]:
        prefix = self._prefix()
        if prefix is not None:
            state, _ = prefix._apply(state)
        state, result = self._apply_in_affixes(state)
        suffix = self._suffix()
        if suffix is not None:
            state, _ = suffix._apply(state)
        return state, result

    @override
    def lexer(self) -> Lexer:
        lexer = Lexer()
        prefix = self._prefix()
        if prefix is not None:
            lexer |= prefix.lexer()
        suffix = self._suffix()
        if suffix is not None:
            lexer |= suffix.lexer()
        return lexer
