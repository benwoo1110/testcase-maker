from typing import Dict, Any, Optional, Union

import attr

from testcase_maker.value import Value
from testcase_maker.values import NamedValue


@attr.define()
class Resolver:
    _override_name_values: Dict = attr.ib(factory=dict)
    _resolved_values: Dict = attr.ib(factory=dict)

    def get_override(self, name: Any, default: Optional[Value] = None):
        return self._override_name_values.get(name, default)

    def get_value(self, var_name: Any) -> Optional[Any]:
        if var_name not in self._resolved_values:
            raise ValueError(f"No such resolved variable '{var_name}'.")
        return self._resolved_values[var_name]

    def resolve(self, value: Union[Value, Any], check_type: type = None):
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
