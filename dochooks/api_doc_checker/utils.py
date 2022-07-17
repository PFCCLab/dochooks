from __future__ import annotations

import re
from typing import Pattern

REGEX_IS_IDENTIFIER: Pattern[str] = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def is_valid_identifier(identifier: str) -> bool:
    return REGEX_IS_IDENTIFIER.match(identifier) is not None
