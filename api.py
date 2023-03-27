import base64
import fastapi

from Entities import CppRunnerRequest, CppCompilerRequest
from cpp_compiler import compile_cpp_code_with_docker
from cpp_runner import run_cpp_native_with_docker
from timeout import TimeoutError

app = fastapi.FastAPI()


@app.post("/test/api/cpp_compiler")
async def cpp_compiler(code: CppCompilerRequest):
    result = compile_cpp_code_with_docker(
        base64.b64decode(code.code).decode("utf-8"), f"codes/cpp/{code.submission_id}.cpp",
        f"target/{code.submission_id}")
    return {
        "submission_id": code.submission_id,
        "is_ok": result.isOk,
        "message": result.message
    }


@app.post("/test/api/cpp_runner/")
async def cpp_runner(request: CppRunnerRequest):
    try:
        result = run_cpp_native_with_docker(request)
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
