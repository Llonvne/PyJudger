from enum import Enum

from Entities import CompilerRequest
from abstract.Compiler import Compiler
from lifecycle.Checker import Checker
from lifecycle.Supplier import Supplier


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
    def __init__(self, request: CompilerRequest, compilerSupplier: Supplier[Compiler], dataChecker: Checker = None):
        self.status = CompileLifeCycleStatus.CompilationRequestReceived
        self.request = request
        self.compilerSupplier = compilerSupplier
        self.dataChecker = dataChecker

    def startLifeCycle(self, source_file, target_file):
        self.AfterReceivedCompilationRequest()
        self.BeforeCheckingLegitimacy()
        if self.dataChecker is not None:
            self.dataChecker.check(self.request)
        self.BeforePreparingCompilationEnvironment()
        compiler = self.compilerSupplier.get()
        self.BeforeCompilation()
        compiler.compiler(self.request.code, source_file, target_file)
        self.BeforeResponse()

    def AfterReceivedCompilationRequest(self):
        pass

    def BeforeCheckingLegitimacy(self):
        pass

    def BeforePreparingCompilationEnvironment(self):
        pass

    def BeforeCompilation(self):
        pass

    def BeforeResponse(self):
        pass
