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

    @property
    def file_extension(self) -> str:
        return "java"

    def compile(self, tempdir: Union["Path", str], source_filename: Union["Path", str]) -> Union["Path", str]:
        args = ["javac", str(source_filename), "-d", str(tempdir)]
        run_command(args, cwd=tempdir)
        return tempdir.joinpath(f"{source_filename.stem}.class")

    def execute(self, tempdir: Union["Path", str], exec_filename: Union["Path", str], stdin: str) -> str:
        args = ["java", str(exec_filename.stem)]
        return run_command(args, stdin, exec_filename.parent)
