from abc import ABC
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from pathlib import Path


class Executor(ABC):
    @property
    def file_extension(self) -> str:
        raise NotImplementedError

    def compile(self, tempdir: Union["Path", str], source_filename: Union["Path", str]) -> Union["Path", str]:
        raise NotImplementedError

    def execute(self, exec_filename: Union["Path", str], stdin: str) -> bytes:
        raise NotImplementedError
