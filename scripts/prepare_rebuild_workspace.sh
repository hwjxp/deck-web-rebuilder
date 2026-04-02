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
mkdir -p "$WORKSPACE_DIR"/12-reference-study
mkdir -p "$WORKSPACE_DIR"/20-logic
mkdir -p "$WORKSPACE_DIR"/30-assets
mkdir -p "$WORKSPACE_DIR"/35-strategy
mkdir -p "$WORKSPACE_DIR"/40-rebuild
mkdir -p "$WORKSPACE_DIR"/40-rebuild/deck
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

cat > "$WORKSPACE_DIR/12-reference-study/reference-deck-notes.md" <<'EOF'
# Reference Deck Notes

## Reference Files Reviewed

## Deck-Shell Rules

## Recurring Page Archetypes

## Text-Image Rules Worth Copying

## Anti-Patterns To Avoid

## Transfer Plan For The Target Deck
EOF

cat > "$WORKSPACE_DIR/12-reference-study/reference-deck-notes.yaml" <<'EOF'
reference_deck_notes:
  shell:
    cover_style: "replace-me"
    section_divider: "replace-me"
    body_chrome: "replace-me"
    accent_color_count: 1
  page_archetypes:
    - name: "replace-me"
      layout_pattern: "HEADLINE-PROOF"
      text_image_ratio: "70:30"
  text_image_contract:
    anchor_count: 1
    caption_distance: "tight"
    note_panel_behavior: "replace-me"
  anti_patterns:
    - "replace-me"
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

cat > "$WORKSPACE_DIR/35-strategy/deck-design-system.md" <<'EOF'
# Deck Design System

Copy the baseline structure from `references/deck-design-system-template.md`, then replace each placeholder with deck-specific decisions.

## 1. Rhetorical Context

- theme:
- occasion:
- speaker:
- audience:
- persuasion job:
- tone keywords:

## 2. Canvas Rules

- base canvas: `1440 x 810`
- aspect ratio: `16:9`
- viewport policy:
- overflow policy:
- scaling model:
- preferred units:

## 3. CSS Tokens

```css
:root {
  --font-family-display: "Inter", "Helvetica Neue", sans-serif;
  --font-family-body: "Inter", "Helvetica Neue", sans-serif;
  --font-family-mono: "JetBrains Mono", monospace;

  --font-size-display: 5.6cqi;
  --font-size-title: 3.4cqi;
  --font-size-subtitle: 2.3cqi;
  --font-size-body: 1.55cqi;
  --font-size-caption: 1.2cqi;
  --font-size-label: 0.98cqi;
}
```

## 4. Typography Rules

- title wrapping:
- body measure:
- bilingual fallback order:

## 5. Grid And Page Chrome

- grid:
- navigation:
- language toggle:
- deep links:

## 6. Negative Space And Mobile

- blank ratio:
- counterweight rule:
- mobile degradation order:

## 7. Do / Don't

Do:

- one dominant visual anchor per slide

Don't:

- narrow title columns
- duplicate agenda after the cover already orients
EOF

