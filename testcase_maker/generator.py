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
    target_folder: Path = attr.ib(converter=Path)
    answer_script: Path = attr.ib(converter=Path)
    script_executor: "Executor" = attr.ib(default=None)
    subtasks: List[Subtask] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        self.script_executor = PythonExecutor()  # TODO get based on file extension.

    def new_subtask(self, builder: "ValueGroup", no_of_testcase: int, name: str = None) -> Subtask:
        if not name:
            name = str(len(self.subtasks) + 1)

        subtask = Subtask(name, builder, no_of_testcase)
        self.subtasks.append(subtask)
        return subtask

    def generate(self):
        self.target_folder.mkdir(parents=True, exist_ok=True)

        for subtask in self.subtasks:
            for case_no in range(1, subtask.no_of_testcase + 1):
                print(f"Generating subtask '{subtask.name}', testcase '{case_no}'...")

                stdin_file = self.target_folder.joinpath(f"{subtask.name}-{case_no}.in")
                resolver = Resolver(subtask.override_name_values)
                stdin = resolver.resolve(subtask.builder)

                with open(stdin_file, "w", newline="\n") as input_buffer:
                    input_buffer.write(stdin)
                print(f"Saved '{stdin_file}'")

                stdout_file = self.target_folder.joinpath(f"{subtask.name}-{case_no}.out")
                with tempfile.TemporaryDirectory() as tmpdir:
                    exec_filename = self.script_executor.compile(tmpdir, self.answer_script)
                    stdout = self.script_executor.execute(exec_filename, stdin).decode("UTF-8")

                with open(stdout_file, "w", newline="\n") as output_buffer:
                    output_buffer.write(stdout)
                print(f"Saved '{stdout_file}'")
