#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from _deck_checks_common import DESIGN_SCHEMA, DESIGN_SYSTEM_JSON, load_workspace_json, maybe_validate_with_jsonschema
from check_bilingual_fit import run_check as run_bilingual_fit_check
from check_layout_quality import run_check as run_layout_quality_check
from check_page_specs import run_check as run_page_spec_check
from check_redundancy import run_check as run_redundancy_check


REQUIRED_FILES = [
    Path("00-source/input-profile.md"),
    Path("00-source/visual-regions.json"),
    Path("10-understanding/deck-brief.md"),
    Path("12-reference-study/reference-deck-notes.md"),
    Path("12-reference-study/reference-deck-notes.yaml"),
    Path("20-logic/storyline.md"),
    Path("20-logic/confidence-report.md"),
    Path("30-assets/asset-register.md"),
    Path("30-assets/asset-lineage.json"),
    Path("35-strategy/rebuild-strategy.md"),
    Path("35-strategy/deck-design-system.md"),
    Path("35-strategy/deck-design-system.json"),
    Path("40-rebuild/page-specs.md"),
    Path("40-rebuild/page-specs.json"),
    Path("40-rebuild/pilot-selection.md"),
    Path("50-qa/visual-checklist.md"),
]

GENERATED_DECK_FILES = {
    "html": Path("40-rebuild/deck/index.html"),
    "styles": Path("40-rebuild/deck/styles.css"),
}

ASPECT_RATIO_PATTERN = re.compile(r"aspect-ratio\s*:\s*16\s*/\s*9\b", re.IGNORECASE)
VIEWPORT_HEIGHT_PATTERN = re.compile(r"100(?:d|s)?vh\b", re.IGNORECASE)
VIEWPORT_WIDTH_PATTERN = re.compile(r"100(?:d|s)?vw\b", re.IGNORECASE)
OVERFLOW_HIDDEN_PATTERN = re.compile(r"overflow\s*:\s*hidden\b", re.IGNORECASE)
SCROLL_SUPPRESSION_PATTERN = re.compile(
    r"(html\s*,\s*body|body|html)\s*\{[^}]*overflow\s*:\s*hidden",
    re.IGNORECASE | re.DOTALL,
)
CONTAINER_TYPE_PATTERN = re.compile(r"container-type\s*:\s*(?:size|inline-size)\b", re.IGNORECASE)
SLIDE_RELATIVE_UNIT_PATTERN = re.compile(
    r"\b\d*\.?\d+(?:cqi|cqw|cqh|cqmin|cqmax|vmin)\b",
    re.IGNORECASE,
)
FIXED_LAYOUT_PX_PATTERN = re.compile(
    r"\b(left|right|top|bottom|width|height)\s*:\s*(\d+(?:\.\d+)?)px\b",
    re.IGNORECASE,
)
SLIDE_SPEC_HEADING_PATTERN = re.compile(r"^##\s+slide-[0-9]{2}\b", re.IGNORECASE | re.MULTILINE)
SLIDE_ID_PATTERN = re.compile(r"slide-[0-9]{2}", re.IGNORECASE)


def is_meaningful(path: Path) -> bool:
    text = path.read_text(encoding="utf-8").strip()
    nonempty_lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(nonempty_lines) < 3:
        return False

    meaningful_lines = []
    for line in nonempty_lines:
        if line.startswith("#"):
            continue
        if re.fullmatch(r"\|?\s*[-:| ]+\|?", line):
            continue
        if re.fullmatch(r"\|?\s*[A-Za-z][A-Za-z /_-]*\s*(\|\s*[A-Za-z][A-Za-z /_-]*\s*)+\|?", line):
            continue
        if re.fullmatch(r"-\s+[^:]+:\s*", line):
            continue
        if re.fullmatch(r"[{}\[\],\": ]+", line):
            continue
        meaningful_lines.append(line)

    return len(meaningful_lines) >= 2


