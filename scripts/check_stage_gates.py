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

    if missing:
        print("[FAIL] Missing required stage artifacts:")
        for path in missing:
            print(f"  - {path}")
    if weak:
        print("[FAIL] Stage artifacts exist but still look skeletal:")
        for path in weak:
            print(f"  - {path}")

    if missing or weak:
        return 1

    print("[OK] Required stage artifacts exist and look non-trivial.")
    for path in REQUIRED_FILES:
        print(f"  - {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
