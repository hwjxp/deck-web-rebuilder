#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
import re


REQUIRED_FILES = [
    Path("10-understanding/deck-brief.md"),
    Path("12-reference-study/reference-deck-notes.md"),
    Path("20-logic/storyline.md"),
    Path("30-assets/asset-register.md"),
    Path("35-strategy/rebuild-strategy.md"),
    Path("35-strategy/deck-design-system.md"),
    Path("40-rebuild/page-specs.md"),
    Path("40-rebuild/pilot-selection.md"),
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
        if re.fullmatch(r"\|?\s*[A-Za-z][A-Za-z /-]*\s*(\|\s*[A-Za-z][A-Za-z /-]*\s*)+\|?", line):
            continue
        if re.fullmatch(r"-\s+[^:]+:\s*", line):
            continue
        meaningful_lines.append(line)

    return len(meaningful_lines) >= 2


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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
        joined = ", ".join(fixed_layout_hits)
        issues.append(f"found fixed-pixel layout anchors that suggest document-like positioning: {joined}")

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

    deck_issues = inspect_generated_deck(workspace)

    if missing:
        print("[FAIL] Missing required stage artifacts:")
        for path in missing:
            print(f"  - {path}")
    if weak:
        print("[FAIL] Stage artifacts exist but still look skeletal:")
        for path in weak:
            print(f"  - {path}")
    if deck_issues:
        print("[FAIL] Generated deck does not yet satisfy web-presentation constraints:")
        for issue in deck_issues:
            print(f"  - {issue}")

    if missing or weak or deck_issues:
        return 1

    print("[OK] Required stage artifacts exist and look non-trivial.")
    for path in REQUIRED_FILES:
        print(f"  - {path}")
    if (workspace / GENERATED_DECK_FILES["styles"]).exists():
        print("[OK] Generated deck also satisfies web-presentation static checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