def meaningful_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if re.fullmatch(r"\|?\s*[-:| ]+\|?", line):
            continue
        if re.fullmatch(r"\|?\s*[A-Za-z][A-Za-z /_-]*\s*(\|\s*[A-Za-z][A-Za-z /_-]*\s*)+\|?", line):
            continue
        if re.fullmatch(r"-\s+[^:]+:\s*", line):
            continue
        if re.fullmatch(r"[{}\[\],\": ]+", line):
            continue
        lines.append(line)
    return lines


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_deck_brief(path: Path) -> list[str]:
    text = read_text(path)
    issues: list[str] = []
    prose = " ".join(meaningful_lines(text))
    if len(prose) <= 150:
        issues.append("deck-brief.md is too short; write a real deck-level understanding before moving on")
    lowered = text.lower()
    for keyword in ("audience", "persuasion goal"):
        if keyword not in lowered:
            issues.append(f"deck-brief.md should explicitly include `{keyword}`")
    return issues


def check_input_profile(path: Path) -> list[str]:
    text = read_text(path)
    lowered = text.lower()
    issues: list[str] = []
    for keyword in ("input mode", "source-of-truth", "normalization plan"):
        if keyword not in lowered:
            issues.append(f"input-profile.md should explicitly include `{keyword}`")
    if "visual" not in lowered:
        issues.append("input-profile.md should note the role of visual parsing for this source")
    return issues


def check_design_system_markdown(path: Path) -> list[str]:
    text = read_text(path)
    issues: list[str] = []
    if "--font" not in text and "font-size" not in text:
        issues.append("deck-design-system.md should define real typography tokens such as `--font` or `font-size`")
    if "title" not in text.lower() or "bilingual" not in text.lower():
        issues.append("deck-design-system.md should include title and bilingual rules, not only mood-board prose")
    if "title band" not in text.lower() and "title-band" not in text.lower():
        issues.append("deck-design-system.md should define a title-band system, not only local title styling")
    return issues


def check_reference_notes_yaml(path: Path) -> list[str]:
    text = read_text(path)
    issues: list[str] = []
    for token in ("reference_deck_notes:", "shell:", "page_archetypes:", "text_image_contract:", "anti_patterns:"):
        if token not in text:
            issues.append(f"reference-deck-notes.yaml should include `{token}`")
    return issues


def check_confidence_report(path: Path) -> list[str]:
    text = read_text(path)
    lowered = text.lower()
    issues: list[str] = []
    for keyword in ("high", "medium", "low"):
        if keyword not in lowered:
            issues.append(f"confidence-report.md should explicitly include `{keyword}` confidence")
    if "follow-up" not in lowered and "next action" not in lowered and "action" not in lowered:
        issues.append("confidence-report.md should note follow-up actions for uncertain slides or relations")
    return issues


def check_page_specs_markdown(path: Path) -> list[str]:
    text = read_text(path)
    count = len(SLIDE_SPEC_HEADING_PATTERN.findall(text))
    if count < 3:
        return ["page-specs.md should contain at least 3 concrete `## slide-NN` sections before implementation"]
    return []


def check_pilot_selection(path: Path) -> list[str]:
    text = read_text(path)
    slide_ids = {match.lower() for match in SLIDE_ID_PATTERN.findall(text)}
    if len(slide_ids) < 5:
        return ["pilot-selection.md should identify at least 5 slide ids such as `slide-01`"]
    return []


def check_visual_regions_json(workspace: Path) -> list[str]:
    issues: list[str] = []
    relative = Path("00-source/visual-regions.json")
    try:
        data = load_workspace_json(workspace, relative)
    except Exception as exc:
        return [f"could not read {relative}: {exc}"]

    slides = data.get("slides", [])
    if not slides:
        return ["visual-regions.json should contain at least one slide or page parse"]

    total_regions = 0
    for slide in slides:
        regions = slide.get("regions", [])
        total_regions += len(regions)
        for region in regions:
            if "type" not in region or "confidence" not in region:
                issues.append("visual-regions.json regions should include at least `type` and `confidence`")
                return issues
    if total_regions == 0:
        issues.append("visual-regions.json should contain actual visual regions, not only slide shells")
    return issues


