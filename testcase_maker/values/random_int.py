import random
from typing import Any, TYPE_CHECKING

import attr

from testcase_maker.values.base import BaseValue

if TYPE_CHECKING:
    from testcase_maker.core import Resolver


@attr.define()
class RandomInt(BaseValue):
    min: int = attr.ib()
    max: int = attr.ib()

    def generate(self, resolver: "Resolver") -> int:
        min_range = resolver.resolve(self.min, int)
        max_range = resolver.resolve(self.max, int)
        return random.randint(min_range, max_range)
