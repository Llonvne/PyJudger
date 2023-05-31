import uuid

import fastapi
import uvicorn

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


@app.post("/api/cpp_compiler")
async def cpp_compiler(request: CompilerRequest):
    return CompileLifeCycle(request, lambda: CppCompiler()) \
        .addPlugin(AutomaticPathGenerator()).startLifeCycle()


@app.post("/api/cpp_runner/")
async def cpp_runner(request: RunnerRequest):
    return RunnerLifeCycle(request, lambda: CppRunner()).startLifeCycle()


@app.post("/api/python3_compiler")
async def python3_compiler(request: CompilerRequest):
    return CompileLifeCycle(request, lambda: PythonCompiler()) \
        .addPlugin(AutomaticPathGenerator()).startLifeCycle()


@app.post("/api/python3_runner/{python_version}")
async def python3_runner(request: RunnerRequest, python_version: str):
    return RunnerLifeCycle(request, lambda: GenericPython3Runner(python_version)).startLifeCycle()


@app.post("/api/jdk_compiler")
async def jdk_compiler(request: CompilerRequest):
    return CompileLifeCycle(request, lambda: JDKCompiler()) \
        .addPlugin(AutomaticPathGenerator()).startLifeCycle()


@app.post("/api/jdk_runner/{java_version}")
async def jdk_runner(request: RunnerRequest, java_version: int):
    return RunnerLifeCycle(request, lambda: GenericJavaRunner(java_version)) \
        .startLifeCycle()


name = uuid.uuid4()


@app.get("/api/metadata")
async def get_metadata():
    return {
        "serverName": name,
        "networkMetadata": {
            "apiRootUrl": "http://127.0.0.1:8080/api/",
        },
        "compilerMetadata": {
            "supportCompilers": [
                {
                    "name": "gcc-cpp",
                    "version": "17",
                    "url": "cpp_compiler"
                },
                {
                    "name": "java",
                    "version": "17",
                    "url": "jdk_compiler"
                },
                {
                    "name": "python",
                    "version": "3.10",
                    "url": "python3_compiler"
                }
            ]
        },
        "runnerMetadata": {
            "supportRunners": [
                {
                    "name": "cpp-runner",
                    "version": "unknown",
                    "url": "cpp_runner"
                }
            ]
        }
    }


@app.get("/")
async def root():
    return "Welcome to Llonvne Judge Server!"


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