def check_asset_lineage_json(workspace: Path) -> list[str]:
    issues: list[str] = []
    relative = Path("30-assets/asset-lineage.json")
    try:
        data = load_workspace_json(workspace, relative)
    except Exception as exc:
        return [f"could not read {relative}: {exc}"]

    assets = data.get("assets", [])
    if not assets:
        return ["asset-lineage.json should contain at least one asset lineage record"]

    for asset in assets:
        if not asset.get("source_region_ids"):
            issues.append("asset-lineage.json assets should record `source_region_ids`")
            break
        if not asset.get("chosen_action"):
            issues.append("asset-lineage.json assets should record `chosen_action`")
            break
    return issues


def check_design_system_json(workspace: Path) -> list[str]:
    issues: list[str] = []
    try:
        data = load_workspace_json(workspace, DESIGN_SYSTEM_JSON)
    except FileNotFoundError:
        return [f"missing {DESIGN_SYSTEM_JSON}"]
    except Exception as exc:  # pragma: no cover - defensive path
        return [f"could not read {DESIGN_SYSTEM_JSON}: {exc}"]

    issues.extend(maybe_validate_with_jsonschema(data, DESIGN_SCHEMA))

    title_wrap = data.get("typography", {}).get("title_wrapping", {})
    if title_wrap.get("min_title_container_ratio", 0) < 0.6:
        issues.append("deck-design-system.json should target a title container ratio of at least 60%")

    fallback_order = title_wrap.get("fallback_order", [])
    if fallback_order[:3] != ["rewrite", "restack", "widen-title-region"]:
        issues.append("deck-design-system.json should prioritize rewrite -> restack -> widen-title-region before shrinking")

    title_band = data.get("title_band", {})
    if title_band.get("min_width_ratio", 0) < 0.6:
        issues.append("deck-design-system.json should keep the title band above 60% width on ordinary slides")
    if not title_band.get("prefer_single_line", False):
        issues.append("deck-design-system.json should prefer single-line titles by default on body slides")

    grid = data.get("grid", {})
    if grid.get("columns") != 8:
        issues.append("deck-design-system.json should use an 8-column base slide grid")
    outer_margin = grid.get("outer_margin", {})
    expected_margins = {"mobile": "16px", "tablet": "24px", "desktop": "32px"}
    if outer_margin != expected_margins:
        issues.append("deck-design-system.json should define outer margins as 16px / 24px / 32px for mobile / tablet / desktop")
    if grid.get("content_max_width") != "1280px":
        issues.append("deck-design-system.json should set `content_max_width` to `1280px`")

    language_toggle = data.get("page_chrome", {}).get("language_toggle", "").lower()
    if "toggle" not in language_toggle:
        issues.append("deck-design-system.json should define a persistent language toggle in page chrome")

    return issues


def run_script_checks(workspace: Path) -> list[str]:
    issues: list[str] = []
    for issue in check_design_system_json(workspace):
        issues.append(f"design system: {issue}")
    for label, runner in (
        ("page specs", run_page_spec_check),
        ("layout quality", run_layout_quality_check),
        ("bilingual fit", run_bilingual_fit_check),
        ("redundancy", run_redundancy_check),
    ):
        for issue in runner(workspace):
            issues.append(f"{label}: {issue}")
    return issues


