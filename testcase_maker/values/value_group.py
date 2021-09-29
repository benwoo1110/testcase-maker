from typing import List, Union, TYPE_CHECKING, Any

import attr

from testcase_maker.value import Value
from testcase_maker.values import Constant

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class ValueGroup(Value):
    values: List[Any, "Value"] = attr.ib(factory=list)

    def add(self, value: Union[Any, "Value"]):
        self.values.append(value)

    def space(self):
        self.add(Constant(" "))

    def newline(self):
        self.add(Constant("\n"))

    def generate(self, resolver: "Resolver") -> str:
        return "".join([str(resolver.resolve(value)) for value in self.values])
