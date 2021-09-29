import time
from pathlib import Path
from subprocess import Popen, PIPE
from typing import List

import attr


def run_command(args: List[str], stdin: str = None, cwd: "Path" = None):
    if stdin:
        stdin = stdin.encode()

    process = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=cwd)
    out = process.communicate(stdin)
    if out[1]:
        print(out[1].decode("UTF-8"))
        raise Exception("Error executing answer script.")

    return out[0].decode("utf-8")


class Timer:
    start_time: float = attr.ib(default=-1, init=False)
    end_time: float = attr.ib(default=-1, init=False)

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def start(self):
        self.start_time = time.perf_counter()

    def end(self) -> float:
        self.end_time = time.perf_counter()
        return self.duration