def inspect_generated_deck(workspace: Path) -> list[str]:
    styles_path = workspace / GENERATED_DECK_FILES["styles"]
    if not styles_path.exists():
        return []

    css = read_text(styles_path)
    issues: list[str] = []

    if not ASPECT_RATIO_PATTERN.search(css):
        issues.append("missing `aspect-ratio: 16 / 9` on the generated slide canvas")
    if not VIEWPORT_HEIGHT_PATTERN.search(css) or not VIEWPORT_WIDTH_PATTERN.search(css):
        issues.append("missing clear viewport-bound sizing tokens such as `100vh` and `100vw`")
    if not OVERFLOW_HIDDEN_PATTERN.search(css):
        issues.append("missing `overflow: hidden` needed for bounded slide playback")
    if not SCROLL_SUPPRESSION_PATTERN.search(css):
        issues.append("missing native-scroll suppression on `html` or `body` for presentation mode")
    if not CONTAINER_TYPE_PATTERN.search(css):
        issues.append("missing `container-type` declaration for synchronized slide scaling")
    if not SLIDE_RELATIVE_UNIT_PATTERN.search(css):
        issues.append("missing container-query or slide-relative sizing units such as `cqi`, `cqw`, `cqh`, or `vmin`")

    fixed_layout_hits = []
    for match in FIXED_LAYOUT_PX_PATTERN.finditer(css):
        value = float(match.group(2))
        if value >= 24:
            fixed_layout_hits.append(f"{match.group(1)}: {match.group(2)}px")
        if len(fixed_layout_hits) >= 5:
            break
    if fixed_layout_hits:
        issues.append(
            "found fixed-pixel layout anchors that suggest document-like positioning: "
            + ", ".join(fixed_layout_hits)
        )

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <workspace-dir>")
        return 1

    workspace = Path(sys.argv[1]).expanduser().resolve()
    if not workspace.is_dir():
        print(f"[FAIL] Workspace not found: {workspace}")
        return 1

    missing = []
    weak = []
    for relative_path in REQUIRED_FILES:
        full_path = workspace / relative_path
        if not full_path.exists():
            missing.append(relative_path)
            continue
        if not is_meaningful(full_path):
            weak.append(relative_path)

    content_issues: list[str] = []
    script_issues: list[str] = []
    if not missing:
        content_issues.extend(check_input_profile(workspace / "00-source/input-profile.md"))
        content_issues.extend(check_deck_brief(workspace / "10-understanding/deck-brief.md"))
        content_issues.extend(check_reference_notes_yaml(workspace / "12-reference-study/reference-deck-notes.yaml"))
        content_issues.extend(check_confidence_report(workspace / "20-logic/confidence-report.md"))
        content_issues.extend(check_design_system_markdown(workspace / "35-strategy/deck-design-system.md"))
        content_issues.extend(check_page_specs_markdown(workspace / "40-rebuild/page-specs.md"))
        content_issues.extend(check_pilot_selection(workspace / "40-rebuild/pilot-selection.md"))
        content_issues.extend(check_visual_regions_json(workspace))
        content_issues.extend(check_asset_lineage_json(workspace))
        script_issues = run_script_checks(workspace)

    deck_issues = inspect_generated_deck(workspace)

    if missing:
        print("[FAIL] Missing required stage artifacts:")
        for path in missing:
            print(f"  - {path}")
    if weak:
        print("[FAIL] Stage artifacts exist but still look skeletal:")
        for path in weak:
            print(f"  - {path}")
    if content_issues:
        print("[FAIL] Required documents exist but still miss key design-system content:")
        for issue in content_issues:
            print(f"  - {issue}")
    if script_issues:
        print("[FAIL] Schema-driven quality checks failed:")
        for issue in script_issues:
            print(f"  - {issue}")
    if deck_issues:
        print("[FAIL] Generated deck does not yet satisfy web-presentation constraints:")
        for issue in deck_issues:
            print(f"  - {issue}")

    if missing or weak or content_issues or script_issues or deck_issues:
        return 1

    print("[OK] Required stage artifacts exist and look non-trivial.")
    for path in REQUIRED_FILES:
        print(f"  - {path}")
    print("[OK] Schema-driven page, bilingual, layout, and redundancy checks passed.")
    if (workspace / GENERATED_DECK_FILES["styles"]).exists():
        print("[OK] Generated deck also satisfies web-presentation static checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
