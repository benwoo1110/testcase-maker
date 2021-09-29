from typing import TYPE_CHECKING, Union

from testcase_maker.executor import Executor

if TYPE_CHECKING:
    from pathlib import Path


class CPPExecutor(Executor):
    """
    !!! danger "Notice"
            Not implemented yet.
    """

    @property
    def file_extension(self) -> str:
        return "cpp"

    def compile(self, tempdir: Union["Path", str], source_filename: Union["Path", str]) -> Union["Path", str]:
        pass

    def execute(self, exec_filename: Union["Path", str], stdin: str) -> bytes:
        pass
