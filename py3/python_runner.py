from Entities import RunnerRequest
from utils import DockerUtils
from abstract.Runner import Runner
from timeout import timeout


class PythonRunner(Runner):
    imageName = "python3_runner"
    dockerfile = "FROM python:3.10"

    def image_dependency(self):
        DockerUtils.resolve_image_dependency(self.imageName, self.dockerfile)

    @timeout(10)
    def run(self, request: RunnerRequest):
        self.image_dependency()
        return self.standard_runner(request, "python3_runner", f" python ./target/{request.submission_id}.py")
