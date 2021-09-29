from typing import TYPE_CHECKING, Union, Any

import attr

from testcase_maker.value import Value

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class LoopValue(Value):
    value: Union[Any, "Value"] = attr.ib()
    amount: Union[int, "Value"] = attr.ib()
    delimiter: Union[str, "Value"] = attr.ib(default=" ")

    def generate(self, resolver: "Resolver") -> str:
        amount = resolver.resolve(self.amount, int)
        delimiter = resolver.resolve(self.delimiter, str)
        return delimiter.join([str(resolver.resolve(self.value)) for _ in range(amount)])
