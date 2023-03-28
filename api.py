import fastapi

from Entities import RunnerRequest, CompilerRequest
from cpp.cpp_compiler import CppCompiler
from cpp.cpp_runner import CppRunner
from jdk.GenericJavaRunner import GenericJavaRunner
from jdk.JDKCompiler import JDKCompiler
from lifecycle.CompileLifeCycle import CompileLifeCycle
from lifecycle.RunnerLifeCycle import RunnerLifeCycle
from lifecycle.plugins.AutomaticPathGenerator import AutomaticPathGenerator
from py3.GenericPythonRunner import GenericPython3Runner
from py3.python_compiler import PythonCompiler

app = fastapi.FastAPI()


@app.post("/test/api/cpp_compiler")
async def cpp_compiler(request: CompilerRequest):
    return CompileLifeCycle(request, lambda: CppCompiler()) \
        .addPlugin(AutomaticPathGenerator()).startLifeCycle()


@app.post("/test/api/cpp_runner/")
async def cpp_runner(request: RunnerRequest):
    return RunnerLifeCycle(request, lambda: CppRunner()).startLifeCycle()


@app.post("/test/api/python3_compiler")
async def python3_compiler(request: CompilerRequest):
    return CompileLifeCycle(request, lambda: PythonCompiler()) \
        .addPlugin(AutomaticPathGenerator()).startLifeCycle()


@app.post("/test/api/python3_runner/{python_version}")
async def python3_runner(request: RunnerRequest, python_version: str):
    return RunnerLifeCycle(request, lambda: GenericPython3Runner(python_version)).startLifeCycle()


@app.post("/test/api/jdk_compiler")
async def jdk_compiler(request: CompilerRequest):
    return CompileLifeCycle(request, lambda: JDKCompiler()) \
        .addPlugin(AutomaticPathGenerator()).startLifeCycle()


@app.post("/test/api/jdk_runner/{java_version}")
async def jdk_runner(request: RunnerRequest, java_version: int):
    return RunnerLifeCycle(request, lambda: GenericJavaRunner(java_version)).startLifeCycle()


@app.get("/")
async def root():
    return "Welcome to Llonvne Judge Server!"
