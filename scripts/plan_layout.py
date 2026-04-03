#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SPINE_PATTERN = re.compile(r"^(slide-\d{2})\s*\|\s*([A-Z0-9-]+)\s*\|\s*([a-z-]+)\s*\|\s*(.+)$")

PATTERN_DEFAULTS = {
    "HERO-FULL": {
        "reading_path": "hero-to-note",
        "default_anchor": "hero field",
        "diagram_policy": "n/a",
        "zones": [
            {"zone_name": "HERO-ZONE", "zone_purpose": "hero field", "content_rule": "one dominant field only"},
            {"zone_name": "TITLE-ZONE", "zone_purpose": "headline", "content_rule": "one strong headline plus optional subtitle"},
        ],
        "title_band_pct": 22,
        "anchor_region_pct": 58,
        "support_region_pct": 8,
        "whitespace_reserve_pct": 12,
    },
    "HEADLINE-PROOF": {
        "reading_path": "title-to-proof",
        "default_anchor": "primary proof object",
        "diagram_policy": "conservative-redraw",
        "zones": [
            {"zone_name": "TITLE-ZONE", "zone_purpose": "claim", "content_rule": "one claim or headline only"},
            {"zone_name": "EVIDENCE-ZONE", "zone_purpose": "proof", "content_rule": "one primary proof object"},
            {"zone_name": "ANNOTATION-ZONE", "zone_purpose": "support", "content_rule": "short interpretation only"},
        ],
        "title_band_pct": 28,
        "anchor_region_pct": 50,
        "support_region_pct": 14,
        "whitespace_reserve_pct": 8,
    },
    "SPLIT-50": {
        "reading_path": "left-to-right",
        "default_anchor": "left visual panel",
        "diagram_policy": "conservative-redraw",
        "zones": [
            {"zone_name": "VISUAL-ZONE", "zone_purpose": "left panel", "content_rule": "one balanced visual field"},
            {"zone_name": "TITLE-ZONE", "zone_purpose": "right heading", "content_rule": "headline at top of content panel"},
            {"zone_name": "INSIGHT-ZONE", "zone_purpose": "right explanation", "content_rule": "compact explanation only"},
        ],
        "title_band_pct": 18,
        "anchor_region_pct": 42,
        "support_region_pct": 26,
        "whitespace_reserve_pct": 14,
    },
    "SPLIT-60-40": {
        "reading_path": "left-to-right",
        "default_anchor": "wide-side proof field",
        "diagram_policy": "conservative-redraw",
        "zones": [
            {"zone_name": "VISUAL-ZONE", "zone_purpose": "proof side", "content_rule": "dominant visual proof"},
            {"zone_name": "TITLE-ZONE", "zone_purpose": "note rail title", "content_rule": "headline at top of note rail"},
            {"zone_name": "INSIGHT-ZONE", "zone_purpose": "note rail", "content_rule": "2-4 lines of interpretation"},
            {"zone_name": "ANNOTATION-ZONE", "zone_purpose": "secondary labels", "content_rule": "short labels only"},
        ],
        "title_band_pct": 18,
        "anchor_region_pct": 50,
        "support_region_pct": 22,
        "whitespace_reserve_pct": 10,
    },
    "GRID-2COL": {
        "reading_path": "comparison-scan",
        "default_anchor": "comparison pair",
        "diagram_policy": "n/a",
        "zones": [
            {"zone_name": "TITLE-ZONE", "zone_purpose": "title band", "content_rule": "full-width title strip"},
            {"zone_name": "GRID-CELL", "zone_purpose": "left cell", "content_rule": "parallel cell content only"},
            {"zone_name": "GRID-CELL", "zone_purpose": "right cell", "content_rule": "parallel cell content only"},
        ],
        "title_band_pct": 18,
        "anchor_region_pct": 42,
        "support_region_pct": 26,
        "whitespace_reserve_pct": 14,
    },
    "GRID-3COL": {
        "reading_path": "comparison-scan",
        "default_anchor": "comparison grid",
        "diagram_policy": "n/a",
        "zones": [
            {"zone_name": "TITLE-ZONE", "zone_purpose": "title band", "content_rule": "full-width title strip"},
            {"zone_name": "GRID-CELL", "zone_purpose": "column 1", "content_rule": "compact parallel content"},
            {"zone_name": "GRID-CELL", "zone_purpose": "column 2", "content_rule": "compact parallel content"},
            {"zone_name": "GRID-CELL", "zone_purpose": "column 3", "content_rule": "compact parallel content"},
        ],
        "title_band_pct": 18,
        "anchor_region_pct": 42,
        "support_region_pct": 26,
        "whitespace_reserve_pct": 14,
    },
    "TIMELINE-H": {
        "reading_path": "timeline-sequence",
        "default_anchor": "timeline rail",
        "diagram_policy": "redraw-as-svg",
        "zones": [
            {"zone_name": "TITLE-ZONE", "zone_purpose": "title band", "content_rule": "short headline before sequence"},
            {"zone_name": "VISUAL-ZONE", "zone_purpose": "timeline rail", "content_rule": "sequence nodes and connectors"},
            {"zone_name": "ANNOTATION-ZONE", "zone_purpose": "timeline notes", "content_rule": "short labels only"},
        ],
        "title_band_pct": 16,
        "anchor_region_pct": 48,
        "support_region_pct": 22,
        "whitespace_reserve_pct": 14,
    },
    "DIAGRAM-CENTER": {
        "reading_path": "center-out",
        "default_anchor": "central diagram",
        "diagram_policy": "redraw-as-svg",
        "zones": [
            {"zone_name": "TITLE-ZONE", "zone_purpose": "title band", "content_rule": "headline above the proof object"},
            {"zone_name": "VISUAL-ZONE", "zone_purpose": "central proof", "content_rule": "one centered diagram or matrix"},
            {"zone_name": "ANNOTATION-ZONE", "zone_purpose": "labels", "content_rule": "short labels and notes only"},
        ],
        "title_band_pct": 16,
        "anchor_region_pct": 54,
        "support_region_pct": 18,
        "whitespace_reserve_pct": 12,
    },
}


