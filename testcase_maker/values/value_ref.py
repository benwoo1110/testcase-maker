from typing import Any, TYPE_CHECKING

import attr

from testcase_maker.values import BaseValue

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class ValueRef(BaseValue):
    name: Any = attr.ib()

    def generate(self, resolver: "Resolver") -> Any:
        var_name = resolver.resolve(self.name)
        return resolver.get_value(var_name)
