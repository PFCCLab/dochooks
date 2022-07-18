from __future__ import annotations

import re
from typing import Pattern

from .._compat import Final

REGEX_CN_CHAR_STR: Final[str] = r"[\u4e00-\u9fa5]"
REGEX_EN_CHAR_STR: Final[str] = r"[a-zA-Z0-9]"

REGEX_CN_WITH_EN: Pattern[str] = re.compile(f"(?P<cn>{REGEX_CN_CHAR_STR})(?P<en>{REGEX_EN_CHAR_STR})")
REGEX_EN_WITH_CN: Pattern[str] = re.compile(f"(?P<en>{REGEX_EN_CHAR_STR})(?P<cn>{REGEX_CN_CHAR_STR})")
