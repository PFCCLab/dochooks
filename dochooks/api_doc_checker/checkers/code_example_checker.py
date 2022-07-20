from __future__ import annotations

import re

import docutils.nodes

from ..utils import PATTERN_IDENTIFIER
from .checker import Checker


class CodeExampleChecker(Checker):
    CODE_EXAMPLE_SECTION_NAME = "代码示例"
    COPY_FROM_REGEX = re.compile(rf"COPY-FROM: {PATTERN_IDENTIFIER}(\.{PATTERN_IDENTIFIER})*(:[a-zA-Z0-9_\-]+)?")

    _check_result = True
    _section_name_stack: list[str] = []

    def visit_section(self, node: docutils.nodes.Element):
        node_names = node.get("names")
        if node_names:
            self._section_name_stack.append(node_names[0])
        else:
            self._section_name_stack.append(" <Unknown section title> ")

    def depart_section(self, node: docutils.nodes.Element):
        self._section_name_stack.pop()

    def visit_literal_block(self, node: docutils.nodes.Element):
        """
        检查示例代码块（directive code-block）
        """
        if not self.in_code_example_section:
            return

        # 检查代码示例是否已经使用 `COPY-FROM` 替换
        if node.get("is_directive") is True and node.get("directive_name") == "code-block":
            lineno = node.line
            print(
                f"{self.source_path}:{lineno}: Found a code block in the code example section. Please use `COPY-FROM` instead."
            )
            self._check_result = False

    def visit_paragraph(self, node: docutils.nodes.Element):
        """
        检查 COPY-FROM 段落
        """
        if not self.in_code_example_section:
            return

        if node.tagname == "paragraph" and node.rawsource.startswith("COPY-FROM:"):
            # 检查 `COPY-FROM` 格式正确性
            if not self.COPY_FROM_REGEX.fullmatch(node.rawsource):
                lineno = node.line
                print(
                    f"{self.source_path}:{lineno}: Invalid `COPY-FROM` format. Please use `COPY-FROM: <full_API_path>`."
                )
                self._check_result = False

            # TODO: 检查 `COPY-FROM` 的路径是否可导入（要注意类方法路径）

    @property
    def in_code_example_section(self) -> bool:
        return self.CODE_EXAMPLE_SECTION_NAME in self._section_name_stack

    @property
    def result(self) -> bool:
        return self._check_result
