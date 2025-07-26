from __future__ import annotations

import argparse
from collections.abc import Iterable, Sequence

from dochooks import __version__

from ..utils.return_code import FAIL, PASS, ReturnCode
from .check import check
from .pragma import PragmaManager
from .regex import REGEX_CN_WITH_EN, REGEX_EN_WITH_CN


def format(text: str) -> str:
    text = REGEX_CN_WITH_EN.sub(r"\g<cn> \g<en>", text)
    text = REGEX_EN_WITH_CN.sub(r"\g<en> \g<cn>", text)
    return text


def format_lines(lines: Iterable[str]) -> tuple[bool, str, list[tuple[int, str]]]:
    formatted_text: str = ""
    diagnostics: list[tuple[int, str]] = []
    need_format = False
    pragma_manager = PragmaManager()
    for lineno, line in enumerate(lines, 1):
        with pragma_manager.scan(line) as skip_line:
            if skip_line:
                formatted_text += line
                continue
            if not check(line):
                line = format(line)
                need_format = True
                diagnostics.append((lineno, line))
            formatted_text += line
    return need_format, formatted_text, diagnostics


def _format_file(file_path: str) -> ReturnCode:
    with open(file_path, encoding="utf8", newline="\n") as f:
        need_format, formatted_text, diagnostics = format_lines(f)

    if formatted_text:
        with open(file_path, "w", encoding="utf8", newline="\n") as f:
            f.write(formatted_text)
        for lineno, line in diagnostics:
            print(f"Add spaces between EN and CN chars in: {file_path}:{lineno}:\t{line.strip()}")
    return FAIL if need_format else PASS


def main(argv: Sequence[str] | None = None) -> ReturnCode:
    parser = argparse.ArgumentParser(prog="dochooks", description="pre-commit hooks for documentation")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument("filenames", nargs="*", help="Filenames to check")
    args = parser.parse_args(argv)

    ret_code: ReturnCode = PASS
    for filename in args.filenames:
        ret_code |= _format_file(filename)

    if ret_code != PASS:
        print("")
        print("Snuged en and cn chars have been separated by a space. Now aborting the commit.")
        print('You can check the changes made. Then simply "git add --update ." and re-commit')
        print(
            "If the changes are not correct, you can @SigureMo in that PR, or directly open a issue in https://github.com/ShigureLab/dochooks"
        )
    return ret_code


if __name__ == "__main__":
    raise SystemExit(main())
