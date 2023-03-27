from enum import Enum

from Entities import RunnerRequest
from abstract.Runner import Runner


class RunnerLifeCycleStatus(Enum):
    pass


class RunnerLifeCycle:
    def __init__(self, request: RunnerRequest, runnerSupplier: lambda: Runner):
        self.request = request
        self.runnerSupplier = runnerSupplier
