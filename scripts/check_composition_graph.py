#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from _deck_checks_common import load_workspace_json


VALID_INTENTS = {"semantic-composite", "layout-scaffold", "content-bearing", "presentation-chrome"}
VALID_SOURCES = {"rendered-only", "object-structure", "both"}
VALID_POLICIES = {"preserve-as-group", "collapse-to-grid", "redraw-as-svg", "convert-to-css-layout", "ignore"}


def run_check(workspace: Path) -> list[str]:
    issues: list[str] = []
    relative = Path("00-source/composition-graph.json")
    try:
        data = load_workspace_json(workspace, relative)
    except FileNotFoundError:
        return [f"missing {relative}"]

    groups = data.get("groups", [])
    if not groups:
        return ["composition-graph.json should contain at least one decoded group or scaffold record"]

    for group in groups:
        group_id = group.get("group_id", "<unknown>")
        if group.get("group_intent") not in VALID_INTENTS:
            issues.append(f"{group_id}: invalid or missing group_intent")
        if group.get("evidence_source") not in VALID_SOURCES:
            issues.append(f"{group_id}: invalid or missing evidence_source")
        if group.get("rebuild_policy") not in VALID_POLICIES:
            issues.append(f"{group_id}: invalid or missing rebuild_policy")
        if group.get("confidence") in {"", None, "replace-me"}:
            issues.append(f"{group_id}: missing confidence")
        if group.get("notes") in {"", None}:
            issues.append(f"{group_id}: missing notes explaining the intent call")
        if not group.get("member_object_ids") and not group.get("member_region_ids"):
            issues.append(f"{group_id}: needs member_object_ids or member_region_ids")
        if group.get("group_intent") == "layout-scaffold" and group.get("rebuild_policy") == "preserve-as-group":
            issues.append(f"{group_id}: layout scaffolds should usually collapse to CSS layout, not preserve as a literal group")
        if group.get("group_intent") == "semantic-composite" and group.get("rebuild_policy") not in {"redraw-as-svg", "preserve-as-group"}:
            issues.append(f"{group_id}: semantic composites should redraw as SVG or preserve as a unified group")
        if group.get("group_intent") == "content-bearing" and group.get("rebuild_policy") == "ignore":
            issues.append(f"{group_id}: content-bearing objects should not default to ignore")

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <workspace-dir>")
        return 1

    workspace = Path(sys.argv[1]).expanduser().resolve()
    issues = run_check(workspace)
    if issues:
        print("[FAIL] Composition graph checks failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("[OK] Composition graph checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
