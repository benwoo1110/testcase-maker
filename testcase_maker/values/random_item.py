import random
from typing import Any, TYPE_CHECKING, List, Union

import attr

from testcase_maker.value import Value

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class RandomItem(Value):
    items: List[Union[Value, Any]] = attr.ib()

    def generate(self, resolver: "Resolver") -> Any:
        item = random.choice(self.items)
        return resolver.resolve(item)
