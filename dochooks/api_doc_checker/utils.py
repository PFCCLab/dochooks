from __future__ import annotations

import re
from typing import Pattern

PATTERN_IDENTIFIER: str = r"[a-zA-Z_][a-zA-Z0-9_]*"
REGEX_IS_IDENTIFIER: Pattern[str] = re.compile(PATTERN_IDENTIFIER)


def is_valid_identifier(identifier: str) -> bool:
    return REGEX_IS_IDENTIFIER.fullmatch(identifier) is not None
