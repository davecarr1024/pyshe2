from dataclasses import dataclass
from typing import Callable, Optional, override
from pysh.core.errors import error


class Errorable:
    @dataclass(kw_only=True)
    class Error(error.Error):
        obj: "Errorable"

        @override
        def _str_line(self) -> str:
            return f"{self.obj}: {super()._str_line()}"

    def _error(
        self,
        msg: Optional[str] = None,
        *children: error.Error,
    ) -> Error:
        return self.Error(
            msg=msg,
            children=list(children),
            obj=self,
        )

    def _try[T](self, func: Callable[[], T], message: Optional[str] = None) -> T:
        try:
            return func()
        except error.Error as error_:
            raise self._error(message, error_)
