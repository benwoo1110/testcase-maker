import timeit
from pathlib import Path
from subprocess import Popen, PIPE
from typing import List, TYPE_CHECKING

import attr

from testcase_maker.resolver import Resolver
from testcase_maker.subtask import Subtask

if TYPE_CHECKING:
    from testcase_maker.values.value_group import ValueGroup


@attr.define()
class TestcaseGenerator:
    target_folder: Path = attr.ib(converter=Path)
    answer_script: Path = attr.ib(converter=Path)
    subtasks: List[Subtask] = attr.ib(factory=list)

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
                resolver = Resolver(subtask.override_name_values)
                result = resolver.resolve(subtask.builder)
                input_file = self.target_folder.joinpath(f"{subtask.name}-{case_no}.in")
                print(f"Saving to '{input_file}'...")
                with open(input_file, 'w', newline="\n") as input_buffer:
                    input_buffer.write(result)

                print("Time taken", timeit.timeit(lambda: self.execute(result), number=1))
                output = self.execute(result).decode('UTF-8')

                output_file = self.target_folder.joinpath(f"{subtask.name}-{case_no}.out")
                print(f"Saving to '{output_file}'...")
                with open(output_file, 'w', newline="\n") as output_buffer:
                    output_buffer.write(output)

    def execute(self, result, ) -> bytes:
        p = Popen(["python", str(self.answer_script)], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        return p.communicate(input=result.encode())[0]
