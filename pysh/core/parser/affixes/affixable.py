from dataclasses import dataclass, field, replace
from typing import Optional, Self, override

from pysh.core.lexer import Lexer
from pysh.core.parser.affixes.abstract_affixable import AbstractAffixable
from pysh.core.parser.parser import Parser


@dataclass(frozen=True)
class Affixable[Result](AbstractAffixable[Result]):
    _prefix_value: Optional[Parser] = field(kw_only=True, default=None)
    _suffix_value: Optional[Parser] = field(kw_only=True, default=None)

    @override
    def _prefix(self) -> Parser | None:
        return self._prefix_value

    @override
    def _suffix(self) -> Parser | None:
        return self._suffix_value

    def _with_prefix(self, prefix: Parser) -> Self:
        return replace(self, _prefix_value=prefix)

    def _with_suffix(self, suffix: Parser) -> Self:
        return replace(self, _suffix_value=suffix)
