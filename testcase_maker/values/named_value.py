from typing import Any, TYPE_CHECKING, Union

import attr

from testcase_maker.value import Value

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class NamedValue(Value):
    name: str = attr.ib()
    value: Union[Any, "Value"] = attr.ib()

    def generate(self, resolver: "Resolver") -> Any:
        return resolver.resolve(self.value)
