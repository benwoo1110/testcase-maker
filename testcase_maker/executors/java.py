from subprocess import Popen, PIPE
from typing import TYPE_CHECKING, Union

from testcase_maker.executor import Executor
from testcase_maker.utils import run_command

if TYPE_CHECKING:
    from pathlib import Path


class JavaExecutor(Executor):
    """
    Run your answer script in java!
    """

    @staticmethod
    def file_extension() -> str:
        return ".java"

    def compile(self) -> "Path":
        args = ["javac", str(self.source_file.absolute()), "-d", str(self.tempdir)]
        run_command(args, cwd=self.tempdir)
        return self.tempdir.joinpath(f"{self.source_file.stem}.class")

    def execute(self, stdin: str) -> str:
        args = ["java", str(self.compiled_file.stem)]
        return run_command(args, stdin, self.compiled_file.parent)
