import tempfile
from pathlib import Path
from typing import List, TYPE_CHECKING

import attr

from testcase_maker.resolver import Resolver
from testcase_maker.subtask import Subtask
from testcase_maker.executor import Executor
from testcase_maker.executors import PythonExecutor

if TYPE_CHECKING:
    from testcase_maker.values import ValueGroup


@attr.define()
class TestcaseGenerator:
    values: "ValueGroup" = attr.ib()
    output_dir: Path = attr.ib(converter=Path)  # TODO Add a default
    answer_script: Path = attr.ib(default=None, converter=Path)  # TODO Handle if its None.
    script_executor: "Executor" = attr.ib(default=None)
    subtasks: List[Subtask] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        self.script_executor = PythonExecutor()  # TODO get based on file extension.

    def new_subtask(self, no_of_testcase: int, name: str = None) -> Subtask:
        if not name:
            name = str(len(self.subtasks) + 1)

        subtask = Subtask(name, no_of_testcase)
        self.subtasks.append(subtask)
        return subtask

    def generate(self):  # TODO Override toggle
        self.output_dir.mkdir(parents=True, exist_ok=True)

        for subtask in self.subtasks:
            for case_no in range(1, subtask.no_of_testcase + 1):
                print(f"Generating subtask '{subtask.name}', testcase '{case_no}'...")

                stdin_file = self.output_dir.joinpath(f"{subtask.name}-{case_no}.in")
                resolver = Resolver(subtask.override_name_values)
                stdin = resolver.resolve(self.values)

                with open(stdin_file, "w", newline="\n") as input_buffer:
                    input_buffer.write(stdin)
                print(f"Saved '{stdin_file}'")

                stdout_file = self.output_dir.joinpath(f"{subtask.name}-{case_no}.out")
                with tempfile.TemporaryDirectory() as tmpdir:
                    exec_filename = self.script_executor.compile(tmpdir, self.answer_script)
                    stdout = self.script_executor.execute(exec_filename, stdin).decode("UTF-8")

                with open(stdout_file, "w", newline="\n") as output_buffer:
                    output_buffer.write(stdout)
                print(f"Saved '{stdout_file}'")
