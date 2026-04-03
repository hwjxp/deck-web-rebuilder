#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

from _deck_checks_common import PAGE_SPECS_JSON, load_workspace_json


LAYOUT_PATTERNS = {
    "HERO-FULL",
    "HEADLINE-PROOF",
    "SPLIT-50",
    "SPLIT-60-40",
    "GRID-2COL",
    "GRID-3COL",
    "TIMELINE-H",
    "DIAGRAM-CENTER",
}
SPINE_PATTERN = re.compile(r"^(slide-\d{2})\s*\|\s*([A-Z0-9-]+)\s*\|\s*([a-z-]+)\s*\|\s*(.+)$")
LOGIC_HEAVY_ROLES = {"framing", "framework", "process", "timeline", "proof"}
GRID_PATTERNS = {"GRID-2COL", "GRID-3COL"}


def parse_spine(path: Path) -> tuple[list[tuple[str, str, str, str]], list[str]]:
    issues: list[str] = []
    entries: list[tuple[str, str, str, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue
        match = SPINE_PATTERN.match(line)
        if not match:
            continue
        slide_id, pattern, role, intent = match.groups()
        entries.append((slide_id, pattern, role, intent))
        if pattern not in LAYOUT_PATTERNS:
            issues.append(f"{slide_id}: invalid layout pattern `{pattern}` in layout-spine.md")
        if not intent.strip():
            issues.append(f"{slide_id}: layout-spine entry needs a one-line visual intent")
    return entries, issues


def run_check(workspace: Path) -> list[str]:
    issues: list[str] = []
    spine_path = workspace / "40-rebuild/layout-spine.md"
    plan_path = workspace / "35-strategy/layout-plan.json"
    if not spine_path.exists():
        return ["missing 40-rebuild/layout-spine.md"]
    try:
        plan = load_workspace_json(workspace, Path("35-strategy/layout-plan.json"))
    except FileNotFoundError:
        return [f"missing {plan_path.relative_to(workspace)}"]

    spine_entries, spine_issues = parse_spine(spine_path)
    issues.extend(spine_issues)
    if len(spine_entries) < 3:
        issues.append("layout-spine.md should contain at least 3 concrete slide entries")

    plan_slides = {slide.get("slide_id"): slide for slide in plan.get("slides", [])}
    if not plan_slides:
        issues.append("layout-plan.json should contain slide entries")
        return issues

    try:
        page_specs = load_workspace_json(workspace, PAGE_SPECS_JSON)
    except FileNotFoundError:
        page_specs = {"slides": []}

    spec_map = {slide.get("slide_id"): slide for slide in page_specs.get("slides", [])}

    for slide_id, pattern, role, intent in spine_entries:
        plan_slide = plan_slides.get(slide_id)
        if plan_slide is None:
            issues.append(f"{slide_id}: missing from layout-plan.json")
            continue
        if plan_slide.get("layout_pattern") != pattern:
            issues.append(f"{slide_id}: layout-plan pattern must match layout-spine.md")
        if plan_slide.get("slide_role") != role:
            issues.append(f"{slide_id}: layout-plan role must match layout-spine.md")
        dominant_anchor = plan_slide.get("dominant_visual_anchor")
        if not dominant_anchor or dominant_anchor == "replace-me":
            issues.append(f"{slide_id}: layout plan needs one dominant visual anchor")
        budgets = [
            plan_slide.get("title_band_pct", 0),
            plan_slide.get("anchor_region_pct", 0),
            plan_slide.get("support_region_pct", 0),
            plan_slide.get("whitespace_reserve_pct", 0),
        ]
        if sum(budgets) > 100:
            issues.append(f"{slide_id}: layout-plan budgets exceed 100%")
        if role not in {"cover", "section-divider"}:
            title_band_pct = plan_slide.get("title_band_pct", 0)
            if title_band_pct < 14:
                issues.append(f"{slide_id}: title band is too shallow for a stable deck headline system")
            if title_band_pct > 34:
                issues.append(f"{slide_id}: title band is too tall and risks turning the slide into a stacked document")
        if (
            role in LOGIC_HEAVY_ROLES
            and pattern in GRID_PATTERNS
            and role != "comparison"
        ):
            issues.append(f"{slide_id}: logic-heavy slide drifts into a grid pattern instead of a structural layout")
        if abs(plan_slide.get("anchor_region_pct", 0) - plan_slide.get("support_region_pct", 0)) < 6:
            issues.append(f"{slide_id}: anchor and support regions are too equal in weight; the slide risks losing hierarchy")
        if len(plan_slide.get("zone_skeleton", [])) == 0:
            issues.append(f"{slide_id}: layout-plan needs a zone_skeleton")
        spec = spec_map.get(slide_id)
        if spec and spec.get("layout_pattern") != pattern:
            issues.append(f"{slide_id}: page-specs.json pattern must match layout-spine.md")
        if spec:
            spec_plan = spec.get("layout_plan", {})
            if spec_plan.get("layout_hypothesis") in {"", None}:
                issues.append(f"{slide_id}: page-specs.json should carry the layout hypothesis, not only budgets")
            if spec_plan.get("dominant_reading_path") != plan_slide.get("dominant_reading_path"):
                issues.append(f"{slide_id}: page-specs.json should match layout-plan dominant_reading_path")
            if spec_plan.get("layout_confidence") != plan_slide.get("layout_confidence"):
                issues.append(f"{slide_id}: page-specs.json should match layout-plan confidence")
            if len(spec_plan.get("zone_skeleton", [])) != len(plan_slide.get("zone_skeleton", [])):
                issues.append(f"{slide_id}: page-specs.json should carry the same zone skeleton count as layout-plan.json")

    body_title_bands = [
        plan_slides[slide_id].get("title_band_pct", 0)
        for slide_id, _pattern, role, _intent in spine_entries
        if slide_id in plan_slides and role not in {"cover", "section-divider"}
    ]
    if body_title_bands and max(body_title_bands) - min(body_title_bands) > 12:
        issues.append("layout-plan title bands vary too widely across body slides and may break deck rhythm")

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <workspace-dir>")
        return 1

    workspace = Path(sys.argv[1]).expanduser().resolve()
    issues = run_check(workspace)
    if issues:
        print("[FAIL] Layout plan checks failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("[OK] Layout plan checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
