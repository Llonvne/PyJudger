from enum import Enum
from typing import Callable

from Entities import CompilerRequest
from abstract.Compiler import Compiler
from lifecycle.plugins.LifeCyclePlugin import LifeCyclePlugin


class CompileError(Exception):
    pass


class CompileLifeCycleStatus(Enum):
    CompilationRequestReceived = 0
    CheckingDataLegitimacy = 1
    AwaitingCompilation = 2
    PreparingCompilationEnvironment = 3
    CompilationInProgress = 4
    CompleteCompilation = 5
    ExecuteHTTPResponse = 6
    End = 7


class CompileLifeCycle:
    def __init__(self, request: CompilerRequest, compilerSupplier: Callable[[], Compiler], source_file: str = None,
                 target_file: str = None):
        self.status = CompileLifeCycleStatus.CompilationRequestReceived
        self.request = request
        self.compilerSupplier = compilerSupplier
        self.__listeners: [list[Callable[['CompileLifeCycle'], None]]] = [[] for i in range(8)]
        self.source_file = source_file
        self.target_file = target_file
        self.compiler = None
        self.result = None

    def startLifeCycle(self):
        for i in range(8):
            for listener in self.__listeners[i]:
                listener(self)
            if i == 3:
                self.compiler = self.compilerSupplier()
            if i == 4:
                if self.source_file is None:
                    raise CompileError("source path is None")
                if self.target_file is None:
                    raise CompileError("target path is None")
                self.result = self.compiler.compiler(self.request.code, self.source_file, self.target_file)
        return self.doResponse()

    def addStatusListener(self, status: CompileLifeCycleStatus,
                          listener: Callable[['CompileLifeCycle'], None]) -> 'CompileLifeCycle':
        self.__listeners[status.value].append(listener)
        return self

    def addPlugin(self, plugin: LifeCyclePlugin) -> 'CompileLifeCycle':
        for scope in plugin.scopes():
            self.__listeners[scope.value].append(
                lambda x: plugin.on(x)
            )
        return self

    def doResponse(self):
        return {
            "submission_id": self.request.submission_id,
            "is_ok": "self.result.isOk",
            "message": "self.result.message"
        }
