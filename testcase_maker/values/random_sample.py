import random
from typing import Any, TYPE_CHECKING, List, Union

import attr

from testcase_maker.value import Value

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class RandomSample(Value):
    items: Union[Value, List[Union[Value, Any]]] = attr.ib()
    amount: Union[Value, int] = attr.ib()
    delimiter: Union[Value, str] = attr.ib()

    def generate(self, resolver: "Resolver") -> Any:
        items = resolver.resolve(self.items, list)
        amount = resolver.resolve(self.amount, int)
        delimiter = resolver.resolve(self.delimiter, str)
        return delimiter.join([str(n) for n in random.sample(items, amount)])
