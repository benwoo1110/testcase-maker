from pathlib import Path
from subprocess import Popen, PIPE
from typing import List


def run_command(args: List[str], stdin: str = None, cwd: "Path" = None):
    if stdin:
        stdin = stdin.encode()

    process = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=cwd)
    out = process.communicate(stdin)
    if out[1]:
        print(out[1].decode("UTF-8"))
        raise Exception("Error executing answer script.")

    return out[0].decode("utf-8")
