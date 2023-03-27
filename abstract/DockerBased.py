import abc
import subprocess
from subprocess import Popen

from utils import DockerUtils


class DockerBased(abc.ABC):
    def __init__(self, imageName: str, dockerfile: str):
        self.imageName = imageName
        self.dockerfile = dockerfile
        DockerUtils.resolve_image_dependency(imageName, dockerfile)

    def run(self, command) -> Popen:
        DockerUtils.resolve_image_dependency(self.imageName, self.dockerfile)
        compile_command = f"docker run -i --rm -v $(pwd):/src -w /src {self.imageName} {command}"
        program = subprocess.Popen(compile_command, shell=True, text=True, stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        return program
