import random
from typing import Any, TYPE_CHECKING, List, Union

import attr

from testcase_maker.value import Value

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class RandomSample(Value):
    items: Union[List[Union[Value, Any]], "Value"] = attr.ib()
    amount: Union[int, "Value"] = attr.ib()
    delimiter: Union[str, "Value"] = attr.ib(default=" ")

    def generate(self, resolver: "Resolver") -> Any:
        items = resolver.resolve(self.items)
        amount = resolver.resolve(self.amount, int)
        delimiter = resolver.resolve(self.delimiter, str)
        return delimiter.join([str(item) for item in random.sample(items, amount)])
