from typing import TYPE_CHECKING

import attr

from testcase_maker.value import Value

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class Range(Value):
    min: int = attr.ib()
    max: int = attr.ib()
    step: int = attr.ib(default=1)

    def generate(self, resolver: "Resolver") -> range:
        min_range = resolver.resolve(self.min, int)
        max_range = resolver.resolve(self.max, int)
        step = resolver.resolve(self.step, int)
        return range(min_range, max_range, step)
