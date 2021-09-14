import timeit
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Any, Dict, Optional, TYPE_CHECKING, List, Union

import attr

from testcase_maker.values.base import BaseValue
from testcase_maker.values.named_value import NamedValue

if TYPE_CHECKING:
    from testcase_maker.values.value_group import ValueGroup


@attr.define()
class Resolver:
    _override_name_values: Dict = attr.ib(factory=dict)
    _resolved_values: Dict = attr.ib(factory=dict)

    def get_override(self, name: Any, default: Optional[BaseValue] = None):
        return self._override_name_values.get(name, default)

    def get_value(self, var_name: Any) -> Optional[Any]:
        if var_name not in self._resolved_values:
            raise ValueError(f"No such resolved variable '{var_name}'.")
        return self._resolved_values[var_name]

    def resolve(self, value: Union[BaseValue, Any], check_type: type = None):
        if isinstance(value, NamedValue):
            target_value = self.get_override(value.name, value.value)
            resolved_value = self.resolve(target_value, check_type)
            self._resolved_values[value.name] = resolved_value
            return resolved_value

        if isinstance(value, BaseValue):
            value = value.generate(self)

        if check_type and not isinstance(value, check_type):
            raise TypeError(f"Expected type '{check_type}', but got type '{type(value)}' instead.")

        return value


@attr.define()
class Subtask:
    name: str = attr.ib()
    builder: "ValueGroup" = attr.ib()
    no_of_testcase: int = attr.ib()
    override_name_values: Dict = attr.ib(factory=dict)

    def override_value(self, name: str, value: BaseValue):
        self.override_name_values[name] = value


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
