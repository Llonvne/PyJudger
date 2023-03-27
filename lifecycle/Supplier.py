import abc
from typing import TypeVar, Generic

T = TypeVar('T')


class Supplier(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def get(self) -> T:
        pass
