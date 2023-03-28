from Entities import RunnerRequest
from abstract.DockerBasedStandardRunner import DockerBasedStandardRunner


class CppRunner(DockerBasedStandardRunner):
    def __init__(self):
        super().__init__("ubuntu", """FROM ubuntu:latest""")

    def get_command(self, request: RunnerRequest):
        return f"./target/{request.submission_id}/{request.submission_id}"

    def get_version(self) -> str:
        return "unknown"
