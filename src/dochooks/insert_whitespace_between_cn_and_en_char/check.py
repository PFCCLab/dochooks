from __future__ import annotations

import argparse
from collections.abc import Iterable, Sequence

from dochooks import __version__

from ..utils.return_code import FAIL, PASS, ReturnCode
from .pragma import PragmaManager
from .regex import REGEX_CN_WITH_EN, REGEX_EN_WITH_CN


def check(string: str) -> bool:
    if REGEX_CN_WITH_EN.search(string) or REGEX_EN_WITH_CN.search(string):
        return False
    return True


def check_lines(lines: Iterable[str]) -> tuple[bool, list[tuple[int, str]]]:
    diagnostics: list[tuple[int, str]] = []
    need_format = False
    pragma_manager = PragmaManager()
    for lineno, line in enumerate(lines, 1):
        with pragma_manager.scan(line) as skip_line:
            if skip_line:
                continue
            if not check(line):
                need_format = True
                diagnostics.append((lineno, line))
    return need_format, diagnostics


def _check_file(file_path: str) -> ReturnCode:
    with open(file_path, encoding="utf8", newline="\n") as f:
        need_format, diagnostics = check_lines(f)
    if need_format:
        for lineno, line in diagnostics:
            print(f"No spaces between EN and CN chars detected at: {file_path}:{lineno}:\t{line.strip()}")
    return FAIL if need_format else PASS


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
