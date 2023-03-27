import abc
import subprocess

from Entities import RunnerRequest


class Runner(abc.ABC):

    @abc.abstractmethod
    def run(self, runnerRequest: RunnerRequest):
        pass
