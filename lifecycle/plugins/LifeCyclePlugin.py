import abc
from typing import TypeVar

T = TypeVar('T')


class LifeCyclePlugin(abc.ABC):
    @abc.abstractmethod
    def scopes(self) -> list[T]:
        return []

    @abc.abstractmethod
    def on(self, lifeCycle: T):
        pass
