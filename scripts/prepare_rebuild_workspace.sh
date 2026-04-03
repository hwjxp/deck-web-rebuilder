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
mkdir -p "$WORKSPACE_DIR"/30-assets/slices
mkdir -p "$WORKSPACE_DIR"/35-strategy
mkdir -p "$WORKSPACE_DIR"/40-rebuild
mkdir -p "$WORKSPACE_DIR"/40-rebuild/deck
mkdir -p "$WORKSPACE_DIR"/50-qa

cp -f "$INPUT_ABS" "$WORKSPACE_DIR/00-source/$INPUT_BASENAME"

cat > "$WORKSPACE_DIR/00-source/input-profile.md" <<'EOF'
# Input Profile

## Source Files

## Input Mode

## Source-Of-Truth Order

## Normalization Plan

## Parsing Risks

## Visual Parsing Role
EOF

cat > "$WORKSPACE_DIR/00-source/visual-regions.json" <<'EOF'
{
  "source_id": "replace-with-source-id",
  "slides": [
    {
      "slide_id": "slide-01",
      "regions": [
        {
          "region_id": "slide-01-headline",
          "type": "headline-band",
          "bbox": [0.08, 0.08, 0.82, 0.18],
          "group_id": "headline-group",
          "z_order_hint": 10,
          "confidence": "replace-me",
          "slice_path": "",
          "relation_type": "none",
          "primitive_count": 0,
          "label_anchor_strategy": "none",
          "must_show_full_frame": false,
          "crop_tolerance": "none",
          "alignment_group_id": ""
        }
      ]
    }
  ]
}
EOF

cat > "$WORKSPACE_DIR/00-source/composition-graph.json" <<'EOF'
{
  "source_id": "replace-with-source-id",
  "groups": [
    {
      "group_id": "slide-01-cover-shell",
      "source_slide": 1,
      "member_region_ids": ["slide-01-headline"],
      "group_intent": "layout-scaffold",
      "evidence_source": "both",
      "confidence": "medium",
      "rebuild_policy": "convert-to-css-layout",
      "notes": "Template example: a cover shell can be a layout scaffold rather than a semantic object."
    }
  ]
}
EOF

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

cat > "$WORKSPACE_DIR/20-logic/visual-structure-map.md" <<'EOF'
# Visual Structure Map

## Slide 1 - cover

Visual structures detected:
- layered composition at full frame: hero field plus title band

Rebuild decisions:
- layered composition -> live-text-layer
- reason: keep the title searchable and bilingual while preserving the layered shell

## Slide 2 - framing

Visual structures detected:
- semantic composite at center-left: replace with the actual diagram, overlap, or scaffold

Rebuild decisions:
- semantic composite -> redraw-as-SVG
- reason: preserve the diagram grammar as one unit instead of exploding it into unrelated cards

## Slide 3 - proof

Visual structures detected:
- transparent-border table at lower field: replace with the actual alignment scaffold or table decision

Rebuild decisions:
- transparent-border table -> css-layout
- reason: alignment scaffolds should collapse into grid or flex, not become visible tables
EOF

cat > "$WORKSPACE_DIR/20-logic/authoring-intent.md" <<'EOF'
# Authoring Intent

## Structural Signals

- note repeated use of semantic composite diagrams built from grouped shapes
- note repeated layout scaffold patterns such as transparent-border tables or spacer groups
- note which groups are content-bearing versus presentation chrome

## Table Intent

- list pseudo-table cases used only for alignment
- list semantic table cases that must remain audience-visible tables

## Connector And Layering Intent

- note connector arrows whose direction carries sequence or causality
- note z-order or reading-surface patterns that must remain layered in the web rebuild

## Rebuild Implications

- convert scaffolds into CSS layout rules
- preserve semantic composites as one proof object
- rebuild uncertain structures conservatively and record the confidence
EOF

cat > "$WORKSPACE_DIR/20-logic/confidence-report.md" <<'EOF'
# Confidence Report

