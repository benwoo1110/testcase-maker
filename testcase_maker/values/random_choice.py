import random
from typing import Any, TYPE_CHECKING, List, Union

import attr

from testcase_maker.value import Value

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class RandomChoice(Value):
    items: List[Union[Any, "Value"]] = attr.ib()  # TODO Make this resolvable?

    def generate(self, resolver: "Resolver") -> Any:
        return resolver.resolve(random.choice(self.items))
