import inspect
from pathlib import Path
from typing import Union

from testcase_maker import executors
from testcase_maker.executor import Executor


_registered_executors = {}


def register_executor(executor: Executor, override: bool = False) -> Executor:
    if executor.file_extension in _registered_executors and not override:
        raise ValueError(
            f"Executor with extension '{executor.file_extension}' already exist. Set override to True to "
            f"replace existing registered executor with the same file extension."
        )

    _registered_executors[executor.file_extension] = executor
    return executor


def get_executor_for_script(script_filename: Union["Path", str]) -> Executor:
    try:
        file_extension = str(script_filename).rsplit(".", 1)[1]
    except IndexError:
        raise ValueError(f"Script '{script_filename}' does not have a file extension.")

    try:
        executor = _registered_executors[file_extension]
    except KeyError:
        raise ValueError(f"No registered executor for script '{script_filename}' with extension '{file_extension}'.")

    return executor


def _register_builtin_executors():
    modules = inspect.getmembers(executors, inspect.ismodule)
    for module in modules:
        classes = inspect.getmembers(module[1], inspect.isclass)
        for cls in classes:
            if cls[1] is Executor or not issubclass(cls[1], Executor):
                continue
            register_executor(cls[1]())


_register_builtin_executors()
