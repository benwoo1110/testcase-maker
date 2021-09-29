from abc import ABC
from typing import Any, TYPE_CHECKING

import attr

if TYPE_CHECKING:
    from testcase_maker.resolver import Resolver


@attr.define()
class Value(ABC):
    def generate(self, resolver: "Resolver") -> Any:
        raise NotImplementedError
