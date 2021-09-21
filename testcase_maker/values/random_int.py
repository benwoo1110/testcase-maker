import random
from typing import TYPE_CHECKING

import attr

from testcase_maker.value import Value

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class RandomInt(Value):
    min: int = attr.ib()
    max: int = attr.ib()

    def generate(self, resolver: "Resolver") -> int:
        min_range = resolver.resolve(self.min, int)
        max_range = resolver.resolve(self.max, int)
        return random.randint(min_range, max_range)
