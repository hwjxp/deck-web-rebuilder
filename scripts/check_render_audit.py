#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from _deck_checks_common import PAGE_SPECS_JSON, load_workspace_json


REQUIRED_STATUSES = {
    "title_wrap_status",
    "overlap_status",
    "clipping_status",
    "occlusion_status",
    "media_uniformity_status",
    "diagram_semantics_status",
}
ALLOWED_STATUS_VALUES = {"pass", "fail", "n/a"}


def run_check(workspace: Path) -> list[str]:
    issues: list[str] = []
    page_specs = load_workspace_json(workspace, PAGE_SPECS_JSON)
    audit_path = Path("50-qa/render-audit.json")
    try:
        audit = load_workspace_json(workspace, audit_path)
    except FileNotFoundError:
        return [f"missing {audit_path}"]

    entries = {item.get("slide_id"): item for item in audit.get("slides", [])}
    if not entries:
        return ["render-audit.json should contain at least one audited slide entry"]

    for slide in page_specs.get("slides", []):
        slide_id = slide.get("slide_id", "<unknown>")
        entry = entries.get(slide_id)
        if entry is None:
            issues.append(f"{slide_id}: missing render audit entry")
            continue

        checked_languages = set(entry.get("checked_languages", []))
        if slide.get("bilingual_mode") == "toggle" and not {"zh", "en"}.issubset(checked_languages):
            issues.append(f"{slide_id}: toggle slides should be audited in both zh and en")

        title_line_counts = entry.get("title_line_counts", {})
        if slide.get("render_audit_targets", {}).get("verify_title_lines"):
            for lang in ("zh", "en"):
                if lang not in title_line_counts:
                    issues.append(f"{slide_id}: render audit should record title line counts for {lang}")

        for key in REQUIRED_STATUSES:
            value = entry.get(key)
            if value not in ALLOWED_STATUS_VALUES:
                issues.append(f"{slide_id}: render audit field `{key}` should be one of {sorted(ALLOWED_STATUS_VALUES)}")

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <workspace-dir>")
        return 1

    workspace = Path(sys.argv[1]).expanduser().resolve()
    issues = run_check(workspace)
    if issues:
        print("[FAIL] Render audit checks failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("[OK] Render audit checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
