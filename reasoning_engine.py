from __future__ import annotations

import os


class ReasoningEngine:
    """Laedt Strategievorlagen und injiziert sie in den Basis-Prompt."""

    def __init__(self, strategies_base_dir: str):
        self.strategies_base_dir = strategies_base_dir

    def inject_strategies(self, base_prompt: str, strategy_selection: dict, language_code: str = "de") -> str:
        language = self._normalize_language(language_code)
        strategy_keys = strategy_selection.get("strategy_sequence", [])
        if not strategy_keys:
            return base_prompt

        loaded_blocks = []
        seen = set()
        for strategy_key in strategy_keys:
            if strategy_key in seen:
                continue
            seen.add(strategy_key)

            strategy_text = self._load_strategy(strategy_key, language)
            if strategy_text:
                loaded_blocks.append(strategy_text.strip())

        if not loaded_blocks:
            return base_prompt

        depth_mode = strategy_selection.get("depth_mode", "medium")
        token_budget_mode = strategy_selection.get("token_budget_mode", "balanced")
        header_lines = self._get_header_lines(language, depth_mode, token_budget_mode)

        merged = "\n\n".join(["\n".join(header_lines), *loaded_blocks, base_prompt])
        return self._remove_duplicate_lines(merged)

    def _load_strategy(self, strategy_key: str, language: str) -> str:
        relative_base = strategy_key.replace("/", os.sep)
        candidates = [
            os.path.join(self.strategies_base_dir, f"{relative_base}.{language}.md"),
            os.path.join(self.strategies_base_dir, f"{relative_base}.de.md"),
            os.path.join(self.strategies_base_dir, f"{relative_base}.md"),
        ]

        for strategy_path in candidates:
            if not os.path.exists(strategy_path):
                continue
            try:
                with open(strategy_path, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except OSError:
                continue
        return ""

    def _normalize_language(self, language_code: str) -> str:
        code = str(language_code or "de").strip().lower()
        if code.startswith("en"):
            return "en"
        if code.startswith("fr"):
            return "fr"
        if code.startswith("es"):
            return "es"
        return "de"

    def _get_header_lines(self, language: str, depth_mode: str, token_budget_mode: str) -> list[str]:
        header_texts = {
            "de": {
                "title": "STRATEGIE-INJEKTION",
                "depth": "Planungstiefe",
                "token": "Token-Budget-Modus",
            },
            "en": {
                "title": "STRATEGY INJECTION",
                "depth": "Depth mode",
                "token": "Token budget mode",
            },
            "fr": {
                "title": "INJECTION DE STRATEGIE",
                "depth": "Mode de profondeur",
                "token": "Mode de budget tokens",
            },
            "es": {
                "title": "INYECCION DE ESTRATEGIA",
                "depth": "Modo de profundidad",
                "token": "Modo de presupuesto de tokens",
            },
        }

        depth_labels = {
            "de": {"light": "leicht", "medium": "mittel", "deep": "tief"},
            "en": {"light": "light", "medium": "medium", "deep": "deep"},
            "fr": {"light": "leger", "medium": "moyen", "deep": "profond"},
            "es": {"light": "ligero", "medium": "medio", "deep": "profundo"},
        }

        token_labels = {
            "de": {"minimal": "minimal", "balanced": "ausgewogen", "extended": "erweitert"},
            "en": {"minimal": "minimal", "balanced": "balanced", "extended": "extended"},
            "fr": {"minimal": "minimal", "balanced": "equilibre", "extended": "etendu"},
            "es": {"minimal": "minimal", "balanced": "equilibrado", "extended": "ampliado"},
        }

        texts = header_texts.get(language, header_texts["de"])
        depth_value = depth_labels.get(language, depth_labels["de"]).get(depth_mode, depth_mode)
        token_value = token_labels.get(language, token_labels["de"]).get(token_budget_mode, token_budget_mode)

        return [
            texts["title"],
            f"{texts['depth']}: {depth_value}",
            f"{texts['token']}: {token_value}",
            "",
        ]

    def _remove_duplicate_lines(self, text: str) -> str:
        output = []
        seen = set()
        for line in text.splitlines():
            normalized = line.strip()
            if normalized and normalized in seen:
                continue
            if normalized:
                seen.add(normalized)
            output.append(line)
        return "\n".join(output).strip()
