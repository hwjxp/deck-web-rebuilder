#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from _deck_checks_common import DESIGN_SYSTEM_JSON, PAGE_SPECS_JSON, chinese_char_count, english_word_count, load_workspace_json


EXPECTED_FALLBACK_PREFIX = ["rewrite", "restack", "widen-title-region"]


def run_check(workspace: Path) -> list[str]:
    issues: list[str] = []
    try:
        page_specs = load_workspace_json(workspace, PAGE_SPECS_JSON)
        design_system = load_workspace_json(workspace, DESIGN_SYSTEM_JSON)
    except FileNotFoundError as exc:
        return [f"missing {exc.args[0]}"]

    bilingual_policy = design_system.get("bilingual_policy", {})
    title_wrap = design_system.get("typography", {}).get("title_wrapping", {})

    en_limit = bilingual_policy.get("title_word_limit_en", 22)
    zh_limit = bilingual_policy.get("title_char_limit_zh", 28)
    max_title_lines = title_wrap.get("max_title_lines", 2)
    min_title_ratio = title_wrap.get("min_title_container_ratio", 0.55)

    for slide in page_specs.get("slides", []):
        slide_id = slide.get("slide_id", "<unknown>")
        title = slide.get("title", {})
        text = title.get("text", {})
        en_words = english_word_count(text.get("en", ""))
        zh_chars = chinese_char_count(text.get("zh", ""))

        if en_words > en_limit:
            issues.append(f"{slide_id}: English title exceeds word budget ({en_words} > {en_limit})")
        if zh_chars > zh_limit:
            issues.append(f"{slide_id}: Chinese title exceeds character budget ({zh_chars} > {zh_limit})")

        if slide.get("bilingual_mode") == "side-by-side" and slide.get("density") != "low":
            issues.append(f"{slide_id}: side-by-side bilingual mode is only allowed on low-density slides")

        if title.get("max_lines", 0) > max_title_lines:
            issues.append(f"{slide_id}: title line budget exceeds the design-system max")

        if title.get("min_container_ratio", 1) < min_title_ratio:
            issues.append(f"{slide_id}: title width policy is narrower than the deck-wide minimum")

        fallback = title.get("fallback_strategy", [])
        if fallback[:3] != EXPECTED_FALLBACK_PREFIX:
            issues.append(
                f"{slide_id}: title fallback should begin with {' -> '.join(EXPECTED_FALLBACK_PREFIX)}"
            )

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <workspace-dir>")
        return 1

    workspace = Path(sys.argv[1]).expanduser().resolve()
    issues = run_check(workspace)
    if issues:
        print("[FAIL] Bilingual fit checks failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("[OK] Bilingual fit checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