## High Confidence

## Medium Confidence

## Low Confidence

## Follow-Up Actions
EOF

cat > "$WORKSPACE_DIR/30-assets/asset-register.md" <<'EOF'
# Asset Register

| Asset ID | Source Slide | Asset Type | Semantic Role | Action | Reason | Translation Needed | Redraw Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
EOF

cat > "$WORKSPACE_DIR/30-assets/asset-lineage.json" <<'EOF'
{
  "assets": [
    {
      "asset_id": "replace-me",
      "source_slide": 1,
      "source_region_ids": ["slide-01-headline"],
      "original_file_path": "00-source/replace-me",
      "derived_slice_path": "30-assets/slices/replace-me.png",
      "semantic_role": "replace-me",
      "chosen_action": "keep",
      "redraw": false,
      "confidence": "replace-me",
      "fit_policy": "contain",
      "must_show_full_frame": true,
      "visible_area_min_pct": 100,
      "focal_region_hint": ""
    }
  ]
}
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
- title band:
- body measure:
- bilingual fallback order:

## 5. Grid And Page Chrome

- grid:
- outer margins:
  - mobile: `16px`
  - tablet: `24px`
  - desktop: `32px`
- content max width: `1280px`
- navigation:
- language toggle:
- deep links:

## 6. Media Policy

- default raster fit:
- diagram fit:
- board / contact-sheet fit:
- allow safe crop only when:
- gallery uniform height default:

## 7. Negative Space And Mobile

- blank ratio:
- counterweight rule:
- mobile degradation order:

