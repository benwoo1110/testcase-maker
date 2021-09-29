from typing import Dict, Any, Optional, Union

import attr

from testcase_maker.value import Value
from testcase_maker.values import NamedValue


@attr.define()
class Resolver:
    _override_name_values: Dict[str, "Value"] = attr.ib(factory=dict)
    _resolved_values: Dict[str, Any] = attr.ib(factory=dict)

    def get_override(self, name: str, default: Optional[Value] = None) -> "Value":
        return self._override_name_values.get(name, default)

    def get_value(self, name: str) -> Optional[Any]:
        if name not in self._resolved_values:
            raise ValueError(f"No such resolved variable '{name}'.")
        return self._resolved_values[name]

    def resolve(self, value: Union[Value, Any], check_type: type = None) -> Any:
        if isinstance(value, NamedValue):
            target_value = self.get_override(value.name, value.value)
            resolved_value = self.resolve(target_value, check_type)
            self._resolved_values[value.name] = resolved_value
            return resolved_value

        if isinstance(value, Value):
            value = value.generate(self)

        if check_type and not isinstance(value, check_type):
            raise TypeError(f"Expected type '{check_type}', but got type '{type(value)}' instead.")

        return value
