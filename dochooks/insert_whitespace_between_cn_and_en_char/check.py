from __future__ import annotations

import argparse
from typing import Sequence

from dochooks import __version__

from ..utils.return_code import FAIL, PASS, ReturnCode
from .regex import REGEX_CN_WITH_EN, REGEX_EN_WITH_CN


def check(string: str) -> bool:
    if REGEX_CN_WITH_EN.search(string) or REGEX_EN_WITH_CN.search(string):
        return False
    return True


def _check_file(file_path: str) -> ReturnCode:
    return_code = PASS
    with open(file_path, encoding="utf8", newline="\n") as f:
        for lineno, line in enumerate(f, 1):
            if not check(line):
                print(f"No spaces between EN and CN chars detected at: {file_path}:{lineno}:\t{line}")
                return_code = FAIL
    return return_code


def main(argv: Sequence[str] | None = None) -> ReturnCode:
    parser = argparse.ArgumentParser(prog="dochooks", description="pre-commit hooks for documentation")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument("filenames", nargs="*", help="Filenames to check")
    args = parser.parse_args(argv)

    ret_code: ReturnCode = PASS
    for filename in args.filenames:
        ret_code |= _check_file(filename)
    return ret_code


if __name__ == "__main__":
    raise SystemExit(main())
