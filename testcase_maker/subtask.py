from typing import Dict, TYPE_CHECKING, Any, Iterator, List, Tuple, Union

import attr

if TYPE_CHECKING:
    from testcase_maker.value import Value


@attr.define()
class Edgecase:
    override_name_values: Dict[str, Union[Any, "Value"]] = attr.ib(factory=dict)

    def override_value(self, name: str, value: Union[Any, "Value"]):
        self.override_name_values[name] = value


@attr.define()
class Subtask:
    name: str = attr.ib()
    no_of_testcase: int = attr.ib()
    override_name_values: Dict[str, Union[Any, "Value"]] = attr.ib(factory=dict)
    edgecases: List[Edgecase] = attr.ib(factory=list)

    def new_edgecase(self) -> Edgecase:
        self.edgecases.append(Edgecase())
        if len(self.edgecases) > self.no_of_testcase:
            raise ValueError("Number of edgecases more than number of testcases for subtask.")
        return self.edgecases[-1]

    def override_value(self, name: str, value: Union[Any, "Value"]):
        self.override_name_values[name] = value

    def iterate(self) -> Iterator[Tuple[int, Dict[str, Union[Any, "Value"]]]]:
        generic_amount = self.no_of_testcase - len(self.edgecases)
        for t_num in range(1, generic_amount + 1):
            yield (t_num, self.override_name_values)

        for t_num, edgecase in enumerate(self.edgecases, generic_amount + 1):
            yield (t_num, edgecase.override_name_values)
