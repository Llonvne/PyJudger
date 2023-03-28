import abc

from Entities import RunnerRequest


class Runner(abc.ABC):

    @abc.abstractmethod
    def run(self, runnerRequest: RunnerRequest):
        pass

    @abc.abstractmethod
    def get_version(self) -> str:
        pass
