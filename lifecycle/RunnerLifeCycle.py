from enum import Enum
from typing import Callable

from Entities import RunnerRequest
from abstract.Runner import Runner
from lifecycle.plugins.LifeCyclePlugin import LifeCyclePlugin


class RunnerLifeCycleStatus(Enum):
    RunnerRequestReceived = 0
    PrepareTester = 1
    AwaitingRunning = 2
    PreparingRunningEnvironment = 3
    RunningInProgress = 4
    CompleteRunning = 5
    AnswerChecking = 6
    ExecuteHTTPResponse = 7
    End = 8


class RunnerLifeCycle:
    def __init__(self, request: RunnerRequest,
                 runnerSupplier: lambda: Runner = None,
                 pathIndicator: Callable[[], str] = None
                 ):
        self.status = RunnerLifeCycleStatus.RunnerRequestReceived
        self.__listeners: [list[Callable]] = [[] for i in range(9)]

        self.request = request
        self.runnerSupplier = runnerSupplier
        self.runner = None
        self.result = None

    def startLifeCycle(self):
        for i in range(9):
            self.status = RunnerLifeCycleStatus(i)
            for listeners in self.__listeners[i]:
                for listener in listeners:
                    listener(self)
            if i == 3:
                self.runner = self.runnerSupplier()
            if i == 4:
                self.runner.run(self.runnerSupplier)
        return self.doResponse()

    def addStatusListener(self, status: RunnerLifeCycleStatus,
                          listener: Callable) -> 'RunnerLifeCycle':
        self.__listeners[status.value].append(listener)
        return self

    def addPlugin(self, plugin: LifeCyclePlugin) -> 'RunnerLifeCycle':
        for scope in plugin.scopes():
            self.__listeners[scope.value].append(lambda x: plugin.on(x))
        return self

    def doResponse(self):
        return {
            "submission_id": self.request.submission_id,
            "status": "OK",
            "result": self.result,
        }