## 8. Do / Don't

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
      "min_title_container_ratio": 0.6,
      "fallback_order": ["rewrite", "restack", "widen-title-region", "shrink-last"]
    }
  },
  "title_band": {
    "default_posture": "single-line",
    "prefer_single_line": true,
    "min_width_ratio": 0.6,
    "min_height": "18%",
    "alignment": "left"
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
    "columns": 8,
    "gutter": "1.6cqi",
    "outer_margin": {
      "mobile": "16px",
      "tablet": "24px",
      "desktop": "32px"
    },
    "content_max_width": "1280px"
  },
  "page_chrome": {
    "navigation": "top-right controls with previous and next buttons",
    "counter": "persistent current / total slide counter",
    "language_toggle": "sticky visible toggle in chrome",
    "deep_links": "slide ids use #slide-NN"
  },
  "media_policy": {
    "default_raster_fit": "contain",
    "diagram_fit": "redraw",
    "board_fit": "contain",
    "allow_safe_crop_only_with_justification": true,
    "gallery_uniform_height_default": "strict"
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

cat > "$WORKSPACE_DIR/35-strategy/layout-rationale.md" <<'EOF'
# Layout Rationale

## Pattern Families

- explain why each major slide family uses its chosen layout pattern

## Rhythm

- explain how the deck alternates dense and spacious slides

## Title Discipline

- note which slides preserve source one-line posture and which may use two lines

## Media Discipline

- note which slides require strict media alignment or full-frame containment

## Anchor Strategy

- explain the dominant visual anchor strategy across the pilot set
EOF

cat > "$WORKSPACE_DIR/35-strategy/layout-plan.json" <<'EOF'
{
  "slides": [
    {
      "slide_id": "slide-01",
      "layout_pattern": "HERO-FULL",
      "slide_role": "cover",
      "visual_intent": "calm hero field with one-line opening claim",
      "dominant_reading_path": "hero-to-note",
      "dominant_visual_anchor": "hero-image",
      "zone_skeleton": [
        {
          "zone_name": "HERO-ZONE",
          "zone_purpose": "background field",
          "content_rule": "one hero field only"
        },
        {
          "zone_name": "TITLE-ZONE",
          "zone_purpose": "headline band",
          "content_rule": "one headline plus optional subtitle"
        }
      ],
      "title_band_pct": 22,
      "anchor_region_pct": 58,
      "support_region_pct": 8,
      "whitespace_reserve_pct": 12,
      "max_body_blocks": 2,
      "copy_budget_en": 40,
      "copy_budget_zh": 36,
      "group_preservation_rules": [
        {
          "group_id": "slide-01-headline-shell",
          "policy": "convert-to-css-layout",
          "reason": "Treat the cover shell as layout, not a literal exported box."
        }
      ],
      "diagram_redraw_policy": "n/a",
      "layout_confidence": "medium"
    },
    {
      "slide_id": "slide-02",
      "layout_pattern": "SPLIT-60-40",
      "slide_role": "framing",
      "visual_intent": "proof object on the wide side, interpretation on the rail",
      "dominant_reading_path": "left-to-right",
      "dominant_visual_anchor": "diagram",
      "zone_skeleton": [
        {
          "zone_name": "VISUAL-ZONE",
          "zone_purpose": "proof field",
          "content_rule": "one dominant proof object"
        },
        {
          "zone_name": "TITLE-ZONE",
          "zone_purpose": "headline band",
          "content_rule": "short title only"
        },
        {
          "zone_name": "INSIGHT-ZONE",
          "zone_purpose": "interpretation rail",
          "content_rule": "2-4 lines of explanation"
        }
      ],
      "title_band_pct": 18,
      "anchor_region_pct": 50,
      "support_region_pct": 22,
      "whitespace_reserve_pct": 10,
      "max_body_blocks": 3,
      "copy_budget_en": 60,
      "copy_budget_zh": 56,
      "group_preservation_rules": [
        {
          "group_id": "replace-me",
          "policy": "redraw-as-svg",
          "reason": "Preserve semantic-composite diagram logic."
        }
      ],
      "diagram_redraw_policy": "redraw-as-svg",
      "layout_confidence": "medium"
    },
    {
      "slide_id": "slide-03",
      "layout_pattern": "HEADLINE-PROOF",
      "slide_role": "proof",
      "visual_intent": "headline up top, one proof object below",
      "dominant_reading_path": "title-to-proof",
      "dominant_visual_anchor": "proof-strip",
      "zone_skeleton": [
        {
          "zone_name": "TITLE-ZONE",
          "zone_purpose": "claim band",
          "content_rule": "one claim only"
        },
        {
          "zone_name": "EVIDENCE-ZONE",
          "zone_purpose": "proof object",
          "content_rule": "one primary proof object"
        },
        {
          "zone_name": "ANNOTATION-ZONE",
          "zone_purpose": "support note",
          "content_rule": "short interpretation only"
        }
      ],
      "title_band_pct": 28,
      "anchor_region_pct": 50,
      "support_region_pct": 14,
      "whitespace_reserve_pct": 8,
      "max_body_blocks": 2,
      "copy_budget_en": 42,
      "copy_budget_zh": 40,
      "group_preservation_rules": [
        {
          "group_id": "replace-me",
          "policy": "convert-to-css-layout",
          "reason": "Collapse alignment scaffolds instead of showing them literally."
        }
      ],
      "diagram_redraw_policy": "n/a",
      "layout_confidence": "medium"
    }
  ]
}
EOF

cat > "$WORKSPACE_DIR/40-rebuild/layout-spine.md" <<'EOF'
# Layout Spine

slide-01 | HERO-FULL      | cover    | calm hero field with one-line opening claim
slide-02 | SPLIT-60-40    | framing  | proof object on the wide side, interpretation on the rail
slide-03 | HEADLINE-PROOF | proof    | headline above one primary proof object
EOF

cat > "$WORKSPACE_DIR/40-rebuild/page-specs.md" <<'EOF'
# Page Specs

Use `references/layout-patterns.md`, `references/layout-first-method.md`, `references/page-archetypes.md`, and `references/typography-rules.md`. Do not invent new layout vocabulary. Write zones first, then fill copy.

## Deck-Level Settings

- Input Mode:
- Default Source Of Truth:

## slide-01

- Source Slide:
- Input Mode:
- Destination Slide ID: `slide-01`
- Slide Role:
- Archetype:
- Layout Pattern:
- Zone Skeleton:
- Core Takeaway:
- Source Of Truth:
- Confidence Level:
- Dominant Reading Path:
- Layout Hypothesis:
- Title Posture:
- Source Title Line-Count Strategy:
- Required Copy Blocks:
- Required Assets:
- Proportional Spatial Map:
- Whitespace Reserve:
- Copy Budget:
- Dominant Visual Anchor:
- Group Preservation Rules:
- Primary Proof Device:
- Diagram Redraw Policy:
- Diagram Contract:
- Media Layout Contract:
- Bilingual Treatment:
- Mobile Degradation Plan:
- Animation Intent:
- Render Audit Targets:
- Forbidden Patterns:
- Fidelity Notes:

## slide-02

- Source Slide:
- Input Mode:
- Destination Slide ID: `slide-02`
- Slide Role:
- Archetype:
- Layout Pattern:
- Zone Skeleton:
- Core Takeaway:
- Source Of Truth:
- Confidence Level:
- Dominant Reading Path:
- Layout Hypothesis:
- Title Posture:
- Source Title Line-Count Strategy:
- Required Copy Blocks:
- Required Assets:
- Proportional Spatial Map:
- Whitespace Reserve:
- Copy Budget:
- Dominant Visual Anchor:
- Group Preservation Rules:
- Primary Proof Device:
- Diagram Redraw Policy:
- Diagram Contract:
- Media Layout Contract:
- Bilingual Treatment:
- Mobile Degradation Plan:
- Animation Intent:
- Render Audit Targets:
- Forbidden Patterns:
- Fidelity Notes:

## slide-03

- Source Slide:
- Input Mode:
- Destination Slide ID: `slide-03`
- Slide Role:
- Archetype:
- Layout Pattern:
- Zone Skeleton:
- Core Takeaway:
- Source Of Truth:
- Confidence Level:
- Dominant Reading Path:
- Layout Hypothesis:
- Title Posture:
- Source Title Line-Count Strategy:
- Required Copy Blocks:
- Required Assets:
- Proportional Spatial Map:
- Whitespace Reserve:
- Copy Budget:
- Dominant Visual Anchor:
- Group Preservation Rules:
- Primary Proof Device:
- Diagram Redraw Policy:
- Diagram Contract:
- Media Layout Contract:
- Bilingual Treatment:
- Mobile Degradation Plan:
- Animation Intent:
- Render Audit Targets:
- Forbidden Patterns:
- Fidelity Notes:
EOF

cat > "$WORKSPACE_DIR/40-rebuild/page-specs.json" <<'EOF'
{
  "deck_id": "replace-with-deck-id",
  "source_file": "00-source/replace-with-source-file",
  "input_mode": "polish",
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
      "confidence_level": "high",
      "source_of_truth": ["source-object", "visual-render"],
      "title": {
        "text": {
          "en": "Replace With The Final Cover Title",
          "zh": "请替换为最终封面标题"
        },
        "posture": "single-line",
        "prefer_no_wrap": true,
        "max_lines": 1,
        "source_line_count": 1,
        "line_count_strategy": "preserve-source",
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
          "fit_policy": "contain",
          "must_show_full_frame": true,
          "visible_area_min_pct": 100,
          "notes": "Replace with the chosen hero asset or tonal field."
        }
      ],
      "layout_plan": {
        "dominant_reading_path": "hero-to-note",
        "layout_hypothesis": "Keep the cover as a calm hero field with one dominant title band and no extra agenda row.",
        "zone_skeleton": [
          {
            "zone_name": "HERO-ZONE",
            "zone_purpose": "background field",
            "content_rule": "one hero field only"
          },
          {
            "zone_name": "TITLE-ZONE",
            "zone_purpose": "headline band",
            "content_rule": "one headline plus optional subtitle"
          }
        ],
        "title_band_pct": 22,
        "anchor_region_pct": 58,
        "support_region_pct": 8,
        "whitespace_reserve_pct": 12,
        "max_body_blocks": 2,
        "copy_budget_en": 40,
        "copy_budget_zh": 36,
        "group_preservation_rules": [
          {
            "group_id": "slide-01-headline-shell",
            "policy": "convert-to-css-layout",
            "reason": "Use CSS layout for the cover shell instead of a literal exported box."
          }
        ],
        "diagram_redraw_policy": "n/a",
        "layout_confidence": "medium"
      },
      "proportional_spatial_map": {
        "title_region_pct": 22,
        "anchor_region_pct": 58,
        "support_region_pct": 8,
        "notes": "Cover shell only; no extra agenda row."
      },
      "primary_proof_device": "hero-image",
      "diagram_contract": {
        "relation_type": "none",
        "primitive_count": 0,
        "must_preserve_overlap": false,
        "label_anchor_strategy": "none"
      },
      "media_layout_contract": {
        "default_fit_policy": "contain",
        "uniform_media_height": "n/a",
        "allow_occlusion": false,
        "clip_tolerance": "none"
      },
      "bilingual_mode": "toggle",
      "mobile_degradation_plan": {
        "order": ["scale-slide", "trim-decoration", "tighten-spacing", "rewrite-copy"],
        "reflow_threshold": "Only if title becomes illegible after scaling.",
        "notes": "Do not turn the cover into a stacked long-scroll page."
      },
      "negative_space_strategy": "Reserve a calm field around the title and hold it with one large hero mass.",
      "counterweight_strategy": "Use the hero field or tonal block as the opposing weight.",
      "animation_intent": ["section-transition"],
      "render_audit_targets": {
        "verify_title_lines": true,
        "verify_overlap": true,
        "verify_clipping": true,
        "verify_occlusion": true,
        "verify_media_alignment": false,
        "verify_diagram_semantics": false
      },
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
      "confidence_level": "medium",
      "source_of_truth": ["visual-render", "ocr", "inferred"],
      "title": {
        "text": {
          "en": "Replace With A Wide Two-Line Max Framing Title",
          "zh": "请替换为两行以内的宽标题"
        },
        "posture": "balanced-two-line",
        "prefer_no_wrap": false,
        "max_lines": 2,
        "source_line_count": 2,
        "line_count_strategy": "fit-deck-system",
        "wrap_justification": "Allow one additional line only if the reframed title cannot stay clear at deck scale.",
        "preferred_width_ch": 30,
        "min_container_ratio": 0.62,
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
          "fit_policy": "redraw",
          "must_show_full_frame": true,
          "visible_area_min_pct": 100,
          "notes": "Main proof object for the framing page."
        }
      ],
      "layout_plan": {
        "dominant_reading_path": "left-to-right",
        "layout_hypothesis": "Use a wide proof field plus a note rail so the argument reads from diagram to interpretation.",
        "zone_skeleton": [
          {
            "zone_name": "VISUAL-ZONE",
            "zone_purpose": "proof field",
            "content_rule": "one dominant proof object"
          },
          {
            "zone_name": "TITLE-ZONE",
            "zone_purpose": "headline band",
            "content_rule": "short title only"
          },
          {
            "zone_name": "INSIGHT-ZONE",
            "zone_purpose": "interpretation rail",
            "content_rule": "2-4 lines of explanation"
          }
        ],
        "title_band_pct": 18,
        "anchor_region_pct": 50,
        "support_region_pct": 22,
        "whitespace_reserve_pct": 10,
        "max_body_blocks": 3,
        "copy_budget_en": 60,
        "copy_budget_zh": 56,
        "group_preservation_rules": [
          {
            "group_id": "replace-me",
            "policy": "redraw-as-svg",
            "reason": "Keep semantic-composite diagram logic as one unit."
          }
        ],
      "diagram_redraw_policy": "redraw-as-svg",
        "layout_confidence": "medium"
      },
      "proportional_spatial_map": {
        "title_region_pct": 18,
        "anchor_region_pct": 50,
        "support_region_pct": 22,
        "notes": "Main proof on the wide side, interpretation on the narrow side."
      },
      "primary_proof_device": "diagram",
      "diagram_contract": {
        "relation_type": "overlap",
        "primitive_count": 2,
        "must_preserve_overlap": true,
        "label_anchor_strategy": "outside-with-leader"
      },
      "media_layout_contract": {
        "default_fit_policy": "redraw",
        "uniform_media_height": "n/a",
        "allow_occlusion": false,
        "clip_tolerance": "none"
      },
      "bilingual_mode": "toggle",
      "mobile_degradation_plan": {
        "order": ["scale-slide", "trim-decoration", "tighten-spacing", "reflow-layout"],
        "reflow_threshold": "If the diagram labels no longer fit after scaling.",
        "notes": "Keep the proof object dominant even in a simplified mobile layout."
      },
      "negative_space_strategy": "Keep breathing room around the diagram rather than filling the panel with extra cards.",
      "counterweight_strategy": "Let the side insight panel hold the opposite side of the composition.",
      "animation_intent": ["focus-shift", "proof-build"],
      "render_audit_targets": {
        "verify_title_lines": true,
        "verify_overlap": true,
        "verify_clipping": true,
        "verify_occlusion": true,
        "verify_media_alignment": false,
        "verify_diagram_semantics": true
      },
      "forbidden_patterns": ["duplicate-agenda", "narrow-title-column", "double-proof-layer", "generic-cardification", "diagram-semantic-drift"]
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
      "confidence_level": "high",
      "source_of_truth": ["source-object", "visual-render"],
      "title": {
        "text": {
          "en": "Replace With The Primary Proof Headline",
          "zh": "请替换为证明页主标题"
        },
        "posture": "single-line",
        "prefer_no_wrap": true,
        "max_lines": 1,
        "source_line_count": 1,
        "line_count_strategy": "preserve-source",
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
          "fit_policy": "redraw",
          "must_show_full_frame": true,
          "visible_area_min_pct": 100,
          "notes": "This is the single primary proof device on the page."
        }
      ],
      "layout_plan": {
        "dominant_reading_path": "title-to-proof",
        "layout_hypothesis": "Use a headline band over one primary proof device and keep support notes secondary.",
        "zone_skeleton": [
          {
            "zone_name": "TITLE-ZONE",
            "zone_purpose": "claim band",
            "content_rule": "one claim only"
          },
          {
            "zone_name": "EVIDENCE-ZONE",
            "zone_purpose": "proof object",
            "content_rule": "one primary proof object"
          },
          {
            "zone_name": "ANNOTATION-ZONE",
            "zone_purpose": "support note",
            "content_rule": "short interpretation only"
          }
        ],
        "title_band_pct": 28,
        "anchor_region_pct": 50,
        "support_region_pct": 14,
        "whitespace_reserve_pct": 8,
        "max_body_blocks": 2,
        "copy_budget_en": 42,
        "copy_budget_zh": 40,
        "group_preservation_rules": [
          {
            "group_id": "replace-me",
            "policy": "convert-to-css-layout",
            "reason": "Collapse alignment scaffolds instead of showing them literally."
          }
        ],
        "diagram_redraw_policy": "n/a",
        "layout_confidence": "medium"
      },
      "proportional_spatial_map": {
        "title_region_pct": 28,
        "anchor_region_pct": 50,
        "support_region_pct": 14,
        "notes": "Headline above, proof below, note tucked into the same composition."
      },
      "primary_proof_device": "proof-strip",
      "diagram_contract": {
        "relation_type": "none",
        "primitive_count": 0,
        "must_preserve_overlap": false,
        "label_anchor_strategy": "none"
      },
      "media_layout_contract": {
        "default_fit_policy": "redraw",
        "uniform_media_height": "strict",
        "allow_occlusion": false,
        "clip_tolerance": "none"
      },
      "bilingual_mode": "toggle",
      "mobile_degradation_plan": {
        "order": ["scale-slide", "trim-decoration", "tighten-spacing", "rewrite-copy"],
        "reflow_threshold": "Only if the proof labels become unreadable.",
        "notes": "Keep one proof band; do not split into stacked cards."
      },
      "negative_space_strategy": "Use whitespace to isolate the proof band and strengthen scanability.",
      "counterweight_strategy": "Pair the headline block with the proof strip so the page still feels held.",
      "animation_intent": ["reveal-sequence", "proof-build"],
      "render_audit_targets": {
        "verify_title_lines": true,
        "verify_overlap": true,
        "verify_clipping": true,
        "verify_occlusion": true,
        "verify_media_alignment": true,
        "verify_diagram_semantics": false
      },
      "forbidden_patterns": ["narrow-title-column", "double-proof-layer", "floating-card-row", "dead-zone", "media-height-drift"]
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

