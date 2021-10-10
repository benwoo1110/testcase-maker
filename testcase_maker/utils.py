from pathlib import Path
from subprocess import Popen, PIPE
from typing import List, Optional


def run_command(args: List[str], stdin: Optional[str] = None, cwd: Optional["Path"] = None, encode_type: str = "UTF-8"):
    if stdin:
        stdin = stdin.encode()

    process = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=cwd)
    out = process.communicate(stdin)
    if out[1]:
        print(out[1].decode(encode_type))
        raise Exception("Error executing answer script.")

    return out[0].decode(encode_type)
