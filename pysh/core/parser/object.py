from dataclasses import dataclass
from typing import Any, Sequence, override

from pysh.core.lexer import Lexer
from pysh.core.parser import arg
from pysh.core.parser.args import Args
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State


@dataclass(frozen=True)
class Object[Object](Parser[Object]):
    args: Args[Object]
    object: Object

    @override
    def _apply(self, state: State) -> tuple[State, Object]:
        setters: Sequence[arg.Setter[Object, Any]]
        state, setters = self._try(lambda: self.args._apply(state))
        object: Object = self.object
        for setter in setters:
            object = self._try(lambda: setter(object))
        return state, object

    @override
    def _str(self, depth: int) -> str:
        return f"Object({self.args},{self.object})"

    @override
    def lexer(self) -> Lexer:
        return self.args.lexer()
