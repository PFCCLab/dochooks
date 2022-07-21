from __future__ import annotations

import docutils
import docutils.nodes
import docutils.parsers.rst


class Checker(docutils.nodes.NodeVisitor):
    """

    class TitleChecker(Checker):
        ...

    ast = parse_rst(text, file_path=file_path)
    result = TitleChecker.check(ast)
    """

    def unknown_visit(self, node: docutils.nodes.Element) -> None:
        """Ensure not raise exception when visiting unknown node."""
        pass

    def unknown_departure(self, node: docutils.nodes.Element) -> None:
        """Ensure not raise exception when leaving unknown node."""
        pass

    @property
    def source_path(self) -> str:
        return self.document.get("source")

    @property
    def result(self) -> bool:
        raise NotImplementedError()

    @classmethod
    def check(cls, node: docutils.nodes.document) -> bool:
        self = cls(node)
        node.walkabout(self)
        check_result = self.result
        return check_result


def create_chained_checker(checkers: list[type[Checker]], abort_on_failure: bool = False) -> type[Checker]:
    """
    建立一个实验性的 Chainer，将各个顺序执行的 checker 合并到一起
    这样 log 就会按照解析顺序打印，而不是按照 checker 顺序打印，阅读体验更友好些

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

        def __init__(self, node: docutils.nodes.document) -> None:
            super().__init__(node)
            self.checker_instances = [checker(node) for checker in self.checker_classes]

        def dispatch_visit(self, node: docutils.nodes.Element) -> None:
            for checker in self.checker_instances:
                checker.dispatch_visit(node)

        def dispatch_departure(self, node: docutils.nodes.Element) -> None:
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


def assert_is_element(node: docutils.nodes.Node) -> docutils.nodes.Element:
    """Assert node is a docutils.nodes.Element.

    由于 Element.children 的类型继承了 Node 下该属性的 list[docutils.nodes.Node]，
    子元素明明是 Element 却会报类型错误，这只是一个临时解决方案

    不使用 TypeGuard（PEP 647）是因为这是一件确定的事情，不需要进行判断

    另外不使用`assert isinstance(node, docutils.nodes.Element)` 也是同样的，我们
    不需要额外引入运行时开销
    """
    return node  # type: ignore
