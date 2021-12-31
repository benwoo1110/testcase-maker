from typing import TYPE_CHECKING, Union

from testcase_maker.executor import Executor
from testcase_maker.utils import run_command

if TYPE_CHECKING:
    from pathlib import Path


class CPPExecutor(Executor):
    """
    Run your answer script in C++!
    """

    @staticmethod
    def file_extension() -> str:
        return ".cpp"

    def compile(self) -> "Path":
        args = ["g++", "-o", str(self.source_file.stem), str(self.source_file.absolute())]
        run_command(args, cwd=self.tempdir)
        return self.tempdir.joinpath(f"{self.source_file.stem}.exe")

    def execute(self, stdin: str) -> str:
        args = [str(self.compiled_file)]
        return run_command(args, stdin, self.compiled_file.parent)
