from typing import List, Any, Union, TYPE_CHECKING, Dict

import attr

from testcase_maker.values.base import BaseValue, ValueContainer
from testcase_maker.values.constant import Constant
from testcase_maker.values.loop_value import LoopValue
from testcase_maker.values.named_value import NamedValue

if TYPE_CHECKING:
    from testcase_maker.core import Resolver


@attr.define()
class ValueGroup(BaseValue):
    values: List[BaseValue] = attr.ib(factory=list)
    value_name_map: Dict[BaseValue, Any] = attr.ib(factory=dict)
    name_value_map: Dict[Any, BaseValue] = attr.ib(factory=dict)

    def add(self, value: BaseValue):
        self.values.append(value)

        while isinstance(value, ValueContainer):
            parent, value = value, value.value
            if isinstance(parent, NamedValue):
                # self.value_name_map[value] = parent.name
                self.name_value_map[parent.name] = value

        if isinstance(value, ValueGroup):
            # self.value_name_map.update(value.value_name_map)
            self.name_value_map.update(value.name_value_map)

    def space(self):
        self.add(Constant(" "))

    def newline(self):
        self.add(Constant("\n"))

    def repeat(self, value: "BaseValue", amount: Union[BaseValue, int], delimiter: str):
        self.add(LoopValue(value, amount, delimiter))

    def generate(self, resolver: "Resolver") -> str:
        output_string = ""
        for value in self.values:
            resolved_value = resolver.resolve(value)
            output_string += str(resolved_value)

        return output_string
