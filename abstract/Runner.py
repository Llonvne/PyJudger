import abc
import subprocess

from Entities import RunnerRequest


class Runner(abc.ABC):
    @abc.abstractmethod
    def run(self, runnerRequest: RunnerRequest):
        pass

    @abc.abstractmethod
    def image_dependency(self):
        pass

    @staticmethod
    def standard_runner(request: RunnerRequest, imageName: str, command: str):
        results = []
        for testcase in request.testcases:
            compile_command = f"docker run -i --rm -v $(pwd):/src -w /src {imageName} {command}"
            program = subprocess.Popen(compile_command, shell=True, text=True, stderr=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            program.stdin.write(testcase.input + "\n")
            program.stdin.flush()
            program.wait()
            results.append({
                "expect": testcase.output,
                "stdout": program.stdout.read(),
                "stderr": program.stderr.read(),
            })
        return results
