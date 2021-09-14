import random
from typing import Any, TYPE_CHECKING, List, Union

import attr

from testcase_maker.values.base import BaseValue

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class RandomSample(BaseValue):
    items: Union[BaseValue, List[Union[BaseValue, Any]]] = attr.ib()
    amount: Union[BaseValue, int] = attr.ib()
    delimiter: Union[BaseValue, str] = attr.ib()

    def generate(self, resolver: "Resolver") -> Any:
        items = resolver.resolve(self.items, list)
        amount = resolver.resolve(self.amount, int)
        delimiter = resolver.resolve(self.delimiter, str)
        return delimiter.join([str(n) for n in random.sample(items, amount)])
