from typing import Any, TYPE_CHECKING, Callable, Union

import attr

from testcase_maker.value import Value

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class Apply(Value):
    value: Union[Any, "Value"] = attr.ib()
    func: Callable[[Any], Any] = attr.ib()

    def generate(self, resolver: "Resolver") -> Any:
        return self.func(resolver.resolve(self.value))
