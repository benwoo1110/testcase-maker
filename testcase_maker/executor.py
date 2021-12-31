from abc import ABC
import logging
from pathlib import Path
import tempfile
from timeit import default_timer as timer
from typing import Callable, Union

from testcase_maker.constants import LOGGER_NAME


log = logging.getLogger(LOGGER_NAME)


class Executor(ABC):
    
    def __init__(self, source_file: Union[Path, str]):
        self.source_file: Path = Path(source_file)
        self.compiled_file: Path = None
        self.tempdir: Path = None
        self._tempdir: tempfile.TemporaryDirectory = None

    def __enter__(self) -> Callable[[str], str]:
        self._tempdir = tempfile.TemporaryDirectory()
        self.tempdir = Path(self._tempdir.name)
        log.info(f"Compiling {self.source_file} solution script...")
        start = timer()
        self.compiled_file = self.compile()
        end = timer()
        log.info(f"Compilation done! Took {end-start} seconds.")
        return self.execute

    def __exit__(self, exc, value, tb):
        self._tempdir.cleanup()

    @staticmethod
    def file_extension() -> str:
        raise NotImplementedError

    def compile(self) -> Path:
        raise NotImplementedError

    def execute(self, stdin: str) -> str:
        raise NotImplementedError
