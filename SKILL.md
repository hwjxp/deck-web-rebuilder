---
name: deck-web-rebuilder
description: Rebuild existing presentation decks (`.ppt`, `.pptx`, `.key`, exported `.pdf`) into faithful, interactive web presentations only after first understanding the full deck's theme, storyline, slide logic, and asset logic. Use when Codex must study a deck end-to-end before redesigning it for the web, cleaning or redrawing images and diagrams, preserving necessary text-image relationships, adding bilingual copy, navigation, deep links, animations, or PDF export.
---

# Deck Web Rebuilder

## Overview

Use this skill to turn an existing deck into a web presentation without losing its message, logical structure, or required visual relationships. Read the entire deck first, build the storyline second, and rebuild the web deck only after the deck brief, logic model, and asset register are complete.

## Non-Negotiables

- Read the whole deck before editing anything.
- Do not work slide by slide from the start. First understand the deck-level message, audience, occasion, and persuasion goal.
- Work top-down: `storyline -> layout -> content`.
- Treat image handling as data cleaning. Decide what to keep, crop, redraw, translate, or remove before restyling.
- Preserve necessary logic relationships: deck flow, page flow, text-image mapping, diagram sequence, evidence-to-claim links, comparison structure, and step order.
- Default to one source slide to one web slide. Split or merge slides only when fidelity would otherwise break, and explain the reason in `page-specs.md`.
- Optimize the source language first. Add the bilingual layer only after the source copy is clear.

## Workspace Setup

- Create a task-local workspace before analysis. Prefer `scripts/prepare_rebuild_workspace.sh <input-file> [workspace-dir]`.
- Keep these folders:
  - `00-source/` original file, exported PDF, extracted text, slide screenshots
  - `10-understanding/` deck brief and audience/context notes
  - `20-logic/` storyline and slide-role mapping
  - `30-assets/` asset register and extracted images
  - `35-strategy/` rebuild strategy and style direction
  - `40-rebuild/` page specs and generated web deck
  - `50-qa/` screenshots, comparison notes, and QA report
- Keep a stable artifact trail. Each later stage should inherit from the previous stage instead of re-reading the whole deck from scratch.

## Workflow

### 1. Normalize the Input

- Convert `.key` to a workable export before analysis. Prefer both `.pptx` and `.pdf` when available.
- For `.pptx`, extract text, notes, and images.
- Render full-slide reference images so layout, density, and image-text relationships can be read visually.
- Capture speaker notes, hidden slides, appendix slides, and hyperlinks when present.
- If local helper scripts exist, prefer these paths and fall back to equivalent tools when they do not:
  - `/Users/AlexHuang/.codex/skills/frontend-slides/scripts/extract-pptx.py`
  - `/Users/AlexHuang/.codex/skills/slides/scripts/render_slides.py`
  - `/Users/AlexHuang/.codex/skills/frontend-slides/scripts/export-pdf.sh`

### 2. Read the Whole Deck Before Editing

- Read every slide, including cover, section dividers, appendix, and notes.
- Inspect full-slide images, not just extracted text.
- Answer these questions before doing any redesign work:
  - What is the deck about?
  - Who is speaking?
  - Who is the audience?
  - What belief, action, or decision is the deck trying to move?
- Write `10-understanding/deck-brief.md`.
- Do not start HTML, CSS, or copy rewriting yet.

### 3. Model the Logic

- Write `20-logic/storyline.md`.
- Identify the deck-level arc: setup, tension, diagnosis, solution, proof, ask, close.
- For each slide, note its role: opener, context, problem, comparison, framework, process, case study, evidence, transition, appendix, or close.
- Map relationships:
  - text to image
  - image to image
  - claim to evidence
  - step to step
  - before to after
  - hierarchy and grouping
- Flag broken logic in the source deck, but do not fix it visually yet.
- If a chart or diagram carries logic, describe that logic in words before redrawing it.

### 4. Clean and Classify Assets

