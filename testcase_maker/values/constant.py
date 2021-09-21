from typing import Any, TYPE_CHECKING

import attr

from testcase_maker.value import Value

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class Constant(Value):
    constant: Any = attr.ib()

    def generate(self, resolver: "Resolver") -> Any:
        return resolver.resolve(self.constant)
