#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <input-file> [workspace-dir]" >&2
  exit 1
fi

INPUT_FILE="$1"
if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Input file not found: $INPUT_FILE" >&2
  exit 1
fi

INPUT_ABS="$(cd "$(dirname "$INPUT_FILE")" && pwd)/$(basename "$INPUT_FILE")"
INPUT_BASENAME="$(basename "$INPUT_ABS")"
INPUT_STEM="${INPUT_BASENAME%.*}"

if [[ $# -eq 2 ]]; then
  WORKSPACE_DIR="$2"
else
  WORKSPACE_DIR="${PWD}/${INPUT_STEM}-web-rebuild"
fi

mkdir -p "$WORKSPACE_DIR"/00-source
mkdir -p "$WORKSPACE_DIR"/10-understanding
mkdir -p "$WORKSPACE_DIR"/20-logic
mkdir -p "$WORKSPACE_DIR"/30-assets
mkdir -p "$WORKSPACE_DIR"/35-strategy
mkdir -p "$WORKSPACE_DIR"/40-rebuild
mkdir -p "$WORKSPACE_DIR"/50-qa

cp -f "$INPUT_ABS" "$WORKSPACE_DIR/00-source/$INPUT_BASENAME"

cat > "$WORKSPACE_DIR/10-understanding/deck-brief.md" <<'EOF'
# Deck Brief

## Topic

## Speaker Or Organization

## Audience

## Occasion

## Persuasion Goal

## Tone

## Deck Summary

## Intended Audience Outcome
EOF

cat > "$WORKSPACE_DIR/20-logic/storyline.md" <<'EOF'
# Storyline

## Deck Arc

## Slide Roles

| Source Slide | Role | Main Point | Supporting Evidence | Visual Role | Relationship Notes |
| --- | --- | --- | --- | --- | --- |

## Logic Breaks Or Redundancy
EOF

cat > "$WORKSPACE_DIR/30-assets/asset-register.md" <<'EOF'
# Asset Register

| Asset ID | Source Slide | Asset Type | Semantic Role | Action | Reason | Translation Needed | Redraw Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
EOF

cat > "$WORKSPACE_DIR/35-strategy/rebuild-strategy.md" <<'EOF'
# Rebuild Strategy

## Fidelity Mode

## Style Direction

## Must Not Change

## May Change

## Density Target

## Motion Level

## Bilingual Mode

## Merge Or Split Decisions
EOF

cat > "$WORKSPACE_DIR/40-rebuild/page-specs.md" <<'EOF'
# Page Specs

## Slide Template

- Source Slide:
- Destination Slide ID:
- Slide Role:
- Core Takeaway:
- Required Copy Blocks:
- Required Assets:
- Target Layout Pattern:
- Animation Intent:
- Bilingual Treatment:
- Fidelity Notes:
EOF

cat > "$WORKSPACE_DIR/50-qa/qa-report.md" <<'EOF'
# QA Report

## Layout Issues Found And Fixed

## Remaining Issues

## Logic Fidelity Checks

## Bilingual Checks

## Navigation And Deep Link Checks

## PDF Export Check

## Final Go Or No-Go
EOF

echo "Workspace prepared at: $WORKSPACE_DIR"
echo "Source copied to: $WORKSPACE_DIR/00-source/$INPUT_BASENAME"
