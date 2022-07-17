from __future__ import annotations

from typing import Any

import docutils
import docutils.nodes
import docutils.parsers.rst

Node = Any  # docutils.nodes.Node, avoid type error


class Checker(docutils.nodes.NodeVisitor):
    """

    class TitleChecker(Checker):
        ...

    ast = parse_rst(text, file_path=file_path)
    result = TitleChecker.check(ast)
    """

    def unknown_visit(self, node: Node) -> None:
        """Ensure not raise exception when visiting unknown node."""
        pass

    def unknown_departure(self, node: Node) -> None:
        """Ensure not raise exception when leaving unknown node."""
        pass

    @property
    def source_path(self) -> str:
        return self.document.get("source")

    @property
    def result(self) -> bool:
        raise NotImplementedError()

    @classmethod
    def check(cls, node: Node) -> bool:
        self = cls(node)
        node.walkabout(self)
        check_result = self.result
        return check_result


def create_chained_checker(checkers: list[type[Checker]], abort_on_failure: bool = False) -> type[Checker]:
    """
    class TitleChecker(Checker):
        ...

    class ParameterChecker(Checker):
        ...

    ast = parse_rst(text, file_path=file_path)
    result = create_chained_checker([TitleChecker, ParameterChecker], True).check(ast)
    """

    class _ChainedChecker(Checker):
        """Experimental"""

        checker_classes: list[type[Checker]] = []
        checker_instances: list[Checker]

        def __init__(self, node: Node) -> None:
            super().__init__(node)
            self.checker_instances = [checker(node) for checker in self.checker_classes]

        def dispatch_visit(self, node: Node) -> None:
            for checker in self.checker_instances:
                checker.dispatch_visit(node)

        def dispatch_departure(self, node: Node) -> None:
            for checker in self.checker_instances:
                checker.dispatch_departure(node)

        @classmethod
        def add_checker(cls, checker: type[Checker]) -> None:
            cls.checker_classes.append(checker)

        @property
        def result(self) -> bool:
            result = True
            for checker in self.checker_instances:
                checker_result = checker.result
                if abort_on_failure and not checker_result:
                    # 只要有一个检查失败，则立即返回
                    return False
                else:
                    result = checker_result and result
            return result

    chain = _ChainedChecker
    for checker in checkers:
        chain.add_checker(checker)
    return chain