cat > "$WORKSPACE_DIR/35-strategy/deck-design-system.json" <<'EOF'
{
  "deck_id": "replace-with-deck-id",
  "theme": {
    "tonal_direction": "replace-me",
    "visual_intensity": "balanced",
    "composition_posture": "asymmetric"
  },
  "canvas": {
    "aspect_ratio": "16:9",
    "base_width": 1440,
    "base_height": 810,
    "viewport_policy": "fit the whole slide inside the viewport without native browser scroll",
    "overflow_policy": "hidden-at-slide-level",
    "preferred_units": ["cqi", "cqw", "cqh", "vmin"]
  },
  "typography": {
    "fonts": {
      "display": "Inter 700",
      "body": "Inter 400",
      "mono": "JetBrains Mono 500"
    },
    "type_scale": {
      "display": "5.6cqi",
      "title": "3.4cqi",
      "subtitle": "2.3cqi",
      "body": "1.55cqi",
      "caption": "1.2cqi",
      "label": "0.98cqi"
    },
    "line_heights": {
      "display": 1.1,
      "title": 1.1,
      "body": 1.55,
      "caption": 1.35
    },
    "font_weights": {
      "display": 700,
      "title": 700,
      "body": 400,
      "emphasis": 600
    },
    "body_measure": {
      "body_max_inline_size": "68ch",
      "caption_max_inline_size": "48ch"
    },
    "title_wrapping": {
      "max_title_lines": 2,
      "min_title_container_ratio": 0.55,
      "fallback_order": ["rewrite", "restack", "widen-title-region", "shrink-last"]
    }
  },
  "color_slots": {
    "background": "replace-me",
    "surface": "replace-me",
    "text_primary": "replace-me",
    "accent": "replace-me",
    "muted": "replace-me"
  },
  "spacing_scale": {
    "space_4": "0.4cqi",
    "space_8": "0.8cqi",
    "space_12": "1.2cqi",
    "space_16": "1.6cqi",
    "space_20": "2cqi",
    "space_24": "2.4cqi",
    "space_32": "3.2cqi",
    "space_40": "4cqi"
  },
  "grid": {
    "columns": 12,
    "gutter": "1.6cqi",
    "outer_margin": "2.4cqi",
    "content_max_width": "92cqi"
  },
  "page_chrome": {
    "navigation": "top-right controls with previous and next buttons",
    "counter": "persistent current / total slide counter",
    "language_toggle": "sticky visible toggle in chrome",
    "deep_links": "slide ids use #slide-NN"
  },
  "negative_space_policy": {
    "default_blank_ratio": "20-30%",
    "counterweight_rule": "every large blank field needs a visible anchor or opposing mass"
  },
  "bilingual_policy": {
    "default_mode": "toggle",
    "title_word_limit_en": 22,
    "title_char_limit_zh": 28,
    "fallback_order": ["rewrite", "restack", "widen-title-region", "shrink-last"]
  },
  "motion_policy": {
    "default_level": "subtle",
    "reduced_motion_behavior": "reduce to opacity changes and disable travel motion"
  },
  "layout_do": [
    "one dominant visual anchor per slide",
    "use proportional regions instead of large fixed-pixel positioning"
  ],
  "layout_dont": [
    "narrow title columns",
    "duplicate agenda after the deck shell already orients",
    "flatten logic pages into generic card rows"
  ]
}
EOF

cat > "$WORKSPACE_DIR/40-rebuild/page-specs.md" <<'EOF'
# Page Specs

Use `references/layout-patterns.md`, `references/page-archetypes.md`, and `references/typography-rules.md`. Do not invent new layout vocabulary.

## slide-01

- Source Slide:
- Destination Slide ID: `slide-01`
- Slide Role:
- Archetype:
- Core Takeaway:
- Required Copy Blocks:
- Required Assets:
- Target Layout Pattern:
- Proportional Spatial Map:
- Dominant Visual Anchor:
- Primary Proof Device:
- Bilingual Treatment:
- Mobile Degradation Plan:
- Animation Intent:
- Forbidden Patterns:
- Fidelity Notes:

## slide-02

- Source Slide:
- Destination Slide ID: `slide-02`
- Slide Role:
- Archetype:
- Core Takeaway:
- Required Copy Blocks:
- Required Assets:
- Target Layout Pattern:
- Proportional Spatial Map:
- Dominant Visual Anchor:
- Primary Proof Device:
- Bilingual Treatment:
- Mobile Degradation Plan:
- Animation Intent:
- Forbidden Patterns:
- Fidelity Notes:

## slide-03

- Source Slide:
- Destination Slide ID: `slide-03`
- Slide Role:
- Archetype:
- Core Takeaway:
- Required Copy Blocks:
- Required Assets:
- Target Layout Pattern:
- Proportional Spatial Map:
- Dominant Visual Anchor:
- Primary Proof Device:
- Bilingual Treatment:
- Mobile Degradation Plan:
- Animation Intent:
- Forbidden Patterns:
- Fidelity Notes:
EOF

