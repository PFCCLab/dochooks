from __future__ import annotations

import argparse
from typing import Optional, Sequence

from dochooks import __version__

from ..utils.return_code import FAIL, PASS, ReturnCode
from .regex import REGEX_CN_WITH_EN, REGEX_EN_WITH_CN


def check(string: str) -> bool:
    if REGEX_CN_WITH_EN.search(string) or REGEX_EN_WITH_CN.search(string):
        return True
    return False


def _check_file(file_path: str) -> ReturnCode:
    return_code = PASS
    with open(file_path, "r", encoding="utf8", newline="\n") as f:
        for lineno, line in enumerate(f, 1):
            if check(line):
                print(f"{file_path}:{lineno}:\t{line}")
                return_code = FAIL
    return return_code


def main(argv: Optional[Sequence[str]] = None) -> ReturnCode:
    parser = argparse.ArgumentParser(prog="dochooks", description="pre-commit hooks for documentation")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument("filenames", nargs="*", help="Filenames to check")
    args = parser.parse_args(argv)

    ret_code: ReturnCode = PASS
    for filename in args.filenames:
        ret_code |= _check_file(filename)
        # path.
    return ret_code


if __name__ == "__main__":
    raise SystemExit(main())
