import random
from typing import Any, TYPE_CHECKING, List, Union

import attr

from testcase_maker.values.base import BaseValue

if TYPE_CHECKING:
    from testcase_maker.core import Resolver


@attr.define()
class RandomItem(BaseValue):
    items: List[Union[BaseValue, Any]] = attr.ib()

    def generate(self, resolver: "Resolver") -> Any:
        item = random.choice(self.items)
        return resolver.resolve(item)
