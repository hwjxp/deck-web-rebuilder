#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from _deck_checks_common import PAGE_SPECS_JSON, load_workspace_json


LOGIC_HEAVY_ROLES = {"framework", "process", "timeline", "proof"}
GRID_PATTERNS = {"GRID-2COL", "GRID-3COL"}


def run_check(workspace: Path) -> list[str]:
    issues: list[str] = []
    try:
        data = load_workspace_json(workspace, PAGE_SPECS_JSON)
    except FileNotFoundError:
        return [f"missing {PAGE_SPECS_JSON}"]

    slides = data.get("slides", [])
    opening = slides[:4]
    opening_agendas = [slide for slide in opening if slide.get("role") == "agenda"]
    if len(opening_agendas) > 1:
        issues.append("opening sequence contains more than one agenda slide; this risks duplicate orientation")

    for slide in slides:
        slide_id = slide.get("slide_id", "<unknown>")
        title = slide.get("title", {})
        spatial = slide.get("proportional_spatial_map", {})
        anchor_pct = spatial.get("anchor_region_pct", 0)
        support_pct = spatial.get("support_region_pct", 0)
        if title.get("min_container_ratio", 1) < 0.55:
            issues.append(f"{slide_id}: title container ratio below 55% suggests an artificially narrow title column")

        if (
            slide.get("role") in LOGIC_HEAVY_ROLES
            and slide.get("layout_pattern") in GRID_PATTERNS
            and slide.get("archetype") not in {"comparison-matrix"}
        ):
            issues.append(f"{slide_id}: logic-heavy slide is using a generic grid pattern instead of a structural archetype")

        if slide.get("density") == "low":
            negative_space = slide.get("negative_space_strategy", "").strip().lower()
            counterweight = slide.get("counterweight_strategy", "").strip().lower()
            if negative_space in {"", "none", "n/a"} or counterweight in {"", "none", "n/a"}:
                issues.append(f"{slide_id}: sparse slide needs an explicit negative-space plan and counterweight strategy")

        if slide.get("role") not in {"cover", "section-divider", "decision-close"} and title.get("max_lines", 0) > 2:
            issues.append(f"{slide_id}: ordinary slide titles should stay within two lines")

        if slide.get("visual_anchor") == "stat-cluster" and slide.get("layout_pattern") == "HERO-FULL":
            issues.append(f"{slide_id}: hero-full layouts should not rely on a floating stat cluster as the main anchor")

        if slide.get("layout_pattern") in GRID_PATTERNS and slide.get("density") == "low" and support_pct <= 25:
            issues.append(f"{slide_id}: low-density grid with a shallow support region risks becoming a floating card row")

        if slide.get("density") == "low" and anchor_pct < 35 and support_pct < 20:
            issues.append(f"{slide_id}: composition reserves too much unsupported empty field and risks a dead zone")

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <workspace-dir>")
        return 1

    workspace = Path(sys.argv[1]).expanduser().resolve()
    issues = run_check(workspace)
    if issues:
        print("[FAIL] Layout quality checks failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("[OK] Layout quality checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
