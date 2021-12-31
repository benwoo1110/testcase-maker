import shutil
import sys
from subprocess import PIPE, Popen
from typing import TYPE_CHECKING, Union

from testcase_maker.executor import Executor
from testcase_maker.utils import run_command

if TYPE_CHECKING:
    from pathlib import Path


class PythonExecutor(Executor):
    """
    Run your answer script in python!
    """

    @staticmethod
    def file_extension() -> str:
        return ".py"

    def compile(self) -> "Path":
        copy_source = self.tempdir.joinpath(self.source_file.name)
        shutil.copy(self.source_file, copy_source)
        args = [sys.executable, "-m", "compileall", str(copy_source)]
        run_command(args, cwd=self.tempdir)
        return next(self.tempdir.joinpath("__pycache__").glob('*.pyc'))

    def execute(self, stdin: str) -> str:
        args = [sys.executable, str(self.compiled_file)]
        return run_command(args, stdin)
