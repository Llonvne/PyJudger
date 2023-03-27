import subprocess

from utils import DockerUtils
from abstract.Compiler import Compiler


class CompileResult:
    def __init__(self, message: str):
        self.isOk = "error" not in message
        self.message = message


class CppCompiler(Compiler):
    imageName = "gpp-compiler"
    dockerfile = """FROM ubuntu:latest\nRUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*"""

    def image_dependency(self):
        DockerUtils.resolve_image_dependency(self.imageName, self.dockerfile)

    def compiler(self, code_str: str, source_file: str, target_file: str):
        self.image_dependency()

        code_str = self.decode_from_base64(code_str)

        CppCompiler.write_to_file(code_str, source_file)

        # 使用 Docker 编译源文件
        compile_command = f"docker run --rm -v $(pwd):/src -w /src gpp-compiler g++ {source_file} -o {target_file}"
        compile_result = subprocess.run(compile_command, shell=True, text=True, stderr=subprocess.PIPE)

        # 返回编译结果
        return CompileResult(compile_result.stderr)
