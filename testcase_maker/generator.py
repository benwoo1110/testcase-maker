import tempfile
from pathlib import Path
from typing import Callable, List, TYPE_CHECKING, Union

from timeit import default_timer as timer

import attr
from attr.converters import optional

from testcase_maker.constants import LOGGER_NAME
from testcase_maker.executor_manager import get_executor_for_script
from testcase_maker.resolver import Resolver
from testcase_maker.subtask import Subtask
from testcase_maker.executor import Executor
from testcase_maker.utils import NewlineTypes

if TYPE_CHECKING:
    from testcase_maker.values import ValueGroup

import logging


log = logging.getLogger(LOGGER_NAME)


@attr.define()
class TestcaseGenerator:
    """
    The generator class.

    Attributes:
        values ValueGroup: Structure to build the testcase on.
        output_dir Path: Folder where the generated testcase files will be saved.
        answer_script Path: Script that can solve the testcase to produce the correct stdout.
        stdin_filename_format str: Filename used for stdin. There is 2 placeholders: subtask name and testcase number.
        stdout_filename_format str: Filename used for stdout. There is 2 placeholders: subtask name and testcase number.
        newline: Preferred newline format used for stdin and stdout files. Defaults to \n.
    """

    values: "ValueGroup" = attr.ib()
    output_directory: Path = attr.ib(default="./testcases/", converter=Path)
    answer_script: Path = attr.ib(default=None, converter=optional(Path))
    stdin_filename_format: str = attr.ib(default="{}-{}.in")
    stdout_filename_format: str = attr.ib(default="{}-{}.out")
    newline: Union[str, NewlineTypes] = attr.ib(default=NewlineTypes.LF)

    _subtasks: List[Subtask] = attr.ib(factory=list)

    def new_subtask(self, no_of_testcase: int, name: str = None) -> Subtask:
        """
        Creates a new subtask to work with.

        Args:
            no_of_testcase: The number of testcases to generate for this subtask.
            name: Name of the subtask. To be reflected in testcase filename.

        returns:
            The new subtask object.
        """
        if not name:
            name = str(len(self._subtasks) + 1)

        subtask = Subtask(name, no_of_testcase)
        self._subtasks.append(subtask)
        return subtask

    def generate(self, override: bool = False):
        """
        Generates both stdin and stdout for testcases.

        Args:
            override: Set to ``True`` if you want to override existing testcase files (if any). Defaults to ``False``.
        """
        self.generate_stdin(override)
        self.generate_stdout(override)

    def generate_stdin(self, override: bool = False):
        """
        Generates stdin for testcases.

        Args:
            override: Set to ``True`` if you want to override existing testcase files (if any). Defaults to ``False``.
        """
        self._pre_generation()

        for subtask in self._subtasks:
            for testcase_no, overrides in subtask.iterate():
                start = timer()
                log.info(f"Generating stdin for subtask '{subtask.name}', testcase '{testcase_no}'...")

                stdin_file = self._stdin_path(subtask.name, testcase_no)
                if stdin_file.is_file() and not override:
                    log.info(f"Skipped '{stdin_file}' as file already exist.")
                    continue

                resolver = Resolver(overrides)
                stdin = resolver.resolve(self.values)

                with open(stdin_file, "w", newline=self.newline) as input_buffer:
                    input_buffer.write(stdin)
                    input_buffer.write(self.newline)
                end = timer()
                log.info(f"Saved '{stdin_file}'. Took {end-start} seconds.")

    def generate_stdout(self, override: bool = False):
        """
        Generates stdout for testcases.

        !!! danger "Notice"
            Valid stdin files must be generated and present first.

        Args:
            override: Set to ``True`` if you want to override existing testcase files (if any). Defaults to ``False``.
        """
        self._pre_generation()

        if not self.answer_script:
            log.error("Unable to generate stdout as there is no answer script specified.")
            return

        with get_executor_for_script(self.answer_script) as executor:
            for subtask in self._subtasks:
                for testcase_no in range(1, subtask.no_of_testcase + 1):
                    start = timer()
                    log.info(f"Generating stdout for subtask '{subtask.name}', testcase '{testcase_no}'...")

                    stdin_file = self._stdin_path(subtask.name, testcase_no)
                    if not stdin_file.is_file():
                        log.info(f"Skipped as stdin '{stdin_file}' does not exist.")
                        continue
                    with open(stdin_file, "r", newline=self.newline) as input_buffer:
                        stdin = input_buffer.read()

                    stdout_file = self._stdout_path(subtask.name, testcase_no)
                    if stdout_file.is_file() and not override:
                        log.info(f"Skipped '{stdout_file}' as file already exist.")
                        continue

                    stdout = self._execute_script(stdin, executor)
                    with open(stdout_file, "w", newline=self.newline) as output_buffer:
                        output_buffer.write(stdout)
                
                    end = timer()
                    log.info(f"Saved '{stdout_file}'. Took {end-start} seconds.")

    def validate(self):
        """
        Checks that answer script matches the stdout for the respective stdin.
        """
        if not self.answer_script:
            log.error("Unable to validate stdout as there is no answer script specified.")
            return

        with get_executor_for_script(self.answer_script) as executor:
            for subtask in self._subtasks:
                for testcase_no in range(1, subtask.no_of_testcase + 1):
                    start = timer()
                    log.info(f"Validating stdout for subtask '{subtask.name}', testcase '{testcase_no}'...")

                    stdin_file = self._stdin_path(subtask.name, testcase_no)
                    if not stdin_file.is_file():
                        log.warning(f"Skipped as stdin '{stdin_file}' does not exist.")
                        continue
                    with open(stdin_file, "r", newline=self.newline) as input_buffer:
                        stdin = input_buffer.read()

                    stdout_file = self._stdout_path(subtask.name, testcase_no)
                    if not stdout_file.is_file():
                        log.warning(f"Skipped as stdout '{stdout_file}' does not exist.")
                        continue

                    with open(stdout_file, "r", newline=self.newline) as output_buffer:
                        stdout = output_buffer.read()

                    actual_stdout = self._execute_script(stdin, executor)
                    if actual_stdout.rstrip() != stdout.rstrip():
                        log.warning(f"Incorrect stdout detected, got {actual_stdout} instead of {stdout}.")
                    else:
                        log.info(f"Correct!")

                    end = timer()
                    log.info(f"Validated '{stdout_file}'. Took {end-start} seconds.")

    def _pre_generation(self):
        self.output_directory.mkdir(parents=True, exist_ok=True)
        if len(self._subtasks) < 1:
            self.new_subtask(5)

    def _stdin_path(self, subtask_name: str, testcase_no: int):
        return self.output_directory.joinpath(self.stdin_filename_format.format(subtask_name, testcase_no))

    def _stdout_path(self, subtask_name: str, testcase_no: int):
        return self.output_directory.joinpath(self.stdout_filename_format.format(subtask_name, testcase_no))

    def _execute_script(self, stdin: str, executor: Callable[[str], str]) -> str:
        start = timer()
        stdout = executor(stdin)
        end = timer()
        log.info(f"Executed solution script in {end-start} seconds.")
        return stdout
