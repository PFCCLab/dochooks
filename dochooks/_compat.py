from __future__ import annotations

try:
    from typing import Literal  # type: ignore
except ImportError:
    from typing_extensions import Literal

try:
    from typing import Final  # type: ignore
except ImportError:
    from typing_extensions import Final

try:
    from typing import TypeAlias  # type: ignore
except ImportError:
    from typing_extensions import TypeAlias

try:
    from typing import TypedDict  # type: ignore
except ImportError:
    from typing_extensions import TypedDict

__all__ = ["Literal", "Final", "TypeAlias", "TypedDict"]
