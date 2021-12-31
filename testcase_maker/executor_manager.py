import inspect
from pathlib import Path
from typing import Type, Union

from testcase_maker import executors
from testcase_maker.executor import Executor


_registered_executors = {}


def register_executor(executor: Type[Executor], override: bool = False):
    file_extension = executor.file_extension()
    if file_extension in _registered_executors and not override:
        raise ValueError(
            f"Executor with extension '{file_extension}' already exist. Set override to True to "
            f"replace existing registered executor with the same file extension."
        )
    _registered_executors[file_extension] = executor


def get_executor_for_script(script_file: Union["Path", str]) -> Executor:
    script_file = Path(script_file)
    file_extension = Path(script_file).suffix

    try:
        executor = _registered_executors[file_extension]
    except KeyError:
        raise ValueError(f"No registered executor for script '{script_file}' with extension '{file_extension}'.")

    return executor(script_file)


def _register_builtin_executors():
    modules = inspect.getmembers(executors, inspect.ismodule)
    for module in modules:
        classes = inspect.getmembers(module[1], inspect.isclass)
        for cls in classes:
            if cls[1] is Executor or not issubclass(cls[1], Executor):
                continue
            register_executor(cls[1])


_register_builtin_executors()
