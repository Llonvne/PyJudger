from abstract.DockerBased import DockerBased
from abstract.Compiler import Compiler


class CompileResult:
    def __init__(self, message: str):
        self.isOk = "error" not in message
        self.message = message


class CppCompiler(Compiler, DockerBased):
    def __init__(self):
        super().__init__(
            "gpp-compiler",
            """FROM ubuntu:latest\nRUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*""")

    def compiler(self, code_str: str, source_file: str, target_file: str):
        code_str = self.decode_from_base64(code_str)
        CppCompiler.write_to_file(code_str, source_file)
        result = self.run_docker(f"g++ {source_file} -o {target_file}")
        # 返回编译结果
        return CompileResult(result.stderr)
