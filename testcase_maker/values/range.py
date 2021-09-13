from typing import Any, TYPE_CHECKING

import attr

from testcase_maker.values.base import BaseValue

if TYPE_CHECKING:
    from testcase_maker.core import Resolver


@attr.define()
class Range(BaseValue):
    min: int = attr.ib()
    max: int = attr.ib()
    step: int = attr.ib(default=1)

    def generate(self, resolver: "Resolver") -> list:
        min_range = resolver.resolve(self.min, int)
        max_range = resolver.resolve(self.max, int)
        step = resolver.resolve(self.step, int)
        return list(range(min_range, max_range, step))
