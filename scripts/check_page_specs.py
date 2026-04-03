#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from _deck_checks_common import PAGE_SCHEMA, PAGE_SPECS_JSON, load_workspace_json, maybe_validate_with_jsonschema

VISUAL_ASSET_ROLES = {"hero-image", "support-image", "diagram", "chart", "table", "screenshot"}


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

        layout_plan = slide.get("layout_plan", {})
        if not layout_plan:
            issues.append(f"{slide_id}: missing layout_plan")
            continue

        if layout_plan.get("title_band_pct") != slide.get("proportional_spatial_map", {}).get("title_region_pct"):
            issues.append(f"{slide_id}: layout_plan.title_band_pct should match proportional_spatial_map.title_region_pct")
        if layout_plan.get("anchor_region_pct") != slide.get("proportional_spatial_map", {}).get("anchor_region_pct"):
            issues.append(f"{slide_id}: layout_plan.anchor_region_pct should match proportional_spatial_map.anchor_region_pct")
        if layout_plan.get("support_region_pct") != slide.get("proportional_spatial_map", {}).get("support_region_pct"):
            issues.append(f"{slide_id}: layout_plan.support_region_pct should match proportional_spatial_map.support_region_pct")
        total_budget = (
            layout_plan.get("title_band_pct", 0)
            + layout_plan.get("anchor_region_pct", 0)
            + layout_plan.get("support_region_pct", 0)
            + layout_plan.get("whitespace_reserve_pct", 0)
        )
        if total_budget > 100:
            issues.append(f"{slide_id}: layout budgets exceed 100% of the slide")
        if len(slide.get("body_blocks", [])) > layout_plan.get("max_body_blocks", 99):
            issues.append(f"{slide_id}: body_blocks exceed the planned max_body_blocks")
        if slide.get("visual_anchor") == "diagram" and layout_plan.get("diagram_redraw_policy") == "n/a":
            issues.append(f"{slide_id}: diagram slides need a real diagram_redraw_policy")
        if not layout_plan.get("group_preservation_rules"):
            issues.append(f"{slide_id}: layout_plan should record group preservation rules, even if conservative")

        title = slide.get("title", {})
        if not title.get("fallback_strategy"):
            issues.append(f"{slide_id}: missing title fallback strategy")
        posture = title.get("posture")
        prefer_no_wrap = title.get("prefer_no_wrap")
        max_lines = title.get("max_lines")
        min_container_ratio = title.get("min_container_ratio", 0)
        source_line_count = title.get("source_line_count", 0)
        line_count_strategy = title.get("line_count_strategy")

        if posture == "single-line" and max_lines != 1:
            issues.append(f"{slide_id}: single-line title posture should use `max_lines: 1`")
        if posture == "single-line" and not prefer_no_wrap:
            issues.append(f"{slide_id}: single-line title posture should set `prefer_no_wrap: true`")
        if posture == "balanced-two-line" and prefer_no_wrap:
            issues.append(f"{slide_id}: balanced-two-line titles should not force `prefer_no_wrap: true`")
        if prefer_no_wrap and min_container_ratio < 0.6:
            issues.append(f"{slide_id}: no-wrap titles should keep at least 60% title container width")
        if input_mode != "editorial-compose" and source_line_count <= 0:
            issues.append(f"{slide_id}: non-editorial slides should record the source title line count")
        if line_count_strategy == "preserve-source" and source_line_count > 0 and max_lines != source_line_count:
            issues.append(f"{slide_id}: preserve-source title strategy should keep `max_lines` equal to the source line count")
        if (
            slide.get("role") in {"section-divider", "framing"}
            and source_line_count == 1
            and line_count_strategy != "preserve-source"
        ):
            issues.append(f"{slide_id}: framing and divider slides with one-line source titles should preserve that line-count intent")
        if (
            source_line_count > 0
            and max_lines > source_line_count
            and line_count_strategy != "rewrite-and-refit"
            and not title.get("wrap_justification")
        ):
            issues.append(f"{slide_id}: expanding beyond the source title line count needs a wrap justification or rewrite-and-refit strategy")

        if not slide.get("forbidden_patterns"):
            issues.append(f"{slide_id}: forbidden_patterns should be declared explicitly")

        source_of_truth = set(slide.get("source_of_truth", []))
        if input_mode != "editorial-compose" and "visual-render" not in source_of_truth:
            issues.append(f"{slide_id}: non-editorial slides should include `visual-render` in source_of_truth")
        if slide.get("confidence_level") == "low" and slide.get("primary_proof_device") not in {"none", "hero-image"}:
            issues.append(f"{slide_id}: low-confidence proof slides should be investigated before free redraw")

        diagram_contract = slide.get("diagram_contract", {})
        if slide.get("primary_proof_device") == "diagram" or slide.get("visual_anchor") == "diagram" or slide.get("archetype") == "diagram-plus-insight":
            if diagram_contract.get("relation_type") == "none":
                issues.append(f"{slide_id}: diagram-driven slides should declare a real diagram relation type")
            if diagram_contract.get("primitive_count", 0) <= 0:
                issues.append(f"{slide_id}: diagram-driven slides should declare the source proof primitive count")
        if diagram_contract.get("relation_type") == "overlap":
            if diagram_contract.get("primitive_count", 0) < 2:
                issues.append(f"{slide_id}: overlap diagrams should have at least two primary shapes")
            if not diagram_contract.get("must_preserve_overlap"):
                issues.append(f"{slide_id}: overlap diagrams should explicitly preserve overlap semantics")

        media_contract = slide.get("media_layout_contract", {})
        live_visual_assets = [asset for asset in slide.get("assets", []) if asset.get("role") in VISUAL_ASSET_ROLES and asset.get("action") != "remove"]
        if len(live_visual_assets) >= 3 and media_contract.get("uniform_media_height") == "n/a":
            issues.append(f"{slide_id}: multi-media slides should declare whether media heights are strict or flexible")
        if slide.get("layout_pattern") == "GRID-3COL" and media_contract.get("uniform_media_height") != "strict":
            issues.append(f"{slide_id}: GRID-3COL sample pages should usually enforce strict media height alignment")
        for asset in live_visual_assets:
            if asset.get("must_show_full_frame") and asset.get("fit_policy") in {"cover", "background-cover"}:
                issues.append(f"{slide_id}: assets marked must_show_full_frame should not use cover-style fitting")
            if asset.get("role") in {"diagram", "chart", "table", "screenshot"} and asset.get("fit_policy") == "cover":
                issues.append(f"{slide_id}: structured visual assets should not use `cover` fitting")

        render_targets = slide.get("render_audit_targets", {})
        if source_line_count > 0 and not render_targets.get("verify_title_lines"):
            issues.append(f"{slide_id}: render audit should verify title lines when source line count matters")
        if live_visual_assets and not render_targets.get("verify_clipping"):
            issues.append(f"{slide_id}: render audit should verify clipping on image-bearing slides")
        if len(live_visual_assets) >= 3 and not render_targets.get("verify_media_alignment"):
            issues.append(f"{slide_id}: render audit should verify media alignment on multi-media slides")
        if (slide.get("primary_proof_device") == "diagram" or slide.get("visual_anchor") == "diagram") and not render_targets.get("verify_diagram_semantics"):
            issues.append(f"{slide_id}: diagram slides should verify diagram semantics during render audit")

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
