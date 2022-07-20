from __future__ import annotations

import re

from dochooks.insert_whitespace_between_cn_and_en_char.regex import (
    REGEX_CN_CHAR_STR,
    REGEX_CN_WITH_EN,
    REGEX_EN_CHAR_STR,
    REGEX_EN_WITH_CN,
)


def test_pure_cn_chars_pattern():
    assert re.search(REGEX_CN_CHAR_STR, "纯中文") is not None
    assert re.search(REGEX_EN_CHAR_STR, "纯中文") is None
    assert re.search(REGEX_CN_CHAR_STR, "，") is None
    assert REGEX_CN_WITH_EN.search("纯中文") is None
    assert REGEX_EN_WITH_CN.search("纯中文") is None


def test_pure_en_chars_pattern():
    assert re.search(REGEX_EN_CHAR_STR, "Pure English") is not None
    assert re.search(REGEX_CN_CHAR_STR, "Pure English") is None
    assert REGEX_CN_WITH_EN.search("Pure English") is None
    assert REGEX_EN_WITH_CN.search("Pure English") is None


def test_cn_with_en_pattern():
    assert REGEX_CN_WITH_EN.search("中文后面带English") is not None
    assert REGEX_CN_WITH_EN.sub(r"\g<cn> \g<en>", "中文后面带English") == "中文后面带 English"
    assert REGEX_CN_WITH_EN.sub(r"\g<cn> \g<en>", "中文后面带English啦") == "中文后面带 English啦"


def test_en_with_cn_pattern():
    assert REGEX_EN_WITH_CN.search("English with中文字符") is not None
    assert REGEX_EN_WITH_CN.sub(r"\g<en> \g<cn>", "English with中文字符") == "English with 中文字符"
    assert REGEX_EN_WITH_CN.sub(r"\g<en> \g<cn>", "呀English with 中文字符") == "呀English with 中文字符"


def test_cn_with_punctuation_pattern():
    assert REGEX_CN_WITH_EN.sub(r"\g<cn> \g<en>", "带上标点符号试试，en。") == "带上标点符号试试，en。"
    assert REGEX_EN_WITH_CN.sub(r"\g<en> \g<cn>", "带上标点符号试试，en。") == "带上标点符号试试，en。"
