from abc import ABC, abstractmethod
from typing import Iterable, Self, Sized


class AbstractStream[T](ABC, Sized, Iterable[T]):
    @abstractmethod
    def head(self) -> T: ...

    @abstractmethod
    def tail(self) -> Self: ...
