from subprocess import Popen, PIPE
from typing import TYPE_CHECKING, Union

from testcase_maker.executor import Executor

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
        process = Popen(["javac", str(source_filename), "-d", str(tempdir)], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        out = process.communicate()
        print(out)
        print([x for x in tempdir.iterdir()])
        if out[1]:
            print(out[1].decode("UTF-8"))
            raise Exception("Error compiling answer script.")
        return tempdir.joinpath(f"{source_filename.stem}.class")

    def execute(self, exec_filename: Union["Path", str], stdin: str) -> bytes:
        process = Popen(["java", exec_filename.stem], stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=str(exec_filename.parent))
        out = process.communicate(stdin.encode())
        if out[1]:
            print(out[1].decode("UTF-8"))
            raise Exception("Error executing answer script.")
        return out[0]
