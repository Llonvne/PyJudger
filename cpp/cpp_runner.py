from Entities import RunnerRequest
from utils import DockerUtils
from abstract.Runner import Runner
from timeout import timeout


class CppRunner(Runner):
    imageName = "ubuntu"
    dockerfile = """FROM ubuntu:latest"""

    @timeout(10)
    def run(self, request: RunnerRequest):
        self.image_dependency()
        return Runner.standard_runner(request, "ubuntu:latest", f"./target/{request.submission_id}")

    def image_dependency(self):
        DockerUtils.resolve_image_dependency(self.imageName, self.dockerfile)