cat > "$WORKSPACE_DIR/40-rebuild/page-specs.json" <<'EOF'
{
  "deck_id": "replace-with-deck-id",
  "source_file": "00-source/replace-with-source-file",
  "default_bilingual_mode": "toggle",
  "slides": [
    {
      "slide_id": "slide-01",
      "source_slide_number": 1,
      "role": "cover",
      "archetype": "cover",
      "layout_pattern": "HERO-FULL",
      "takeaway": {
        "en": "Replace with the deck's cover claim.",
        "zh": "请替换为封面的核心表达。"
      },
      "density": "low",
      "visual_anchor": "hero-image",
      "title": {
        "text": {
          "en": "Replace With The Final Cover Title",
          "zh": "请替换为最终封面标题"
        },
        "max_lines": 2,
        "preferred_width_ch": 28,
        "min_container_ratio": 0.62,
        "fallback_strategy": ["rewrite", "restack", "widen-title-region", "shrink-last"]
      },
      "body_blocks": [],
      "assets": [
        {
          "asset_id": "cover-hero",
          "role": "hero-image",
          "action": "keep",
          "notes": "Replace with the chosen hero asset or tonal field."
        }
      ],
      "proportional_spatial_map": {
        "title_region_pct": 68,
        "anchor_region_pct": 72,
        "support_region_pct": 12,
        "notes": "Cover shell only; no extra agenda row."
      },
      "primary_proof_device": "hero-image",
      "bilingual_mode": "toggle",
      "mobile_degradation_plan": {
        "order": ["scale-slide", "trim-decoration", "tighten-spacing", "rewrite-copy"],
        "reflow_threshold": "Only if title becomes illegible after scaling.",
        "notes": "Do not turn the cover into a stacked long-scroll page."
      },
      "negative_space_strategy": "Reserve a calm field around the title and hold it with one large hero mass.",
      "counterweight_strategy": "Use the hero field or tonal block as the opposing weight.",
      "animation_intent": ["section-transition"],
      "forbidden_patterns": ["duplicate-agenda", "narrow-title-column", "dead-zone"]
    },
    {
      "slide_id": "slide-02",
      "source_slide_number": 2,
      "role": "framing",
      "archetype": "diagram-plus-insight",
      "layout_pattern": "SPLIT-60-40",
      "takeaway": {
        "en": "Replace with the opening framing claim.",
        "zh": "请替换为开场 framing 的核心判断。"
      },
      "density": "medium",
      "visual_anchor": "diagram",
      "title": {
        "text": {
          "en": "Replace With A Wide Two-Line Max Framing Title",
          "zh": "请替换为两行以内的宽标题"
        },
        "max_lines": 2,
        "preferred_width_ch": 30,
        "min_container_ratio": 0.58,
        "fallback_strategy": ["rewrite", "restack", "widen-title-region", "shrink-last"]
      },
      "body_blocks": [
        {
          "id": "frame-lede",
          "kind": "lede",
          "purpose": "frame",
          "copy": {
            "en": "Replace with the one short line that sharpens the opening argument.",
            "zh": "请替换为一句短而有判断力的 framing 文案。"
          }
        },
        {
          "id": "insight-note",
          "kind": "insight",
          "purpose": "interpret",
          "copy": {
            "en": "Replace with the insight that explains the diagram instead of repeating it.",
            "zh": "请替换为解释图示而不是复读图示的洞察。"
          }
        }
      ],
      "assets": [
        {
          "asset_id": "logic-diagram-01",
          "role": "diagram",
          "action": "redraw",
          "notes": "Main proof object for the framing page."
        }
      ],
      "proportional_spatial_map": {
        "title_region_pct": 62,
        "anchor_region_pct": 64,
        "support_region_pct": 32,
        "notes": "Main proof on the wide side, interpretation on the narrow side."
      },
      "primary_proof_device": "diagram",
      "bilingual_mode": "toggle",
      "mobile_degradation_plan": {
        "order": ["scale-slide", "trim-decoration", "tighten-spacing", "reflow-layout"],
        "reflow_threshold": "If the diagram labels no longer fit after scaling.",
        "notes": "Keep the proof object dominant even in a simplified mobile layout."
      },
      "negative_space_strategy": "Keep breathing room around the diagram rather than filling the panel with extra cards.",
      "counterweight_strategy": "Let the side insight panel hold the opposite side of the composition.",
      "animation_intent": ["focus-shift", "proof-build"],
      "forbidden_patterns": ["duplicate-agenda", "narrow-title-column", "double-proof-layer", "generic-cardification"]
    },
    {
      "slide_id": "slide-03",
      "source_slide_number": 3,
      "role": "proof",
      "archetype": "proof-strip",
      "layout_pattern": "HEADLINE-PROOF",
      "takeaway": {
        "en": "Replace with the proof page conclusion.",
        "zh": "请替换为证明页的核心结论。"
      },
      "density": "medium",
      "visual_anchor": "proof-strip",
      "title": {
        "text": {
          "en": "Replace With The Primary Proof Headline",
          "zh": "请替换为证明页主标题"
        },
        "max_lines": 2,
        "preferred_width_ch": 28,
        "min_container_ratio": 0.6,
        "fallback_strategy": ["rewrite", "restack", "widen-title-region", "shrink-last"]
      },
      "body_blocks": [
        {
          "id": "proof-lede",
          "kind": "lede",
          "purpose": "frame",
          "copy": {
            "en": "Replace with one short line that frames why the proof matters.",
            "zh": "请替换为一句交代证明意义的短句。"
          }
        },
        {
          "id": "proof-note",
          "kind": "caption",
          "purpose": "interpret",
          "copy": {
            "en": "Replace with the interpretive note that sits next to the proof strip.",
            "zh": "请替换为位于证据带旁边的解释性说明。"
          }
        }
      ],
      "assets": [
        {
          "asset_id": "proof-strip-01",
          "role": "chart",
          "action": "redraw",
          "notes": "This is the single primary proof device on the page."
        }
      ],
      "proportional_spatial_map": {
        "title_region_pct": 60,
        "anchor_region_pct": 58,
        "support_region_pct": 24,
        "notes": "Headline above, proof below, note tucked into the same composition."
      },
      "primary_proof_device": "proof-strip",
      "bilingual_mode": "toggle",
      "mobile_degradation_plan": {
        "order": ["scale-slide", "trim-decoration", "tighten-spacing", "rewrite-copy"],
        "reflow_threshold": "Only if the proof labels become unreadable.",
        "notes": "Keep one proof band; do not split into stacked cards."
      },
      "negative_space_strategy": "Use whitespace to isolate the proof band and strengthen scanability.",
      "counterweight_strategy": "Pair the headline block with the proof strip so the page still feels held.",
      "animation_intent": ["reveal-sequence", "proof-build"],
      "forbidden_patterns": ["narrow-title-column", "double-proof-layer", "floating-card-row", "dead-zone"]
    }
  ]
}
EOF

