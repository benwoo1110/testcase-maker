import sys
from subprocess import PIPE, Popen
from typing import TYPE_CHECKING, Union

from testcase_maker.executor import Executor

if TYPE_CHECKING:
    from pathlib import Path


class PythonExecutor(Executor):
    @property
    def file_extension(self) -> str:
        return "py"

    def compile(self, tempdir: Union["Path", str], source_filename: Union["Path", str]) -> Union["Path", str]:
        return source_filename

    def execute(self, exec_filename: Union["Path", str], stdin: str) -> bytes:
        process = Popen([sys.executable, str(exec_filename)], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        out = process.communicate(input=stdin.encode())
        if out[1]:
            print(out[1].decode("UTF-8"))
            raise Exception("Error executing answer script.")
        return out[0]
