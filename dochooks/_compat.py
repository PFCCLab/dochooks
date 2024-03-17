from __future__ import annotations

import sys

if sys.version_info >= (3, 9):
    from functools import cache  # type: ignore
else:
    from functools import lru_cache  # type: ignore

    cache = lru_cache(maxsize=None)

__all__ = ["cache"]
