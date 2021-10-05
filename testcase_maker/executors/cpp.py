from typing import TYPE_CHECKING, Union

from testcase_maker.executor import Executor
from testcase_maker.utils import run_command

if TYPE_CHECKING:
    from pathlib import Path


class CPPExecutor(Executor):
    """
    Run your answer script in C++!
    """

    @property
    def file_extension(self) -> str:
        return "cpp"

    def compile(self, tempdir: Union["Path", str], source_filename: Union["Path", str]) -> Union["Path", str]:
        args = ["g++", "-o", str(source_filename.stem), str(source_filename.absolute())]
        run_command(args, cwd=tempdir)
        return tempdir.joinpath(f"{source_filename.stem}.exe")

    def execute(self, exec_filename: Union["Path", str], stdin: str) -> bytes:
        args = [str(exec_filename)]
        return run_command(args, stdin, exec_filename.parent)
    
