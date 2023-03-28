from lifecycle.RunnerLifeCycle import RunnerLifeCycleStatus, RunnerLifeCycle, RunnerError
from lifecycle.plugins.LifeCyclePlugin import LifeCyclePlugin


class RunnerVersionLimiter(LifeCyclePlugin):
    def __init__(self, allowed_versions: [str]):
        self.allowed_version = allowed_versions

    def scopes(self) -> list[RunnerLifeCycleStatus]:
        return [RunnerLifeCycleStatus.RunningInProgress]

    def on(self, lifeCycle: RunnerLifeCycle):
        if lifeCycle.runner.get_version() not in self.allowed_version:
            raise RunnerError(f"unsupported version: {lifeCycle.runner.get_version()}")
