from __future__ import annotations

import argparse
from typing import Optional, Sequence

import docutils.frontend
import docutils.nodes
import docutils.parsers.rst
import docutils.parsers.rst.states
import docutils.utils

from dochooks import __version__

from ..utils.return_code import FAIL, PASS, ReturnCode
from .core.directives import preset_sphinx_directives
from .core.roles import preset_sphinx_roles


def parse_rst(text: str) -> docutils.nodes.document:
    parser = docutils.parsers.rst.Parser()

    preset_sphinx_roles()
    preset_sphinx_directives()

    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(components=components).get_default_values()
    document = docutils.utils.new_document("<rst-doc>", settings=settings)
    parser.parse(text, document)
    return document


def check(text: str) -> bool:
    rst_ast = parse_rst(text)
    # checker = APIDocChecker(rst_ast)
    # rst_ast.walk(checker)
    print(rst_ast)
    return False


def _check_file(file_path: str) -> ReturnCode:
    return_code = PASS
    with open(file_path, "r", encoding="utf8", newline="\n") as f:
        content = f.read()
        if check(content):
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
