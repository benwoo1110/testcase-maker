from typing import TYPE_CHECKING

import attr

from testcase_maker.values import ValueContainer

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class LoopValue(ValueContainer):
    amount = attr.ib()
    delimiter: str = attr.ib()

    def generate(self, resolver: "Resolver") -> str:
        amount = resolver.resolve(self.amount)
        delimiter = resolver.resolve(self.delimiter)
        return delimiter.join([str(resolver.resolve(self.value)) for _ in range(amount)])
