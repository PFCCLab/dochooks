from __future__ import annotations

import re

from ..utils import IDENTIFIER_PATTERN
from .checker import Checker, Node


class CodeExampleChecker(Checker):
    CODE_EXAMPLE_SECTION_NAME = "代码示例"
    COPY_FROM_REGEX = re.compile(rf"^COPY-FROM: {IDENTIFIER_PATTERN}(\.{IDENTIFIER_PATTERN})*(:[a-zA-Z0-9_\-]+)?$")

    _check_result = True

    def visit_section(self, node: Node):
        is_code_example_section: bool = False
        for child in node.children:
            if child.tagname == "title" and child.rawsource == self.CODE_EXAMPLE_SECTION_NAME:
                is_code_example_section = True
            if is_code_example_section:
                # TODO: 这样的形式不支持对于深层次的检测（非子节点，而是孙子甚至更深层的节点）
                #       因此仍然需要使用 visit 的方式来检查

                # 检查代码示例是否已经使用 `COPY-FROM` 替换
                if (
                    child.tagname == "literal_block"
                    and child.get("is_directive") is True
                    and child.get("directive_name") == "code-block"
                ):
                    lineno = child.line
                    print(
                        f"{self.source_path}:{lineno}: Found a code block in the code example section. Please use `COPY-FROM` instead."
                    )
                    self._check_result = False

                # 检查 `COPY-FROM` 格式正确性
                if child.tagname == "paragraph" and child.rawsource.startswith("COPY-FROM:"):
                    if not self.COPY_FROM_REGEX.match(child.rawsource):
                        lineno = child.line
                        print(
                            f"{self.source_path}:{lineno}: Invalid `COPY-FROM` format. Please use `COPY-FROM: <full_API_path>`."
                        )
                        self._check_result = False

                    # TODO: 检查 `COPY-FROM` 的路径是否可导入（要注意类方法路径）

    @property
    def result(self) -> bool:
        return self._check_result
