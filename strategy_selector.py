from __future__ import annotations


class StrategySelector:
    """Waehlt Strategien basierend auf Kategorie, Task-Typ und Planungstiefe aus."""

    def select_strategies(self, category_id: str, field_values: dict) -> dict:
        if category_id not in {"sourcecode_planning_style", "sourcecode_planning_style_light"}:
            return {
                "depth_mode": "light",
                "token_budget_mode": "minimal",
                "strategy_sequence": [],
            }

        depth_mode = self._resolve_depth_mode(category_id, field_values)
        token_budget_mode = self._resolve_token_budget_mode(depth_mode)

        strategy_sequence = [
            "planning/discovery",
            "planning/alignment",
            "planning/design",
            "planning/refinement",
            "decomposition/task_breakdown",
            "reflection/self_review",
            "verification/consistency",
        ]

        if depth_mode == "light":
            # Kompaktmodus: weniger kognitive Last
            strategy_sequence = [
                "planning/discovery",
                "planning/design",
                "decomposition/task_breakdown",
                "verification/consistency",
            ]
        elif depth_mode == "medium":
            strategy_sequence = [
                "planning/discovery",
                "planning/alignment",
                "planning/design",
                "decomposition/task_breakdown",
                "verification/consistency",
            ]

        return {
            "depth_mode": depth_mode,
            "token_budget_mode": token_budget_mode,
            "strategy_sequence": strategy_sequence,
        }

    def _resolve_depth_mode(self, category_id: str, field_values: dict) -> str:
        planning_depth = str(field_values.get("planning_depth", "")).strip().lower()
        if "leicht" in planning_depth or planning_depth == "light":
            return "light"
        if "tief" in planning_depth or planning_depth == "deep":
            return "deep"
        if "mittel" in planning_depth or planning_depth == "medium":
            return "medium"

        complexity = str(field_values.get("complexity", "")).strip().lower()
        if complexity in {"einfach", "simple"}:
            return "light"
        if complexity in {"komplex", "very complex", "sehr komplex", "complex"}:
            return "deep"

        if category_id == "sourcecode_planning_style_light":
            return "light"
        return "medium"

    def _resolve_token_budget_mode(self, depth_mode: str) -> str:
        if depth_mode == "light":
            return "minimal"
        if depth_mode == "deep":
            return "extended"
        return "balanced"