def parse_layout_spine(path: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue
        match = SPINE_PATTERN.match(line)
        if not match:
            continue
        slide_id, pattern, role, visual_intent = match.groups()
        entries.append(
            {
                "slide_id": slide_id,
                "layout_pattern": pattern,
                "slide_role": role,
                "visual_intent": visual_intent,
            }
        )
    return entries


def build_layout_plan(entries: list[dict[str, str]]) -> dict[str, object]:
    slides = []
    for entry in entries:
        defaults = PATTERN_DEFAULTS.get(entry["layout_pattern"])
        if defaults is None:
            raise ValueError(f"Unsupported layout pattern: {entry['layout_pattern']}")
        slides.append(
            {
                "slide_id": entry["slide_id"],
                "layout_pattern": entry["layout_pattern"],
                "slide_role": entry["slide_role"],
                "visual_intent": entry["visual_intent"],
                "dominant_reading_path": defaults["reading_path"],
                "dominant_visual_anchor": defaults["default_anchor"],
                "zone_skeleton": defaults["zones"],
                "title_band_pct": defaults["title_band_pct"],
                "anchor_region_pct": defaults["anchor_region_pct"],
                "support_region_pct": defaults["support_region_pct"],
                "whitespace_reserve_pct": defaults["whitespace_reserve_pct"],
                "max_body_blocks": 3,
                "copy_budget_en": 60,
                "copy_budget_zh": 60,
                "group_preservation_rules": [
                    {
                        "group_id": "replace-me",
                        "policy": "preserve-as-group",
                        "reason": "Replace with the actual group decision after visual structure decoding.",
                    }
                ],
                "diagram_redraw_policy": defaults["diagram_policy"],
                "layout_confidence": "medium",
            }
        )
    return {"slides": slides}


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print(f"Usage: {Path(sys.argv[0]).name} <workspace-dir> [output-path]")
        return 1

    workspace = Path(sys.argv[1]).expanduser().resolve()
    output_path = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) == 3 else workspace / "35-strategy/layout-plan.json"
    spine_path = workspace / "40-rebuild/layout-spine.md"
    if not spine_path.exists():
        print(f"Missing layout spine: {spine_path}")
        return 1

    entries = parse_layout_spine(spine_path)
    if not entries:
        print("No layout spine entries found.")
        return 1

    payload = build_layout_plan(entries)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