cat > "$WORKSPACE_DIR/40-rebuild/pilot-selection.md" <<'EOF'
# Pilot Selection

## Chosen Slides

| Source Slide | Archetype | Why It Is In The Pilot | What It Should Validate |
| --- | --- | --- | --- |

| slide-01 | cover | validate shell, title behavior, hero handling | cover hierarchy and navigation chrome |
| slide-02 | diagram-plus-insight | validate logic page grammar | proof versus interpretation balance |
| slide-03 | proof-strip | validate analytical page restraint | single-proof-device discipline |
| slide-04 | timeline | validate sequence handling | timeline grammar and mobile degradation |
| slide-05 | decision-close | validate ending posture | close-page density and call-to-action structure |

## Pilot Review Goal
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

cat > "$WORKSPACE_DIR/50-qa/visual-checklist.md" <<'EOF'
# Visual Checklist

Use this before calling the pilot or full deck finished.

## Hierarchy

- Can I tell title, subtitle, and body apart within two seconds?
- Is there exactly one dominant visual anchor on the slide?
- Does the title container stay wide enough in both English and Chinese?

## Composition

- Does the page still feel held together when I squint?
- Is whitespace purposeful, with a visible counterweight?
- Does the page avoid floating card rows and unsupported dead zones?

## Logic

- Is the proof device singular, or have headline, chart, and chips started repeating the same claim?
- If the page is a timeline, matrix, or framework, does the layout still preserve that logic?
- Are image and text still tightly paired?

## Bilingual

- Does language toggle preserve the same structural widths?
- Does either language cause awkward title wrapping or container jump?
- Is side-by-side bilingual used only on low-density slides?

## Playback

- Does the slide fit within one viewport without native browser scroll?
- Do deep links, keyboard navigation, and reduced motion still work?
- Does print or PDF export hold the same page boundaries?
EOF

echo "Workspace prepared at: $WORKSPACE_DIR"
echo "Source copied to: $WORKSPACE_DIR/00-source/$INPUT_BASENAME"
