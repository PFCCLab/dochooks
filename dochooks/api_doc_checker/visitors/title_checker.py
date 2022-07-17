from __future__ import annotations

import docutils
import docutils.nodes
import docutils.parsers.rst

from typing import Any
from ..utils import is_valid_identifier


Node = Any  # docutils.nodes.Node, avoid type error


class TitleChecker(docutils.nodes.NodeVisitor):
    section_level = 0
    titles: dict[int, list[str]] = {}
    valid_h2_titles = [
        "参数",
        "返回",
        "属性",
        "代码示例",
    ]
    required_h2_titles: list[str] = [
        "参数",
        "代码示例",
    ]

    def _add_title(self, level: int, title: str):
        if level not in self.titles:
            self.titles[level] = []
        self.titles[level].append(title)

    def visit_section(self, node: Node):
        self.section_level += 1

    def depart_section(self, node: Node):
        self.section_level -= 1

    def visit_title(self, node: Node) -> None:

        self._add_title(self.section_level, node.rawsource)

    def unknown_visit(self, node: Node) -> None:
        pass

    def unknown_departure(self, node: Node) -> None:
        pass

    @property
    def source_path(self) -> str:
        return self.document.get("source")

    def check(self) -> bool:
        # 确保存在标题
        if not self.titles:
            print(f"{self.source_path}: No titles found.")
            return False

        # 确保存在（一级）标题
        h1_titles = self.titles.get(1)
        if not h1_titles:
            print(f"{self.source_path}: No h1 title found.")
            return False

        # 确保一级标题唯一
        assert h1_titles is not None
        if len(h1_titles) > 1:
            print(f"{self.source_path}: More than one h1 title found.")
            return False

        # 确保一级标题合法，即合法的变量名
        h1_title = h1_titles[0]
        if not is_valid_identifier(h1_title):
            print(f"{self.source_path}: Invalid h1 title ({h1_title}) found.")
            return False

        # 确保存在二级标题
        h2_titles = self.titles.get(2)
        if not h2_titles:
            print(f"{self.source_path}: No h2 title found.")
            return False

        # 确保二级标题均合法，即为允许的列表内容
        for h2_title in h2_titles:
            if h2_title not in self.valid_h2_titles:
                print(
                    f"{self.source_path}: Invalid h2 title ({h2_title}) found. Allowed titles: {self.valid_h2_titles}"
                )
                return False

        # 确保必须的二级标题均存在
        for required_h2_title in self.required_h2_titles:
            if required_h2_title not in h2_titles:
                print(f"{self.source_path}: Required h2 title ({required_h2_title}) not found.")
                return False

        return True
