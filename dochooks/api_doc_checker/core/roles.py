"""Handlers for additional ReST roles.

refs:

- [rstcheck-core ignore roles and directives](https://github.com/rstcheck/rstcheck-core/blob/53537bcfbce43977030635148db4ce19c3d0aacf/src/rstcheck_core/_docutils.py)
- [Sphinx roles doc](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html)
- [Docutils create roles doc](https://docutils.sourceforge.io/docs/howto/rst-roles.html)
- [Sphinx roles code at GitHub](https://github.com/sphinx-doc/sphinx/blob/93b703131b35da76c87eb72e2d338f55ec2b68a8/sphinx/roles.py)
- [The Docutils Document Tree](https://docutils.sourceforge.io/docs/ref/doctree.html)
"""


from __future__ import annotations

from typing import Any, Callable, Optional

import docutils
import docutils.nodes
import docutils.parsers.rst
import docutils.parsers.rst.states
from docutils.parsers.rst import roles

# Copy the code below into your browser to quickly get results
# [...document.querySelectorAll('dl.rst.role span.sig-name.descname > span')].map((node) => node.innerText.match(/^:(?<roleName>\S+):$/)?.groups.roleName).filter(name => name)

# https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html
SPHINX_BASE_ROLES = [
    "any",
    "ref",
    "doc",
    "download",
    "numref",
    "envvar",
    "token",
    "keyword",
    "option",
    "term",
    "code",
    "math",
    "eq",
    "abbr",
    "command",
    "dfn",
    "file",
    "guilabel",
    "kbd",
    "mailheader",
    "makevar",
    "manpage",
    "menuselection",
    "mimetype",
    "newsgroup",
    "program",
    "regexp",
    "samp",
    "pep",
    "rfc",
]

# https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
_SPHINX_BASE_ROLES_FROM_DIRECTIVE_PAGE = ["index"]

SPHINX_BASE_ROLES.extend(_SPHINX_BASE_ROLES_FROM_DIRECTIVE_PAGE)

# https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html
SPHINX_DOMAIN_ROLES = [
    "py:mod",
    "py:func",
    "py:data",
    "py:const",
    "py:class",
    "py:meth",
    "py:attr",
    "py:exc",
    "py:obj",
    "c:member",
    "c:data",
    "c:var",
    "c:func",
    "c:macro",
    "c:struct",
    "c:union",
    "c:enum",
    "c:enumerator",
    "c:type",
    "c:expr",
    "c:texpr",
    "cpp:expr",
    "cpp:texpr",
    "cpp:any",
    "cpp:class",
    "cpp:struct",
    "cpp:func",
    "cpp:member",
    "cpp:var",
    "cpp:type",
    "cpp:concept",
    "cpp:enum",
    "cpp:enumerator",
    "js:mod",
    "js:func",
    "js:meth",
    "js:class",
    "js:data",
    "js:attr",
    "foo",
    "rst:dir",
    "rst:role",
    "math:numref",
]

# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
SPHINX_EXT_AUTODOC_ROLES: list[str] = []

RoleFn = Callable[
    [
        str,
        str,
        str,
        int,
        docutils.parsers.rst.states.Inliner,
        Optional[dict[str, Any]],
        Optional[list[str]],
    ],
    tuple[list[Any], list[Any]],
]


def _ignore_role(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: docutils.parsers.rst.states.Inliner,
    options: Optional[dict[str, Any]] = None,
    content: Optional[list[str]] = None,
) -> tuple[list[Any], list[Any]]:
    """Stub for unknown roles."""
    print("name:", name)
    print("rawtext:", rawtext)
    print("text:", text)
    return ([], [])


def create_custom_role(
    role_name: str,
) -> RoleFn:
    """
    :role_name:`role_text`

    ->

    <literal classes="role_name" is_role="True" role_name="role_name">role_text</literal>
    """

    def _custom_role(
        name: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: docutils.parsers.rst.states.Inliner,
        options: Optional[dict[str, Any]] = None,
        content: Optional[list[str]] = None,
    ) -> tuple[list[Any], list[Any]]:
        node = docutils.nodes.literal(
            rawsource=rawtext,
            text=text,
            classes=role_name,
            is_role=True,
            role_name=role_name,
        )
        return [node], []

    return _custom_role


def create_ignore_role() -> RoleFn:
    return _ignore_role


def preset_sphinx_roles():
    # https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html
    sphinx_roles = SPHINX_BASE_ROLES + SPHINX_DOMAIN_ROLES + SPHINX_EXT_AUTODOC_ROLES

    docutils_registered_roles = [role_name for role_name in roles._role_registry]
    need_register_roles = [role_name for role_name in sphinx_roles if role_name not in docutils_registered_roles]
    for role_name in need_register_roles:
        roles.register_local_role(role_name, create_custom_role(role_name))
