from __future__ import annotations

import re
from typing import Pattern

IDENTIFIER_PATTERN: str = r"[a-zA-Z_][a-zA-Z0-9_]*"
REGEX_IS_IDENTIFIER: Pattern[str] = re.compile(f"^{IDENTIFIER_PATTERN}$")


def is_valid_identifier(identifier: str) -> bool:
    return REGEX_IS_IDENTIFIER.match(identifier) is not None
