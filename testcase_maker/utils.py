import logging
from enum import Enum
from pathlib import Path
from subprocess import Popen, PIPE
from typing import List, Optional, Union

from testcase_maker.constants import LOGGER_NAME

log = logging.getLogger(LOGGER_NAME)


def run_command(args: List[str], stdin: Optional[str] = None, cwd: Optional[Union[Path, str]] = None, encode_type: str = "UTF-8"):
    if stdin:
        stdin = stdin.encode()

    process = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=cwd)
    out = process.communicate(stdin)
    if out[1]:
        log.error(out[1].decode(encode_type))
        log.error("Error executing answer script.")

    return out[0].decode(encode_type)


class NewlineTypes(str, Enum):
    CRLF = "\r\n"
    LF = "\n"
    CR = "\r"