- Build `30-assets/asset-register.md`.
- For each asset decide `keep`, `crop`, `redraw`, `translate`, or `remove`.
- Separate:
  - photos or illustrations that should stay as images
  - product screenshots or UI captures that may need cropping or annotation
  - diagrams, flows, and architectures that should be redrawn as structured web graphics
  - charts and tables that should be recreated from data or re-encoded visually
  - decorative icons, fillers, stock UI chrome, and noise that can be removed
- Preserve only assets that support meaning, trust, brand, or evidence.
- Remove visuals whose only job was to compensate for weak layout in the source deck.

### 5. Decide the Rebuild Strategy

- Write `35-strategy/rebuild-strategy.md`.
- Judge the visual direction from the theme, occasion, speaker, and audience. Use [style-judgment.md](./references/style-judgment.md).
- Choose the fidelity mode:
  - `faithful`: preserve layout intent closely
  - `faithful-plus`: preserve structure and key relationships but improve hierarchy and spacing
  - `editorial`: preserve the story and required logic while re-composing the page more freely
- State what must not change: required images, diagram order, proof points, hierarchy, and tone.
- State what may change: spacing, typography, color system, pacing, simplified decoration, or clearer grouping.
- Do not choose visual style by trend alone. Ground it in the rhetorical job of the deck.

### 6. Write the Storyline Before Layout

- Turn the logic model into `40-rebuild/page-specs.md`.
- Work top-down:
  1. define the deck storyline
  2. define each slide's job
  3. define the target layout pattern for each slide
  4. fill in refined copy and visuals
- Keep one page spec per slide with:
  - source slide number
  - slide role
  - core takeaway
  - required assets
  - target layout
  - bilingual strategy
  - animation intent
  - fidelity notes
- Rewrite unclear source copy before adding translation.
- Prefer shorter, clearer source-language copy over literal deck transcription.

### 7. Add the Bilingual Layer

- Add bilingual content only after the source copy is solid.
- Bind translation to content blocks, not to the slide as a monolith.
- Default to a language toggle. Use side-by-side bilingual layouts only when density is low enough to stay elegant.
- Keep both languages semantically aligned. Do not make one version more persuasive or more complete than the other unless the user asks.
- When translated text becomes longer, adjust layout or hierarchy instead of shrinking text into unreadability.

### 8. Rebuild the Web Deck

- Generate the deck only after `deck-brief.md`, `storyline.md`, `asset-register.md`, and `page-specs.md` are complete.
- Preserve necessary text-image logic and diagram logic from the source.
- Rebuild diagrams as semantic HTML, SVG, or CSS when possible.
- Provide:
  - a table of contents or slide index
  - direct slide jumps
  - stable deep links such as `#slide-07`
  - keyboard navigation
  - bilingual toggle
  - PDF export path
  - reduced-motion handling
- Keep animations purposeful. Use motion to reveal logic, sequence, emphasis, or transitions, not decoration.
- Avoid slide-internal scrolling.

### 9. Run QA and Repair

- Visually inspect every generated slide.
- Check for overlap, occlusion, clipping, inconsistent spacing, dead links, and broken navigation.
- Check logic as well as layout:
  - does each slide still say the same thing?
  - do images still correspond to the right claims?
  - do arrows, order, comparison groups, and labels still make sense?
- Compare generated slides with source slide screenshots when fidelity matters.
- Write `50-qa/qa-report.md`.
- Fix issues before delivery. Do not treat QA as documentation only.
- Prefer `scripts/check_stage_gates.py <workspace-dir>` to confirm required stage artifacts exist before final delivery.

## References

- Read [artifacts.md](./references/artifacts.md) when creating or reviewing stage outputs.
- Read [style-judgment.md](./references/style-judgment.md) when deciding visual direction.
- Read [fidelity-checks.md](./references/fidelity-checks.md) when deciding what must stay logically faithful and what may change.

## Trigger Examples

- `Use $deck-web-rebuilder to turn this investor deck into a bilingual web version without losing the original logic.`
- `Use $deck-web-rebuilder to rebuild this keynote as an interactive slide site with navigation, deep links, and PDF export.`
- `Use $deck-web-rebuilder to study this PPTX first, clean up the assets, redraw the diagrams, and then make a faithful web deck.`
