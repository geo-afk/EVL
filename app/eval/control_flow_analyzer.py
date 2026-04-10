from __future__ import annotations

from typing import Any, Callable

from generated.EVALParser import EVALParser


class ControlFlowAnalyzer:
    @staticmethod
    def collect_condition_vars(tree: Any) -> set[str]:
        names: set[str] = set()
        if isinstance(tree, EVALParser.IdentExprContext):
            names.add(tree.IDENTIFIER().getText())
        for index in range(tree.getChildCount()):
            names |= ControlFlowAnalyzer.collect_condition_vars(tree.getChild(index))
        return names

    @staticmethod
    def assigned_vars_in_block(tree: Any) -> set[str]:
        names: set[str] = set()
        if isinstance(tree, EVALParser.AssignmentContext):
            names.add(tree.IDENTIFIER().getText())
        for index in range(tree.getChildCount()):
            names |= ControlFlowAnalyzer.assigned_vars_in_block(tree.getChild(index))
        return names

    @staticmethod
    def has_break(tree: Any) -> bool:
        if isinstance(tree, EVALParser.BreakStatementContext):
            return True
        for index in range(tree.getChildCount()):
            if ControlFlowAnalyzer.has_break(tree.getChild(index)):
                return True
        return False

    @staticmethod
    def collect_break_guards(
        block: Any,
        visit: Callable[[Any], Any],
        unwrap: Callable[[Any], Any],
    ) -> list[bool | None]:
        guards: list[bool | None] = []
        ControlFlowAnalyzer._walk_for_breaks(
            block,
            guard=True,
            guards=guards,
            visit=visit,
            unwrap=unwrap,
        )
        return guards

    @staticmethod
    def _walk_for_breaks(
        node: Any,
        guard: bool | None,
        guards: list[bool | None],
        visit: Callable[[Any], Any],
        unwrap: Callable[[Any], Any],
    ) -> None:
        if node is None:
            return

        if isinstance(node, EVALParser.BlockContext):
            for statement in node.statement():
                ControlFlowAnalyzer._walk_for_breaks(statement, guard, guards, visit, unwrap)
            return

        if isinstance(node, EVALParser.BreakStatementContext):
            guards.append(guard)
            return

        if isinstance(node, EVALParser.WhileStatementContext):
            return

        if isinstance(node, EVALParser.IfStatementContext):
            expressions = list(node.expression())
            blocks = list(node.block())
            has_else = len(blocks) > len(expressions)

            for index, condition in enumerate(expressions):
                try:
                    condition_value = unwrap(visit(condition))
                except Exception:
                    condition_value = None

                if guard is False or condition_value is False:
                    branch_guard = False
                elif guard is True and condition_value is True:
                    branch_guard = True
                else:
                    branch_guard = None

                if index < len(blocks):
                    ControlFlowAnalyzer._walk_for_breaks(
                        blocks[index],
                        branch_guard,
                        guards,
                        visit,
                        unwrap,
                    )

            if has_else:
                ControlFlowAnalyzer._walk_for_breaks(blocks[-1], guard, guards, visit, unwrap)
            return

        if isinstance(node, EVALParser.TryStatementContext):
            for block in list(node.block()):
                ControlFlowAnalyzer._walk_for_breaks(block, guard, guards, visit, unwrap)
            return

        if hasattr(node, "getChildCount") and node.getChildCount() == 1:
            child = node.getChild(0)
            if child is not node:
                ControlFlowAnalyzer._walk_for_breaks(child, guard, guards, visit, unwrap)
