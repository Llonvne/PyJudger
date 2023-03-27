import abc
import base64


class Compiler(abc.ABC):

    @abc.abstractmethod
    def image_dependency(self):
        pass

    @staticmethod
    def decode_from_base64(code) -> str:
        return base64.b64decode(code).decode("utf-8")

    @staticmethod
    def write_to_file(code_str, file):
        # 将代码写入源文件
        with open(file, "w") as f:
            f.write(code_str)

    @abc.abstractmethod
    def compiler(self, code_str: str, source_file: str, target_file: str):
        pass
