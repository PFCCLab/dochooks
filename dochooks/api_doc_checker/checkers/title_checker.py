from __future__ import annotations

import docutils.nodes

from ..utils import is_valid_identifier
from .checker import Checker


class TitleChecker(Checker):
    VALID_H2_TITLES = [
        "参数",
        "返回",
        "属性",
        "方法",
        "代码示例",
    ]
    REQUIRED_H2_TITLES: list[str] = [
        "参数",
        "代码示例",
    ]
    section_level = 0
    titles: dict[int, list[str]] = {}

    def _add_title(self, level: int, title: str):
        if level not in self.titles:
            self.titles[level] = []
        self.titles[level].append(title)

    def visit_section(self, node: docutils.nodes.Element):
        self.section_level += 1

    def depart_section(self, node: docutils.nodes.Element):
        self.section_level -= 1

    def visit_title(self, node: docutils.nodes.Element) -> None:
        self._add_title(self.section_level, node.rawsource)

    @property
    def result(self) -> bool:
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
            if h2_title not in self.VALID_H2_TITLES:
                print(
                    f"{self.source_path}: Invalid h2 title ({h2_title}) found. Allowed titles: {self.VALID_H2_TITLES}"
                )
                return False

        # 确保必须的二级标题均存在
        for required_h2_title in self.REQUIRED_H2_TITLES:
            if required_h2_title not in h2_titles:
                print(f"{self.source_path}: Required h2 title ({required_h2_title}) not found.")
                return False

        return True