- Are there any awkward or unnecessary title line breaks?
- Can I tell title, subtitle, and body apart within two seconds?
- Is there exactly one dominant visual anchor on the slide?
- Does the title container stay wide enough in both English and Chinese?

## Composition

- Does the page still feel held together when I squint?
- Is whitespace purposeful, with a visible counterweight?
- Does the page avoid floating card rows and unsupported dead zones?
- Are any images clipping meaningful content at the edges or bottom?
- If there is a media strip or grid, are peer media windows aligned in height?

## Logic

- Is the proof device singular, or have headline, chart, and chips started repeating the same claim?
- If the page is a timeline, matrix, or framework, does the layout still preserve that logic?
- Are image and text still tightly paired?
- If the source used overlap, matrix, or lineup logic, did the rebuild preserve that same grammar?

## Bilingual

- Does language toggle preserve the same structural widths?
- Does either language cause awkward title wrapping or container jump?
- Is side-by-side bilingual used only on low-density slides?

## Playback

- Does the slide fit within one viewport without native browser scroll?
- Do deep links, keyboard navigation, and reduced motion still work?
- Does print or PDF export hold the same page boundaries?
EOF

cat > "$WORKSPACE_DIR/50-qa/render-audit.json" <<'EOF'
{
  "slides": [
    {
      "slide_id": "slide-01",
      "checked_languages": ["zh", "en"],
      "title_line_counts": {
        "zh": 1,
        "en": 1
      },
      "title_wrap_status": "pass",
      "overlap_status": "pass",
      "clipping_status": "pass",
      "occlusion_status": "pass",
      "media_uniformity_status": "n/a",
      "diagram_semantics_status": "n/a",
      "notes": ""
    },
    {
      "slide_id": "slide-02",
      "checked_languages": ["zh", "en"],
      "title_line_counts": {
        "zh": 0,
        "en": 0
      },
      "title_wrap_status": "n/a",
      "overlap_status": "n/a",
      "clipping_status": "n/a",
      "occlusion_status": "n/a",
      "media_uniformity_status": "n/a",
      "diagram_semantics_status": "n/a",
      "notes": ""
    },
    {
      "slide_id": "slide-03",
      "checked_languages": ["zh", "en"],
      "title_line_counts": {
        "zh": 0,
        "en": 0
      },
      "title_wrap_status": "n/a",
      "overlap_status": "n/a",
      "clipping_status": "n/a",
      "occlusion_status": "n/a",
      "media_uniformity_status": "n/a",
      "diagram_semantics_status": "n/a",
      "notes": ""
    }
  ]
}
EOF

echo "Workspace prepared at: $WORKSPACE_DIR"
echo "Source copied to: $WORKSPACE_DIR/00-source/$INPUT_BASENAME"
