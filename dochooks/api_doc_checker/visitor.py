from __future__ import annotations

import docutils
import docutils.nodes
import docutils.parsers.rst


class APIDocChecker(docutils.nodes.NodeVisitor):
    def visit_reference(self, node: docutils.nodes.reference) -> None:
        """Called for "reference" nodes."""
        print(node)

    def unknown_visit(self, node: docutils.nodes.Node) -> None:
        """Called for all other node types."""
        pass
