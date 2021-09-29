import shutil
import sys
from subprocess import PIPE, Popen
from typing import TYPE_CHECKING, Union

from testcase_maker.executor import Executor
from testcase_maker.utils import run_command

if TYPE_CHECKING:
    from pathlib import Path


class PythonExecutor(Executor):
    @property
    def file_extension(self) -> str:
        return "py"

    def compile(self, tempdir: Union["Path", str], source_filename: Union["Path", str]) -> Union["Path", str]:
        copy_source = tempdir.joinpath(source_filename.name)
        shutil.copy(source_filename, copy_source)
        args = [sys.executable, "-m", "compileall", str(copy_source)]
        run_command(args, cwd=tempdir)
        return next(tempdir.joinpath("__pycache__").glob('*.pyc'))

    def execute(self, exec_filename: Union["Path", str], stdin: str) -> bytes:
        args = [sys.executable, str(exec_filename)]
        return run_command(args, stdin)
