import random
from typing import TYPE_CHECKING, Union

import attr

from testcase_maker.value import Value

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class RandomInt(Value):
    min: Union[int, "Value"] = attr.ib()
    max: Union[int, "Value"] = attr.ib()

    def generate(self, resolver: "Resolver") -> int:
        min_range = resolver.resolve(self.min, int)
        max_range = resolver.resolve(self.max, int)
        return random.randint(min_range, max_range)
