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

    input_mode = data.get("input_mode")
    if input_mode not in {"polish", "reverse-engineer", "editorial-compose"}:
        issues.append("page-specs.json should declare a valid top-level input_mode")

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
        posture = title.get("posture")
        prefer_no_wrap = title.get("prefer_no_wrap")
        max_lines = title.get("max_lines")
        min_container_ratio = title.get("min_container_ratio", 0)

        if posture == "single-line" and max_lines != 1:
            issues.append(f"{slide_id}: single-line title posture should use `max_lines: 1`")
        if posture == "single-line" and not prefer_no_wrap:
            issues.append(f"{slide_id}: single-line title posture should set `prefer_no_wrap: true`")
        if posture == "balanced-two-line" and prefer_no_wrap:
            issues.append(f"{slide_id}: balanced-two-line titles should not force `prefer_no_wrap: true`")
        if prefer_no_wrap and min_container_ratio < 0.6:
            issues.append(f"{slide_id}: no-wrap titles should keep at least 60% title container width")

        if not slide.get("forbidden_patterns"):
            issues.append(f"{slide_id}: forbidden_patterns should be declared explicitly")

        source_of_truth = set(slide.get("source_of_truth", []))
        if input_mode != "editorial-compose" and "visual-render" not in source_of_truth:
            issues.append(f"{slide_id}: non-editorial slides should include `visual-render` in source_of_truth")
        if slide.get("confidence_level") == "low" and slide.get("primary_proof_device") not in {"none", "hero-image"}:
            issues.append(f"{slide_id}: low-confidence proof slides should be investigated before free redraw")

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
