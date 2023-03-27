from Entities import RunnerRequest
from abstract.DockerBasedStandardRunner import DockerBasedStandardRunner


class PythonRunner(DockerBasedStandardRunner):
    def get_command(self, request: RunnerRequest):
        return f" python ./target/{request.submission_id}.py"

    def __init__(self):
        super().__init__("python3_runner", "FROM python:3.10")
