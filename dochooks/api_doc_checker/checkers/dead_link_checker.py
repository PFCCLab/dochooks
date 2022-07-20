from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import docutils.nodes
import httpx

from ..._compat import cache
from .checker import Checker

REGEX_EXTERNAL_LINK = re.compile(r"^[\w\.\-]+://")
REGEX_HTTP_LINK = re.compile(r"^https?://")


class DeadLinkChecker(Checker):
    _links: list[tuple[Optional[int], str]] = []

    def visit_reference(self, node: docutils.nodes.Element):

        uri = node.get("refuri")
        self._links.append((node.line, uri))

    @property
    def result(self) -> bool:
        for lineno, link in self._links:
            if REGEX_EXTERNAL_LINK.match(link):
                if not REGEX_HTTP_LINK.match(link):
                    # Ignore the unknown protocols
                    continue

                # 有点慢啊，可以考虑禁用，或者考虑利用协程
                if not check_http_link_is_available(link):
                    print(f"{self.source_path}:{lineno}: Dead http link: {link}")
                    return False
            else:
                link_path = Path(clean_link(link))
                if link_path.is_absolute():
                    print(f"{self.source_path}:{lineno}: Found absolute file link: {link}")
                    return False

                if not check_path_link_is_available(self.source_path, link_path):
                    print(f"{self.source_path}:{lineno}: Dead file link: {link}")
                    return False
        return True


@cache
def check_http_link_is_available(link: str) -> bool:
    try:
        resp = httpx.head(link)
        if resp.status_code >= 400:
            return False
        resp.close()
        return True
    except httpx.HTTPError:
        return False


def clean_link(link: str) -> str:
    link = re.sub(r"[?#].*$", "", link)
    print(link)
    return link


@cache
def check_path_link_is_available(source_path: Path | str, link_path: Path | str) -> bool:
    source_dir = Path(source_path).parent
    file_path = (source_dir / link_path).resolve()

    if str(file_path).endswith("/"):
        return (
            file_path.exists()
            or (file_path / "index.rst").resolve().exists()
            or (file_path / "index.md").resolve().exists()
            or (file_path / "index.html").resolve().exists()
            or (file_path / "README.rst").resolve().exists()
            or (file_path / "README.md").resolve().exists()
        )

    if file_path.suffix in [".rst", ".md", ".html"]:
        return (
            file_path.exists()
            or file_path.with_suffix(".rst").exists()
            or file_path.with_suffix(".md").exists()
            or file_path.with_suffix(".html").exists()
        )
    return file_path.exists()
