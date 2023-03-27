import abc


class LifeCyclePlugin(abc.ABC):
    @abc.abstractmethod
    def scopes(self) -> list['CompileLifeCycleStatus']:
        return []

    @abc.abstractmethod
    def on(self, compileLifeCycle: 'CompileLifeCycle'):
        pass
