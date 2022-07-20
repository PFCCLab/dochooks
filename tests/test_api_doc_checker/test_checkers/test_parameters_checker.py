from __future__ import annotations

import re
from typing import Optional

import pytest

from dochooks.api_doc_checker.checkers import ParametersChecker
from dochooks.api_doc_checker.checkers.parameters_checker import (
    APIParameter,
    parse_api_name_and_parameters,
)


def test_pattern_api_name():
    regex_api_name = re.compile(ParametersChecker.PATTERN_API_NAME)
    assert regex_api_name.fullmatch("a.b.c")
    assert regex_api_name.fullmatch("mod")
    assert regex_api_name.fullmatch("mod.submod")
    assert regex_api_name.fullmatch("mod.submod.func")


def test_pattern_api_parameter():
    regex_api_parameter = re.compile(ParametersChecker.PATTERN_API_PARAMETER)
    assert regex_api_parameter.fullmatch("param")
    assert regex_api_parameter.fullmatch("param  :  type")
    assert regex_api_parameter.fullmatch("param:type")
    assert regex_api_parameter.fullmatch("param  =  'default_value'")
    assert regex_api_parameter.fullmatch("param='default_value'")
    assert regex_api_parameter.fullmatch("param  :  type  =  'default_value'")
    assert regex_api_parameter.fullmatch("param:type='default_value'")
    assert regex_api_parameter.fullmatch("a: int = 1")
    assert regex_api_parameter.fullmatch("*args")
    assert regex_api_parameter.fullmatch("**kwargs")
    assert not regex_api_parameter.fullmatch("***args")


def test_pattern_api_parameter_args_or_kwrgs():
    regex_api_declatation = re.compile(ParametersChecker.PATTERN_API_DECLARATION)
    assert regex_api_declatation.fullmatch("func()")
    assert regex_api_declatation.fullmatch("mod.submod.func(arg1, arg2, arg3)")
    assert regex_api_declatation.fullmatch("mod.submod.func(arg1: str, arg2: int, arg3: bool=False)")
    assert regex_api_declatation.fullmatch("func(arg1: int, arg2: bool=False, *args, **kwargs)")


def test_pattern_doc_parameter_type():
    regex_doc_parameter_type = re.compile(ParametersChecker.PATTERN_DOC_PARAMETER_TYPE)
    assert regex_doc_parameter_type.fullmatch("(int)")
    assert regex_doc_parameter_type.fullmatch("(bool，可选)")


@pytest.mark.parametrize(
    "api_declaration, api_name, api_parameters",
    [
        ("func()", "func", []),
        (
            "mod.func(arg1, arg2)",
            "mod.func",
            [
                APIParameter(
                    name="arg1",
                    type=None,
                    is_rest=False,
                    is_keyword=False,
                    optional=False,
                    default=None,
                ),
                APIParameter(
                    name="arg2",
                    type=None,
                    is_rest=False,
                    is_keyword=False,
                    optional=False,
                    default=None,
                ),
            ],
        ),
        (
            " mod.func(name: str = '111', *args, **kwargs) ",
            "mod.func",
            [
                APIParameter(
                    name="name",
                    type="str",
                    is_rest=False,
                    is_keyword=False,
                    optional=True,
                    default="'111'",
                ),
                APIParameter(
                    name="args",
                    type=None,
                    is_rest=True,
                    is_keyword=False,
                    optional=True,
                    default=None,
                ),
                APIParameter(
                    name="kwargs",
                    type=None,
                    is_rest=False,
                    is_keyword=True,
                    optional=True,
                    default=None,
                ),
            ],
        ),
    ],
)
def test_parse_api_name_and_parameters(
    api_declaration: str, api_name: Optional[str], api_parameters: list[APIParameter]
):
    api_name_actual, api_parameters_actual = parse_api_name_and_parameters(api_declaration)
    assert api_name == api_name_actual
    assert api_parameters == api_parameters_actual
