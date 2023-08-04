from __future__ import annotations

import pytest

from dochooks.insert_whitespace_between_cn_and_en_char.check import check
from dochooks.insert_whitespace_between_cn_and_en_char.format import format

NEED_FORMAT: bool = True
NEEDNT_FORMAT: bool = False

cases: list[tuple[bool, str, str]] = [
    (NEEDNT_FORMAT, "\n", "\n"),
    (NEEDNT_FORMAT, "", ""),
    (NEEDNT_FORMAT, "中文", "中文"),
    (NEED_FORMAT, "中文a", "中文 a"),
    (NEEDNT_FORMAT, "中文\na", "中文\na"),
    (NEED_FORMAT, "中a文", "中 a 文"),
    (
        NEED_FORMAT,
        "这是一行，a line\r\nthe next line呀！\n没了a",
        "这是一行，a line\r\nthe next line 呀！\n没了 a",
    ),
    (
        NEEDNT_FORMAT,
        r"由于没有语法分析，因此并不能将这个与[Python](python.org)分开，公式$\sqrt{\frac{1}{n}}$也是一样",
        r"由于没有语法分析，因此并不能将这个与[Python](python.org)分开，公式$\sqrt{\frac{1}{n}}$也是一样",
    ),
    (
        NEEDNT_FORMAT,
        "不会做额外的事情\r\n比如将在文末插入换行符",
        "不会做额外的事情\r\n比如将在文末插入换行符",
    ),
    (
        NEED_FORMAT,
        """
    这是一段长文本，会混杂一些英文
    啦啦啦，char喵喵喵en啊啦啦啦。xxxx
    en，char。
    """,
        """
    这是一段长文本，会混杂一些英文
    啦啦啦，char 喵喵喵 en 啊啦啦啦。xxxx
    en，char。
    """,
    ),
]


@pytest.mark.parametrize("need_format, unformatted, formatted", cases)
def test_check_and_format(need_format: bool, unformatted: str, formatted: str):
    if need_format:
        assert not check(unformatted)
    else:
        assert unformatted == formatted
        assert check(unformatted)

    assert format(unformatted) == formatted
    # Test format process is stable
    assert check(formatted)
    assert format(formatted) == formatted
