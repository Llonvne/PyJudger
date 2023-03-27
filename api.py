import os.path
from py3.python_compiler import PythonCompiler
from py3.python_runner import PythonRunner

import fastapi

from Entities import RunnerRequest, CompilerRequest
from cpp.cpp_compiler import CppCompiler
from cpp.cpp_runner import CppRunner

app = fastapi.FastAPI()

cppCompiler = CppCompiler()
cppRunner = CppRunner()
python3Compiler = PythonCompiler()
python3Runner = PythonRunner()

code_root_path = "codes"
executable_root_path = "target"


def code_space_path(language: str):
    return os.path.join(code_root_path, language)


@app.post("/test/api/cpp_compiler")
async def cpp_compiler(code: CompilerRequest):
    result = cppCompiler.compiler(
        code.code, os.path.join(code_space_path("cpp"), f"{code.submission_id}.cpp"),
        f"target/{code.submission_id}")
    return {
        "submission_id": code.submission_id,
        "is_ok": result.isOk,
        "message": result.message
    }


@app.post("/test/api/cpp_runner/")
async def cpp_runner(request: RunnerRequest):
    try:
        result = cppRunner.run(request)
        return {
            "submission_id": request.submission_id,
            "status": "OK",
            "result": result,
        }
    except TimeoutError:
        return {
            "submission_id": request.submission_id,
            "status": "timeout",
            "result": []
        }


@app.post("/test/api/python3_compiler")
async def python3_compiler(code: CompilerRequest):
    result = python3Compiler.compiler(code.code, os.path.join(code_space_path("python3"), f"{code.submission_id}.py"),
                                      f"target/{code.submission_id}.py")
    return {
        "submission_id": code.submission_id,
        "is_ok": result.isOk,
        "message": result.message
    }


@app.post("/test/api/python3_runner")
async def python3_runner(request: RunnerRequest):
    try:
        result = python3Runner.run(request)
        return {
            "submission_id": request.submission_id,
            "status": "OK",
            "result": result,
        }
    except TimeoutError:
        return {
            "submission_id": request.submission_id,
            "status": "timeout",
            "result": []
        }


@app.get("/")
async def root():
    return "Welcome to Llonvne Judge Server!"
