from enum import IntEnum
from typing import Callable, Union

from Entities import CompilerRequest
from abstract.Compiler import Compiler
from cpp.cpp_compiler import CompileResult
from lifecycle.plugins.LifeCyclePlugin import LifeCyclePlugin


class CompileError(Exception):
    pass


class CompileLifeCycleStatus(IntEnum):
    CompilationRequestReceived = 0
    CheckingDataLegitimacy = 1
    AwaitingCompilation = 2
    PreparingCompilationEnvironment = 3
    CompilationInProgress = 4
    CompleteCompilation = 5
    ExecuteHTTPResponse = 6
    End = 7


class CompileLifeCycle:
    def __init__(self,
                 request: CompilerRequest,
                 compilerSupplier: Callable[[], Compiler] = None,
                 source_file: str = None,
                 target_file: str = None):
        """
        CompileLifeCycle
        :param request: 传入的请求，该参数必须传入
        :param compilerSupplier: 可选参数，编译器生成器，如果不提供必须由插件在 PreparingCompilationEnvironment
        （包含）前提供 self.compile
        :param source_file: 可选参数，源代码存放路径，如果不提供必须由插件在 CompilationInProgress （包含）前提供
        :param target_file: 可选参数，编译后存放路径，如果不提供必须由插件在 CompilationInProgress （包含）前提供

        Notice: 其中 source_file,target_file 在标准实现中均由插件AutomaticPathGenerator生成
        """
        self.status = CompileLifeCycleStatus.CompilationRequestReceived
        self.request = request
        self.compilerSupplier = compilerSupplier
        self.__listeners: [list[Callable[['CompileLifeCycle'], None]]] = [[] for i in range(8)]
        self.source_file = source_file
        self.target_file = target_file
        self.compiler = None
        self.result: Union[CompileResult, None] = None

    def startLifeCycle(self):
        for i in range(8):

            # 更改自己的状态
            self.status = CompileLifeCycleStatus(i)

            # 跳用所有注册在内部的插件
            for listener in self.__listeners[i]:
                listener(self)

            if i == 3:
                # PreparingCompilationEnvironment 周期
                # 检查自己的编译器是否为空，可能已经被插件注入，如果为空
                if self.compiler is None:

                    # 检查自己的 CompilerSupplier 是否为空
                    if self.compilerSupplier is None:
                        # 如果都为空则报找不到编译器
                        raise CompileError("No valid compiler provided")

                    # 否则使用 compilerSupplier 获得编译器
                    self.compiler = self.compilerSupplier()

            if i == 4:
                # CompilationInProgress 周期
                # 检查 source_path 和 target_path 是否为空
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
            self.__listeners[scope.value].append(lambda x: plugin.on(x))
        return self

    def doResponse(self):
        return {
            "submission_id": self.request.submission_id,
            "is_ok": self.result.isOk
        }
