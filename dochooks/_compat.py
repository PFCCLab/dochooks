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
    from typing import assert_type  # type: ignore
except ImportError:
    from typing_extensions import assert_type

__all__ = ["Literal", "Final", "TypeAlias", "assert_type"]
