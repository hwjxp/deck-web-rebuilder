#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from _deck_checks_common import PAGE_SCHEMA, PAGE_SPECS_JSON, load_workspace_json, maybe_validate_with_jsonschema


def run_check(workspace: Path) -> list[str]:
    issues: list[str] = []
    try:
        data = load_workspace_json(workspace, PAGE_SPECS_JSON)
    except FileNotFoundError:
        return [f"missing {PAGE_SPECS_JSON}"]
    except Exception as exc:  # pragma: no cover - defensive path
        return [f"could not read {PAGE_SPECS_JSON}: {exc}"]

    issues.extend(maybe_validate_with_jsonschema(data, PAGE_SCHEMA))

    slides = data.get("slides", [])
    if len(slides) < 3:
        issues.append("page-specs.json should describe at least 3 slides before implementation starts")

    seen_ids: set[str] = set()
    seen_source_numbers: set[int] = set()
    for slide in slides:
        slide_id = slide.get("slide_id")
        if slide_id in seen_ids:
            issues.append(f"{slide_id}: duplicate slide_id")
        seen_ids.add(slide_id)

        source_no = slide.get("source_slide_number")
        if source_no in seen_source_numbers:
            issues.append(f"{slide_id}: duplicate source_slide_number {source_no}")
        seen_source_numbers.add(source_no)

        if slide.get("role") not in {"cover", "section-divider"} and not slide.get("body_blocks"):
            issues.append(f"{slide_id}: non-divider slides should not have empty body_blocks")

        title = slide.get("title", {})
        if not title.get("fallback_strategy"):
            issues.append(f"{slide_id}: missing title fallback strategy")

        if not slide.get("forbidden_patterns"):
            issues.append(f"{slide_id}: forbidden_patterns should be declared explicitly")

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <workspace-dir>")
        return 1

    workspace = Path(sys.argv[1]).expanduser().resolve()
    issues = run_check(workspace)
    if issues:
        print("[FAIL] Page spec checks failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("[OK] Page specs passed schema and structural checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
