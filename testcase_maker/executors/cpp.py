from typing import TYPE_CHECKING, Union

from testcase_maker.executors import BaseExecutor

if TYPE_CHECKING:
    from pathlib import Path


class CPPExecutor(BaseExecutor):
    def compile(self, tempdir: Union["Path", str], source_filename: Union["Path", str]) -> Union["Path", str]:
        pass

    def execute(self, exec_filename: Union["Path", str], stdin: str) -> bytes:
        pass
