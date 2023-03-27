import os
import shutil

from lifecycle.CompileLifeCycle import CompileLifeCycleStatus, CompileLifeCycle
from lifecycle.plugins.LifeCyclePlugin import LifeCyclePlugin


class AutomaticPathGenerator(LifeCyclePlugin):
    def scopes(self) -> list[CompileLifeCycleStatus]:
        return [CompileLifeCycleStatus.CompilationInProgress]

    def on(self, compileLifeCycle: CompileLifeCycle):
        source_path = f"./codes/{compileLifeCycle.compiler.language_name()}/{compileLifeCycle.request.submission_id}/"
        if os.path.exists(source_path):
            shutil.rmtree(source_path)
        os.makedirs(source_path)
        compileLifeCycle.source_file = source_path + f"source_{compileLifeCycle.request.submission_id}" + compileLifeCycle.compiler.source_extension_name()

        target_path = f"./target/{compileLifeCycle.compiler.language_name()}/{compileLifeCycle.request.submission_id}/"
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        os.makedirs(target_path)
        compileLifeCycle.target_file = target_path + f"compiled_{compileLifeCycle.request.submission_id}" + compileLifeCycle.compiler.compiled_extension_name()
