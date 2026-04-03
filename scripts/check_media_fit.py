#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from _deck_checks_common import PAGE_SPECS_JSON, load_workspace_json


STRUCTURED_ASSET_ROLES = {"diagram", "chart", "table", "screenshot"}


def run_check(workspace: Path) -> list[str]:
    issues: list[str] = []
    try:
        data = load_workspace_json(workspace, PAGE_SPECS_JSON)
    except FileNotFoundError:
        return [f"missing {PAGE_SPECS_JSON}"]

    for slide in data.get("slides", []):
        slide_id = slide.get("slide_id", "<unknown>")
        media_contract = slide.get("media_layout_contract", {})
        for asset in slide.get("assets", []):
            role = asset.get("role")
            action = asset.get("action")
            fit_policy = asset.get("fit_policy")
            must_show_full_frame = asset.get("must_show_full_frame")
            visible_area_min_pct = asset.get("visible_area_min_pct", 0)

            if action == "remove":
                continue

            if must_show_full_frame and visible_area_min_pct < 95:
                issues.append(f"{slide_id}: assets marked must_show_full_frame should target at least 95% visible area")

            if role in STRUCTURED_ASSET_ROLES and fit_policy in {"cover", "background-cover"}:
                issues.append(f"{slide_id}: {role} assets should not use cover-style fitting")

            if role in {"diagram", "chart", "table"} and action != "redraw" and fit_policy == "safe-crop":
                issues.append(f"{slide_id}: structured assets should not rely on safe-crop unless the page spec justifies it elsewhere")

        if any(asset.get("must_show_full_frame") for asset in slide.get("assets", [])):
            if media_contract.get("default_fit_policy") in {"cover", "background-cover"}:
                issues.append(f"{slide_id}: default fit policy should not be cover when the slide includes full-frame assets")
            if media_contract.get("clip_tolerance") != "none":
                issues.append(f"{slide_id}: slides with full-frame assets should default to no clipping")

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <workspace-dir>")
        return 1

    workspace = Path(sys.argv[1]).expanduser().resolve()
    issues = run_check(workspace)
    if issues:
        print("[FAIL] Media fit checks failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("[OK] Media fit checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
