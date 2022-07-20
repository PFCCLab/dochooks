from __future__ import annotations

import argparse
from typing import Optional, Sequence

from dochooks import __version__

from ..utils.return_code import FAIL, PASS, ReturnCode
from .checkers import (
    CodeExampleChecker,
    DeadLinkChecker,
    ParametersChecker,
    TitleChecker,
    create_chained_checker,
)
from .core.parser import parse_rst


def check(text: str, file_path: str = "<rst-doc>") -> bool:
    rst_ast = parse_rst(text, file_path=file_path)
    # print(rst_ast.pformat())
    check_result = create_chained_checker(
        [
            TitleChecker,
            CodeExampleChecker,
            ParametersChecker,
            DeadLinkChecker,
        ],
        False,
    ).check(rst_ast)
    print("Check result:", check_result)
    return check_result


def _check_file(file_path: str) -> ReturnCode:
    return_code = PASS
    with open(file_path, "r", encoding="utf8", newline="\n") as f:
        content = f.read()
        if not check(content, file_path):
            # print(f"No spaces between EN and CN chars detected at: {file_path}:{lineno}:\t{line}")
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
    return ret_code


if __name__ == "__main__":
    raise SystemExit(main())
