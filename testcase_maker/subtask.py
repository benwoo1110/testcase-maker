from typing import Dict, TYPE_CHECKING

import attr

if TYPE_CHECKING:
    from testcase_maker.value import Value


@attr.define()
class Subtask:
    name: str = attr.ib()
    no_of_testcase: int = attr.ib()
    override_name_values: Dict = attr.ib(factory=dict)

    def override_value(self, name: str, value: "Value"):
        self.override_name_values[name] = value
