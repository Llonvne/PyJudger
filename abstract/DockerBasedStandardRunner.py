import abc

from Entities import RunnerRequest
from abstract.DockerBased import DockerBased
from abstract.Runner import Runner


class DockerBasedStandardRunner(DockerBased):
    def __init__(self, imageName: str, dockerfile: str):
        super().__init__(imageName, dockerfile)

    @abc.abstractmethod
    def get_command(self, request: RunnerRequest):
        pass

    def run(self, request: RunnerRequest):
        results = []
        for testcase in request.testcases:
            program = self.run_docker(self.get_command(request))
            program.stdin.write(testcase.input + "\n")
            program.stdin.flush()
            program.wait()
            results.append({
                "expect": testcase.output,
                "stdout": program.stdout.read(),
                "stderr": program.stderr.read(),
            })
        return results
