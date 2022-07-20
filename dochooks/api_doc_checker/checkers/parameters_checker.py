from __future__ import annotations

import re
from typing import Optional

import docutils.nodes

from ..._compat import Literal, TypedDict
from ..utils import PATTERN_IDENTIFIER, is_valid_identifier
from .checker import Checker, assert_is_element

APIType = Literal["class", "function", ""]


class APIParameter(TypedDict):
    name: str
    type: Optional[str]
    is_rest: bool
    is_keyword: bool
    optional: bool
    default: Optional[str]


class ParametersChecker(Checker):
    PARAMETERS_SECTION_NAME = "参数"
    PATTERN_API_NAME = rf"{PATTERN_IDENTIFIER}(\.{PATTERN_IDENTIFIER})*"
    PATTERN_API_PARAMETER = rf"\*{{0,2}}{PATTERN_IDENTIFIER}\s*(:\s*{PATTERN_IDENTIFIER})?\s*(=\s*.+)?"
    # TODO: 支持 Python3.8 的仅位置参数和关键字参数符号（`/` 和 `*`）
    PATTERN_API_DECLARATION = rf"{PATTERN_API_NAME}\(\s*({PATTERN_API_PARAMETER})?(,\s*{PATTERN_API_PARAMETER})*\s*\)"
    REGEX_API_DECLARATION = re.compile(PATTERN_API_DECLARATION)

    PATTERN_DOC_PARAMETER_TYPE = rf"\((?P<type>{PATTERN_IDENTIFIER})(，(?P<optional_text>可选))?\)"
    REGEX_DOC_PARAMETER_TYPE = re.compile(PATTERN_DOC_PARAMETER_TYPE)

    _check_result = True
    _section_name_stack: list[str] = []
    _api_type: Optional[APIType] = None
    _api_name: Optional[str] = None
    _api_parameters: list[APIParameter]

    # TODO: 直接抽取函数声明来检查

    def visit_literal_block(self, node: docutils.nodes.Element):
        """首先获取 API 的声明
        也即 .. py:function:: API_NAME(...) 或者 .. py:class:: API_NAME(...)
        """
        if node.get("is_directive") is not True:
            return

        if node.get("directive_name") in ["py:function", "py:class"]:
            if self._api_type is not None:
                # TODO: 考虑下是否要这么严格
                print(f"{self.source_path}:{node.line}: Found multiple API declarations.")
                self._check_result = False
                return

            if node.get("directive_name") == "py:function":
                self._api_type = "function"
            else:
                self._api_type = "class"
            api_declaration = node.get("content")[0]

            if not self.REGEX_API_DECLARATION.fullmatch(api_declaration):
                print(f"{self.source_path}:{api_declaration}: Invalid API declaration. Got {api_declaration}.")
                self._check_result = False
                return

            api_name, api_parameters = parse_api_name_and_parameters(api_declaration)

            # TODO: 检查 API 是否可以 import

            self._api_name = api_name
            self._api_parameters = api_parameters

    def visit_section(self, node: docutils.nodes.Element):
        node_names = node.get("names")
        if node_names:
            self._section_name_stack.append(node_names[0])
        else:
            self._section_name_stack.append(" <Unknown section title> ")

    def depart_section(self, node: docutils.nodes.Element):
        self._section_name_stack.pop()

    def _extract_parameter_info_from_list_item(self, node: docutils.nodes.Element) -> Optional[APIParameter]:
        """对单行信息进行提取并检查"""

        doc_parameter: APIParameter = APIParameter(
            name="",
            type=None,
            is_rest=False,
            is_keyword=False,
            optional=False,
            default=None,
        )
        node.children
        paragraph = assert_is_element(node.children[0])

        # 确保包含 paragraph
        if paragraph.tagname != "paragraph" or not paragraph.children:
            print(f"{self.source_path}:{node.line}: Expected a paragraph, but got {paragraph.tagname}.")
            self._check_result = False
            return None

        # 确保参数的名称是加粗的（strong tag）
        if assert_is_element(paragraph.children[0]).tagname != "strong":
            print(
                f"{self.source_path}:{node.line}: Expected a strong, but got {assert_is_element(paragraph.children[0]).tagname}."
            )
            self._check_result = False
            return None

        parameter_name: str = paragraph.children[0].astext()
        if parameter_name.startswith("**"):
            doc_parameter["is_keyword"] = True
            parameter_name = parameter_name[2:]

        if parameter_name.startswith("*"):
            doc_parameter["is_rest"] = True
            parameter_name = parameter_name[1:]

        # 确保参数的名称是合法的标识符
        if not is_valid_identifier(parameter_name):
            print(f"{self.source_path}:{node.line}: Parameter name must be a valid identifier. Got {parameter_name}.")
            self._check_result = False
            return None
        doc_parameter["name"] = parameter_name

        # 确保参数名后有内容
        if len(paragraph.children) < 2:
            print(f"{self.source_path}:{node.line}: Expected a content after parameter name.")
            self._check_result = False
            return None

        # 确保参数名后类型信息格式正确
        # TODO: 关于 **kwargs 这种是否必须写类型和可选还需商榷，制定规范后继续修改
        parameter_type_with_part_of_desc: str = paragraph.children[1].astext().lstrip()
        if not self.REGEX_DOC_PARAMETER_TYPE.match(parameter_type_with_part_of_desc):
            print(
                f"{self.source_path}:{node.line}: Expected a valid parameter type. Got {parameter_type_with_part_of_desc}."
            )
            self._check_result = False
            return None

        mth = self.REGEX_DOC_PARAMETER_TYPE.match(parameter_type_with_part_of_desc)
        assert mth is not None
        parameter_type = mth.group("type")
        doc_parameter["type"] = parameter_type
        if mth.group("optional_text"):
            doc_parameter["optional"] = True

        # paragraph.children[1:]
        # TODO: 检查类型是否合法
        # TODO: 提取默认值，并检查书写方式是否正确，比如 int、float 应当为 :math:`3.14`
        # TODO: 检查行末是否有 trailing spaces
        # TODO: 检查第一行行末是否有句号（多行的情况是下面还有列表的情况）

        return doc_parameter

    def visit_bullet_list(self, node: docutils.nodes.Element):
        """
        检查参数列表，通过 _extract_parameter_info_from_list_item 得到的单行结果，结合声明进行全局检查
        """
        if not self.in_parameters_section:
            return

        doc_parameters = [
            self._extract_parameter_info_from_list_item(assert_is_element(list_item)) for list_item in node.children
        ]
        # 检查参数个数是否一致
        if len(self._api_parameters) != len(doc_parameters):
            print(
                f"{self.source_path}:{node.line}: Expected {len(self._api_parameters)} parameters, but got {len(doc_parameters)}."
            )
            self._check_result = False
            return

        # 检查参数属性是否对齐
        for i, (doc_parameter, api_parameter) in enumerate(zip(doc_parameters, self._api_parameters), 1):
            if doc_parameter is None:
                continue

            if doc_parameter["name"] != api_parameter["name"]:
                print(
                    f"{self.source_path}:{node.line}: Expected parameter {i} name {api_parameter['name']}, but got {doc_parameter['name']}."
                )
                self._check_result = False
                return

            if doc_parameter["optional"] != api_parameter["optional"]:
                print(
                    f"{self.source_path}:{node.line}: Expected parameter {i} ({api_parameter['name']}) optional {api_parameter['optional']}, but got {doc_parameter['optional']}."
                )
                self._check_result = False
                return

    @property
    def in_parameters_section(self) -> bool:
        return self.PARAMETERS_SECTION_NAME in self._section_name_stack

    @property
    def result(self) -> bool:
        return self._check_result


