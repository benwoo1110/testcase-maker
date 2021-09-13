from typing import Any, TYPE_CHECKING

import attr

from testcase_maker.values.base import ValueContainer

if TYPE_CHECKING:
    from testcase_maker.core import Resolver


@attr.define()
class NamedValue(ValueContainer):
    name: Any = attr.ib()

    def generate(self, resolver: "Resolver") -> Any:
        return resolver.resolve(self.value)
