from __future__ import annotations

import pytest

from dochooks.insert_whitespace_between_cn_and_en_char.check import check_lines
from dochooks.insert_whitespace_between_cn_and_en_char.format import format_lines

NEED_FORMAT: bool = True
NEEDNT_FORMAT: bool = False
cases = [
    (NEEDNT_FORMAT, "中文and英文 # dochooks: skip-line", "中文and英文 # dochooks: skip-line"),
    (
        NEED_FORMAT,
        """
    中文English # 需要格式化
    中文English # dochooks: skip-line
    中文English # 需要格式化
    中文English # dochooks: skip-line
    中文English # 需要格式化
    # dochooks: skip-next-line
    中文English
    中文English # 需要格式化
    # dochooks: skip-next-line
    中文English
    中文English # 需要格式化
    """,
        """
    中文 English # 需要格式化
    中文English # dochooks: skip-line
    中文 English # 需要格式化
    中文English # dochooks: skip-line
    中文 English # 需要格式化
    # dochooks: skip-next-line
    中文English
    中文 English # 需要格式化
    # dochooks: skip-next-line
    中文English
    中文 English # 需要格式化
    """,
    ),
]


@pytest.mark.parametrize("need_format, unformatted, formatted", cases)
def test_check_and_format_lines(need_format: bool, unformatted: str, formatted: str):
    need_format_from_check, _ = check_lines(unformatted.splitlines(keepends=True))
    need_format_from_format, formatted_text, _ = format_lines(unformatted.splitlines(keepends=True))
    assert need_format_from_check == need_format
    assert need_format_from_format == need_format

    assert formatted_text == formatted
