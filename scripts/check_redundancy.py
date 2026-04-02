#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from _deck_checks_common import PAGE_SPECS_JSON, load_workspace_json, normalize_text, text_blocks_for_slide


def run_check(workspace: Path) -> list[str]:
    issues: list[str] = []
    try:
        page_specs = load_workspace_json(workspace, PAGE_SPECS_JSON)
    except FileNotFoundError:
        return [f"missing {PAGE_SPECS_JSON}"]

    slides = page_specs.get("slides", [])
    agenda_count = sum(1 for slide in slides if slide.get("role") == "agenda")
    if agenda_count > 1:
        issues.append("more than one agenda slide is declared in page specs")

    for slide in slides:
        slide_id = slide.get("slide_id", "<unknown>")
        proof_blocks = [block for block in slide.get("body_blocks", []) if block.get("purpose") == "prove"]
        if slide.get("primary_proof_device") != "none" and len(proof_blocks) > 1:
            issues.append(f"{slide_id}: more than one proof-oriented body block risks a duplicated proof layer")

        seen: dict[str, str] = {}
        for label, text in text_blocks_for_slide(slide):
            normalized = normalize_text(text)
            if len(normalized) < 20:
                continue
            if normalized in seen:
                issues.append(f"{slide_id}: duplicated copy between {seen[normalized]} and {label}")
                break
            seen[normalized] = label

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <workspace-dir>")
        return 1

    workspace = Path(sys.argv[1]).expanduser().resolve()
    issues = run_check(workspace)
    if issues:
        print("[FAIL] Redundancy checks failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("[OK] Redundancy checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