def parse_api_name_and_parameters(api_declaration: str) -> tuple[Optional[str], list[APIParameter]]:
    """解析 API 声明的名称和参数"""

    api_name: Optional[str] = None
    api_parameters: list[APIParameter] = []

    api_declaration = api_declaration.strip()

    api_name, api_parameters_str = api_declaration.split("(")

    api_parameters_str = api_parameters_str.rstrip(")")

    for api_parameter_str in api_parameters_str.split(","):
        if not api_parameter_str:
            continue

        api_parameter: APIParameter = APIParameter(
            name="",
            type=None,
            is_rest=False,
            is_keyword=False,
            optional=False,
            default=None,
        )
        api_parameter_str = api_parameter_str.strip()
        if "=" in api_parameter_str:
            api_parameter_str, api_parameter_default = api_parameter_str.split("=")
            api_parameter_str = api_parameter_str.strip()
            api_parameter_default = api_parameter_default.strip()
            api_parameter["default"] = api_parameter_default
            api_parameter["optional"] = True

        if ":" in api_parameter_str:
            api_parameter_str, api_parameter_type = api_parameter_str.split(":")
            api_parameter_str = api_parameter_str.strip()
            api_parameter_type = api_parameter_type.strip()
            api_parameter["type"] = api_parameter_type

        if api_parameter_str.startswith("**"):
            api_parameter["is_keyword"] = True
            api_parameter["optional"] = True
            api_parameter_str = api_parameter_str[2:]

        if api_parameter_str.startswith("*"):
            api_parameter["is_rest"] = True
            api_parameter["optional"] = True
            api_parameter_str = api_parameter_str[1:]

        api_parameter_name = api_parameter_str
        api_parameter["name"] = api_parameter_name
        api_parameters.append(api_parameter)

    return api_name, api_parameters
