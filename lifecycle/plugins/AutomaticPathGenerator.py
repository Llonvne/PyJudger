import os
import shutil

from lifecycle.CompileLifeCycle import CompileLifeCycleStatus, CompileLifeCycle
from lifecycle.plugins.LifeCyclePlugin import LifeCyclePlugin


class AutomaticPathGenerator(LifeCyclePlugin):
    def scopes(self) -> list[CompileLifeCycleStatus]:
        return [CompileLifeCycleStatus.CompilationInProgress]

    def on(self, lifeCycle: CompileLifeCycle):
        source_path = f"./codes/{lifeCycle.compiler.language_name()}/{lifeCycle.request.submission_id}/"
        if os.path.exists(source_path):
            shutil.rmtree(source_path)
        os.makedirs(source_path)
        lifeCycle.source_file = source_path + f"source_{lifeCycle.request.submission_id}" + lifeCycle.compiler.source_extension_name()

        target_path = f"./target/{lifeCycle.request.submission_id}/"
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        os.makedirs(target_path)
        lifeCycle.target_file = target_path + f"{lifeCycle.request.submission_id}" + lifeCycle.compiler.compiled_extension_name()
