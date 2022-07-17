"""Handlers for additional ReST directives.

refs:

- [rstcheck-core ignore roles and directives](https://github.com/rstcheck/rstcheck-core/blob/53537bcfbce43977030635148db4ce19c3d0aacf/src/rstcheck_core/_docutils.py)
- [Sphinx directives doc](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html)
- [Docutils create directives doc](https://docutils.sourceforge.io/docs/howto/rst-directives.html)
- [Sphinx directives code at GitHub](https://github.com/sphinx-doc/sphinx/blob/e7fc03bce2c2577a9c5331ce5b2fa43a66ce7773/sphinx/directives/__init__.py)
- [The Docutils Document Tree](https://docutils.sourceforge.io/docs/ref/doctree.html)
"""

from __future__ import annotations

import docutils
import docutils.nodes
import docutils.parsers.rst
from docutils.parsers.rst import directives, roles

# Copy the code below into your browser to quickly get results
# [...document.querySelectorAll('dl.rst.directive span.sig-name.descname :nth-child(2)')].map((node) => node.innerText.match(/^(?<directiveName>\S+)::$/).groups?.directiveName).filter(name => name)

# https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
SPHINX_BASE_DIRECTIVES = [
    "toctree",
    "note",
    "warning",
    "versionadded",
    "versionchanged",
    "deprecated",
    "seealso",
    "rubric",
    "centered",
    "hlist",
    "highlight",
    "code-block",
    "literalinclude",
    "glossary",
    "sectionauthor",
    "codeauthor",
    "index",
    "only",
    "tabularcolumns",
    "math",
    "productionlist",
]

# https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html
SPHINX_DOMAIN_DIRECTIVES = [
    "default-domain",
    "py:module",
    "py:currentmodule",
    "py:function",
    "py:data",
    "py:exception",
    "py:class",
    "py:class",
    "py:attribute",
    "py:property",
    "py:method",
    "py:staticmethod",
    "py:classmethod",
    "py:decorator",
    "py:decorator",
    "py:decoratormethod",
    "py:decoratormethod",
    "c:member",
    "c:var",
    "c:function",
    "c:macro",
    "c:macro",
    "c:struct",
    "c:union",
    "c:enum",
    "c:enumerator",
    "c:type",
    "c:type",
    "c:alias",
    "c:namespace",
    "c:namespace-push",
    "c:namespace-pop",
    "cpp:class",
    "cpp:struct",
    "cpp:function",
    "cpp:member",
    "cpp:var",
    "cpp:type",
    "cpp:type",
    "cpp:type",
    "cpp:enum",
    "cpp:enum-struct",
    "cpp:enum-class",
    "cpp:enumerator",
    "cpp:enumerator",
    "cpp:union",
    "cpp:concept",
    "cpp:alias",
    "cpp:namespace",
    "cpp:namespace-push",
    "cpp:namespace-pop",
    "option",
    "envvar",
    "program",
    "describe",
    "object",
    "js:module",
    "js:function",
    "js:method",
    "js:class",
    "js:data",
    "js:attribute",
    "rst:directive",
    "foo",
    "bar",
    "rst:directive:option",
    "toctree",
    "rst:role",
]

# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
SPHINX_EXT_AUTODOC_DIRECTIVES = [
    "automodule",
    "autoclass",
    "autoexception",
    "autofunction",
    "autodecorator",
    "autodata",
    "automethod",
    "autoattribute",
    "autoproperty",
]


class _IgnoredDirective(docutils.parsers.rst.Directive):
    """Stub for unknown directives."""

    has_content = True

    def run(self) -> list[docutils.nodes.Node]:
        """Do nothing."""
        return []


def create_custom_directive(directive_name: str) -> type[docutils.parsers.rst.Directive]:
    """
    .. directive_name:: directive_text_line1
        directive_text_line2
        directive_text_line3

    ->

    <literal_block
        classes="py:function"
        content="['directive_text_line1', 'directive_text_line2', 'directive_text_line3']"
        directive_name="py:function"
        is_directive="True"
        xml:space="preserve">
        directive_text_line1
        directive_text_line2
        directive_text_line3
    </literal_block>
    """

    class _CustomDirective(docutils.parsers.rst.Directive):

        has_content = True

        def run(self):
            node = docutils.nodes.literal_block(
                rawsource=self.block_text,
                text="\n".join(list(self.content)),
                classes=directive_name,
                content=self.content,
                is_directive=True,
                directive_name=directive_name,
            )
            return [node]

    return _CustomDirective


def create_ignore_directive() -> type[docutils.parsers.rst.Directive]:
    return _IgnoredDirective


def preset_sphinx_directives():
    sphinx_roles = SPHINX_BASE_DIRECTIVES + SPHINX_DOMAIN_DIRECTIVES + SPHINX_EXT_AUTODOC_DIRECTIVES

    docutils_registered_directives = [role_name for role_name in roles._role_registry]
    need_register_directives = [
        directive_name for directive_name in sphinx_roles if directive_name not in docutils_registered_directives
    ]
    for directive_name in need_register_directives:
        directives.register_directive(directive_name, create_custom_directive(directive_name))
