from __future__ import annotations

try:
    from typing import Literal  # type: ignore
except ImportError:
    from typing_extensions import Literal  # type: ignore

try:
    from typing import Final  # type: ignore
except ImportError:
    from typing_extensions import Final  # type: ignore

try:
    from typing import TypeAlias  # type: ignore
except ImportError:
    from typing_extensions import TypeAlias  # type: ignore

try:
    from typing import TypedDict  # type: ignore
except ImportError:
    from typing_extensions import TypedDict  # type: ignore

try:
    from typing import assert_type  # type: ignore
except ImportError:
    from typing_extensions import assert_type  # type: ignore

try:
    from functools import cache  # type: ignore
except ImportError:
    from functools import lru_cache  # type: ignore

    cache = lru_cache(maxsize=None)

__all__ = ["Literal", "Final", "TypeAlias", "TypedDict", "assert_type", "cache"]
