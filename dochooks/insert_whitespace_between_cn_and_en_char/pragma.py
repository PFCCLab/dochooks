from __future__ import annotations

from contextlib import contextmanager
from enum import Enum


class Pragma(Enum):
    SKIP_NEXT_LINE = "dochooks: skip-next-line"
    SKIP_LINE = "dochooks: skip-line"


class PragmaManager:
    def __init__(self):
        self.skip_line = False

    @contextmanager
    def scan(self, line: str):
        if Pragma.SKIP_LINE.value in line:
            self.skip_line = True
        yield self.skip_line
        self.skip_line = False
        if Pragma.SKIP_NEXT_LINE.value in line:
            self.skip_line = True
