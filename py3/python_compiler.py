from abstract.Compiler import Compiler
from cpp.cpp_compiler import CompileResult


class PythonCompiler(Compiler):
    def compiler(self, code_str: str, source_file: str, target_file: str):
        code_str = self.decode_from_base64(code_str)
        self.write_to_file(code_str, source_file)
        self.write_to_file(code_str, target_file)
        return CompileResult("ok")
