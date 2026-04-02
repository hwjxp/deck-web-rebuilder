---
name: deck-web-rebuilder
description: Rebuild existing presentation decks (`.ppt`, `.pptx`, `.key`, exported `.pdf`) into faithful, interactive, viewport-bounded web presentations only after first understanding the full deck's theme, storyline, slide logic, and asset logic. Use when Codex must study a deck end-to-end before redesigning it for the web while preserving slide boundaries, logical flow, text-image relationships, navigation, bilingual copy, animations, or PDF export.
---

# Deck Web Rebuilder

## Overview

Use this skill to turn slide-like source material into a web presentation without losing its message, logical structure, or required visual relationships. The target output is a web-based presentation, not a conventional landing page, blog, or long scrolly document. Work like a human editor-designer: first understand the whole deck, then model the logic, then decide the page system, and only then rebuild. Regardless of input type, create a visual parse and a stable deck intermediate representation before redesign begins.

This skill supports three execution modes:

- `polish`: the source deck is already written; improve the design and rebuild it for the web without breaking its logic
- `reverse-engineer`: the source is a PDF, screenshot set, or visually complete artifact; infer structure from the rendered pages and rebuild it faithfully
- `editorial-compose`: the source is loose copy and assets; reorganize the material into a coherent deck before rebuilding

When internal reference decks are available, study them before choosing a visual direction. For non-trivial decks, build a five-slide pilot before scaling to the full rebuild.

## Non-Negotiables

- Read the whole deck before editing anything.
- Do not work slide by slide from the start. First understand the deck-level message, audience, occasion, and persuasion goal.
- Detect the input mode first: `polish`, `reverse-engineer`, or `editorial-compose`.
- Work top-down: `storyline -> layout -> content`.
- Build a visual parse even when source object data exists. Rendered pages are the ground truth for composition, grouping, and emphasis.
- Keep an explicit source-of-truth order: source object layer > rendered slide/page > OCR text > inference.
- Track uncertainty. If diagram logic, grouping, or text-image mapping is only partly inferred, mark the confidence before redesigning.
- Treat the output as a browser-based slide deck, not a normal web page. Preserve slide cadence, frame boundaries, and presenter-controlled reading order.
- Keep each slide as a strict, viewport-bounded frame. Default to a 16:9 container that fits within the active viewport without native browser scrolling.
- Commit to a clear visual direction before implementation. Do not drift into a safe but generic deck-to-web template.
- If the user provides internal reference decks, study them deck-wide before deciding style. Learn the page system, not just isolated visual tricks.
- Treat image handling as data cleaning. Decide what to keep, crop, redraw, translate, or remove before restyling.
- Preserve necessary logic relationships: deck flow, page flow, text-image mapping, diagram sequence, evidence-to-claim links, comparison structure, and step order.
- Preserve or reconstruct build order when the source implies sequential reveals. Do not flatten a staged argument into one simultaneous dump.
- Keep asset lineage. Every extracted or sliced asset should stay traceable to a source page and region.
- Reconstruct slide layouts proportionally. Prefer CSS Grid or Flexbox ratios, named zones, and percentage or `fr` mappings over fixed-pixel absolute placement for major content blocks.
- Scale type, padding, and gaps with the slide container. Prefer container-query units or other slide-relative units so typography shrinks and grows with the canvas instead of drifting independently.
- On small screens, degrade like a presentation. First scale the whole slide, then trim decoration, and only reflow as a last resort while still keeping one slide inside one viewport.
- Default to one source slide to one web slide. Split or merge slides only when fidelity would otherwise break, and explain the reason in `page-specs.md`.
- Optimize the source language first. Add the bilingual layer only after the source copy is clear.
- Reject visually anonymous output. The rebuilt deck should show deliberate composition, hierarchy, spacing rhythm, and typography instead of generic cardification.
- Do not expand to the whole deck immediately. Build a five-slide representative pilot first unless the user explicitly asks to skip this gate.
- Default to a slide-spanning headline band. Most body slides should prefer a single-line title if it fits naturally; do not force wrapping just to manufacture drama.
- Do not force narrow title columns just to manufacture drama. Title breaks must feel intentional in both English and Chinese, and should survive language toggle without awkward wrapping.
- Do not repeat orientation devices unnecessarily. If the cover, chrome, or navigation already explains the deck structure, a second full agenda page must add a new framing job or be removed.
- On analytical pages, pick one primary proof device. If a diagram already carries the numbers and relationship, supporting text should interpret it, not restate it.
- Leave only purposeful whitespace. Empty area should strengthen hierarchy, asymmetry, or pacing, not expose that the layout has no second anchor.
- Avoid slide-internal scrolling and browser-level vertical scroll during playback. If a slide does not fit, redesign or degrade it; do not let it leak into a document model.

## Workspace Setup

- Create a task-local workspace before analysis. Prefer `scripts/prepare_rebuild_workspace.sh <input-file> [workspace-dir]`.
- Keep these folders:
  - `00-source/` original file, exported PDF, extracted text, slide screenshots, input profile, visual region map
  - `10-understanding/` deck brief and audience/context notes
  - `12-reference-study/` notes on any reference decks and extracted layout/system rules
  - `20-logic/` storyline, slide-role mapping, and confidence report
  - `30-assets/` asset register, lineage, extracted images, and sliced regions
  - `35-strategy/` rebuild strategy and style direction
  - `40-rebuild/` page specs and generated web deck
  - `50-qa/` screenshots, comparison notes, and QA report
- Keep a stable artifact trail. Each later stage should inherit from the previous stage instead of re-reading the whole deck from scratch.

## Workflow

### 1. Profile and Normalize the Input

- Determine the input mode before doing any design work:
  - `polish` for an existing `.ppt`, `.pptx`, or `.key` deck whose logic mostly stands
  - `reverse-engineer` for exported `.pdf`, screenshots, or visually complete artifacts without reliable object structure
  - `editorial-compose` for loose copy and assets that still need deck structure
- Write `00-source/input-profile.md`.
- In that file, record:
  - source file types
  - chosen input mode
  - likely source-of-truth order
  - expected parsing risks
  - normalization plan
- Convert `.key` to a workable export before analysis. Prefer both `.pptx` and `.pdf` when available.
- For `.pptx`, extract text, notes, images, and object-layer clues such as grouping, coordinates, and hyperlinks when possible.
- For `.pdf` or screenshots, treat the rendered page as the primary composition source and recover text or objects secondarily.
- For loose materials, inventory the copy and assets first, then prepare synthetic slide candidates before styling.
- Render full-slide reference images so layout, density, and image-text relationships can be read visually.
- Capture speaker notes, hidden slides, appendix slides, and hyperlinks when present.
- If local helper scripts exist, prefer these paths and fall back to equivalent tools when they do not:
  - `/Users/AlexHuang/.codex/skills/frontend-slides/scripts/extract-pptx.py`
  - `/Users/AlexHuang/.codex/skills/slides/scripts/render_slides.py`
  - `/Users/AlexHuang/.codex/skills/frontend-slides/scripts/export-pdf.sh`

### 1A. Study Reference Decks When Provided

- If the user provides internal reference decks, render and review them visually before styling the target deck.
- Write `12-reference-study/reference-deck-notes.md`.
- Write `12-reference-study/reference-deck-notes.yaml` using the schema in [reference-deck-learning.md](./references/reference-deck-learning.md).
- Extract at least:
  - deck shell rules
  - cover and section-divider rules
  - analytical page grammar
  - image-led page grammar
  - closing-page grammar
  - text-image contract
  - color and accent restraint
  - repeated modules worth borrowing
  - anti-patterns to avoid
- Learn systems, not screenshots. Reuse the discipline of the reference decks without blindly copying their brand-specific visuals.
- Use [reference-deck-learning.md](./references/reference-deck-learning.md) when turning reference decks into reusable rules.
- If the user explicitly asks for improvement beyond internal references, study a small set of current external design sources and write the transferable lessons into the strategy or skill notes instead of vaguely saying you "learned from the web."

### 1B. Build a Visual Parse Before Editing

- Render every slide or source page into a full-frame visual reference.
- Write `00-source/visual-regions.json`.
- For each page, segment and classify at least:
  - headline band
  - main proof zone
  - support text zone
  - image blocks
  - diagrams or charts
  - decorative or removable chrome
  - likely navigation or meta elements
- If the source is PDF- or screenshot-only, slice reusable visual regions into `30-assets/slices/` and record them in `30-assets/asset-lineage.json`.
- Record likely grouping, overlap, z-order, and dominant reading path from the rendered page, not only from extracted text.
- Note uncertain regions or relationships instead of pretending the parse is complete. Low-confidence diagrams or chart regions must be called out before redesign begins.
- Use [visual-parsing-playbook.md](./references/visual-parsing-playbook.md) when deciding how to combine object extraction, OCR, layout analysis, and slicing.

### 2. Read the Whole Deck Before Editing

- Read every slide, including cover, section dividers, appendix, and notes.
- Inspect full-slide images and the visual region map, not just extracted text.
- Answer these questions before doing any redesign work:
  - What is the deck about?
  - Who is speaking?
  - Who is the audience?
  - What belief, action, or decision is the deck trying to move?
- Write `10-understanding/deck-brief.md`.
- Do not start HTML, CSS, or copy rewriting yet.

### 3. Model the Logic

- Write `20-logic/storyline.md`.
- Write `20-logic/confidence-report.md`.
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
- For each critical relationship, record a confidence level:
  - `high` when confirmed by source structure and rendered page
  - `medium` when confirmed visually but not structurally
  - `low` when inferred from partial evidence
- If a slide's main proof device is `low` confidence, keep the initial rebuild conservative or investigate further before stylizing it.

### 4. Clean and Classify Assets

- Build `30-assets/asset-register.md`.
- Build `30-assets/asset-lineage.json`.
- For each asset decide `keep`, `crop`, `redraw`, `translate`, or `remove`.
- Preserve asset lineage for every extracted visual: source page, region ID, derived file path, semantic role, chosen action, and confidence.
- Separate:
  - photos or illustrations that should stay as images
  - product screenshots or UI captures that may need cropping or annotation
  - diagrams, flows, and architectures that should be redrawn as structured web graphics
  - charts and tables that should be recreated from data or re-encoded visually
  - decorative icons, fillers, stock UI chrome, and noise that can be removed
- Distinguish implementation targets:
  - simple vector-like marks, logos, and icons for SVG or CSS recreation
  - raster images for `<img>`
  - full-bleed ambient fields for `background-image`
- Preserve only assets that support meaning, trust, brand, or evidence.
- Remove visuals whose only job was to compensate for weak layout in the source deck.

### 5. Decide the Rebuild Strategy

- Write `35-strategy/rebuild-strategy.md`.
- Copy [deck-design-system-template.md](./references/deck-design-system-template.md) into `35-strategy/deck-design-system.md`, then replace the placeholders with deck-specific decisions. Do not start from a blank page.
- Mirror the same rules into `35-strategy/deck-design-system.json` and validate it against `schemas/deck-design-system.schema.json`.
- In `deck-design-system.md`, explicitly define the slide boundary model, aspect ratio policy, scaling model, permitted sizing units, and mobile degradation order for the deck.
- Explicitly define the title-band system for the deck: height, alignment, preferred title posture, no-wrap preference, and when a two-line title is allowed.
- Judge the visual direction from the theme, occasion, speaker, and audience. Use [style-judgment.md](./references/style-judgment.md).
- If reference decks were provided, also ground the strategy in `12-reference-study/reference-deck-notes.md`.
- Choose the fidelity mode:
  - `faithful`: preserve layout intent closely
  - `faithful-plus`: preserve structure and key relationships but improve hierarchy and spacing
  - `editorial`: preserve the story and required logic while re-composing the page more freely
- State what must not change: required images, diagram order, proof points, hierarchy, and tone.
- State what may change: spacing, typography, color system, pacing, simplified decoration, or clearer grouping.
- Do not choose visual style by trend alone. Ground it in the rhetorical job of the deck.
- Before implementation, write down the composition posture for the deck: dense or spacious, centered or asymmetric, sober or expressive, restrained or dramatic.
- Use a high visual bar. Aim for polished modern web design quality, not just functional slide transcription.
- Treat the design contract as executable guidance, not mood-board prose. If it is too vague for another agent to follow, tighten it before coding.
- Pull typography, title-fit, and bilingual limits from [typography-rules.md](./references/typography-rules.md) instead of inventing them per deck.

### 6. Write the Storyline Before Layout

- Turn the logic model into `40-rebuild/page-specs.md` and `40-rebuild/page-specs.json`.
- Work top-down:
  1. define the deck storyline
  2. define each slide's job
  3. define the target layout pattern for each slide
  4. fill in refined copy and visuals
- For each slide, decide the dominant reading path and visual anchor before placing detailed content.
- Decide title posture explicitly: single-line, balanced two-line, or intentional stack. Default to a slide-level headline band that spans the main content width. Never accept accidental newspaper-style wrapping caused by an overly narrow text box.
- Keep one page spec per slide with:
  - source slide number
  - input mode
  - slide role
  - archetype
  - core takeaway
  - source of truth
  - confidence level
  - required assets
  - target layout
  - proportional spatial map
  - dominant visual anchor
  - title posture
  - primary proof device
  - bilingual strategy
  - mobile degradation plan
  - animation intent
  - fidelity notes
- Use layout pattern names only from [layout-patterns.md](./references/layout-patterns.md).
- Use archetype names only from [page-archetypes.md](./references/page-archetypes.md) and, when helpful, start from `templates/archetypes/*.yml`.
- Rewrite unclear source copy before adding translation.
- Prefer shorter, clearer source-language copy over literal deck transcription.
- Treat layout as authorship. Explicitly judge scale contrast, negative space, alignment rhythm, edge control, and whether the page feels designed rather than auto-composed.
- If the opening slides already establish deck structure, use the next slide to deepen framing, stakes, or decision context rather than echo the same table of contents again.

### 7. Add the Bilingual Layer

- Add bilingual content only after the source copy is solid.
- Bind translation to content blocks, not to the slide as a monolith.
- Default to a language toggle. Use side-by-side bilingual layouts only when density is low enough to stay elegant.
- Use [bilingual-toggle-pattern.md](./references/bilingual-toggle-pattern.md) for DOM structure, CSS layering, and toggle behavior. Keep the toggle visible in slide chrome.
- Keep both languages semantically aligned. Do not make one version more persuasive or more complete than the other unless the user asks.
- When translated text becomes longer, adjust layout or hierarchy instead of shrinking text into unreadability.

### 8. Rebuild the Web Deck

- Before full-deck implementation, write `40-rebuild/pilot-selection.md`.
- Pick five representative slides that cover the main page archetypes of the source deck. Prefer a mix such as:
  - cover or chapter framing
  - logic diagram or comparison page
  - timeline / roadmap / process page
  - image-led evidence or product-sample page
  - closing / ask / decision page
- Rebuild those five slides first and use them to validate the visual system, page control, text-image handling, and diagram treatment.
- Scale the deck only after the pilot pages are approved or clearly judged strong enough to extend.
- Generate the deck only after `deck-brief.md`, `storyline.md`, `asset-register.md`, and `page-specs.md` are complete.
- Preserve necessary text-image logic and diagram logic from the source.
- Rebuild diagrams as semantic HTML, SVG, or CSS when possible.
- Start from [slide-shell-template.html](./templates/slide-shell-template.html) for deck chrome, slide IDs, and navigation semantics unless the project already has a stronger shell.
- Implement the deck as a viewport-bounded slide player:
  - give the main slide canvas a strict aspect ratio, typically `16 / 9`
  - constrain it to the viewport with `max-width` and `max-height` logic
  - suppress native browser scrolling in playback mode
  - hide overflow at the slide-container level rather than letting the page grow vertically
- Translate original PPT coordinates into proportional layout zones. Use Grid, Flexbox, `fr`, `%`, and named regions before considering absolute positioning.
- Use absolute positioning only for small, local overlays such as badges, arrows, or diagram labels when the parent zone is already stable.
- When elements overlap, assign explicit `z-index` values instead of relying on DOM order alone.
- If the source implies staged reveals, carry that build order into markup with simple step metadata such as `data-step`.
- Preserve speaker notes or hidden source metadata in a non-visual aside when available.
- Differentiate asset implementation on purpose: SVG or CSS for scalable vector-like marks, `<img>` for raster visuals, and background layers for ambient full-slide fields.
- Prefer container-query units such as `cqi`, `cqw`, or `cqh` for slide-synchronized typography and spacing. If container queries are unavailable, use a documented slide-relative fallback such as carefully chosen `vmin` tokens.
- Provide:
  - a table of contents or slide index
  - direct slide jumps
  - stable deep links such as `#slide-07`
  - keyboard navigation
  - bilingual toggle
  - PDF export path
  - reduced-motion handling
- Keep animations purposeful. Use motion to reveal logic, sequence, emphasis, or transitions, not decoration.
- On mobile, preserve presentation logic before web convenience. Scale the slide first, simplify non-essential chrome second, and only collapse multi-column layouts when readability would otherwise fail.
- Avoid slide-internal scrolling.
- When a stronger example is helpful, inspect `examples/minimal-deck/` before inventing the shell from scratch.

### 9. Run QA and Repair

- Visually inspect every generated slide.
- Check for overlap, occlusion, clipping, inconsistent spacing, dead links, and broken navigation.
- Check that each slide still fits as one bounded frame without native browser scrollbars appearing.
- Check that aspect ratio, scale, and spacing feel synchronized instead of behaving like unrelated webpage modules.
- Check for awkward heading wraps in both languages, especially on covers and opening analytical slides.
- Check that title bands read as a deck-wide system. Most body slides should not wrap unless the copy genuinely requires it.
- Measure title containers in DevTools or an equivalent inspector. The rendered title region should not drop below `55%` of the slide width unless the archetype explicitly justifies it.
- Compare low-confidence slides against the source again before accepting any stylized redraw.
- Check for repeated information across headline, body, stat chips, and diagram labels. Remove duplicated layers instead of polishing them.
- Check for duplicate navigation or duplicated overview content in the opening sequence.
- Check for dead zones: large blank regions that do not improve focus, pacing, or composition.
- Check that mobile degradation still behaves like a slide deck. A reduced-size slide is preferable to a broken long-scroll document unless readability forces a controlled reflow.
- Check logic as well as layout:
  - does each slide still say the same thing?
  - do images still correspond to the right claims?
  - do arrows, order, comparison groups, and labels still make sense?
- Compare generated slides with source slide screenshots when fidelity matters.
- Run a design-quality pass, not only a correctness pass. Ask whether the page has a strong focal point, readable hierarchy within two seconds, controlled density, and typography that feels intentional.
- Reject pages that are merely neat but visually generic. If the composition could be mistaken for a default AI slide template, redesign it.
- Write `50-qa/qa-report.md`.
- Fix issues before delivery. Do not treat QA as documentation only.
- Prefer `scripts/check_stage_gates.py <workspace-dir>` to confirm required stage artifacts exist before final delivery.

## References

- Read [artifacts.md](./references/artifacts.md) when creating or reviewing stage outputs.
- Read [style-judgment.md](./references/style-judgment.md) when deciding visual direction.
- Read [fidelity-checks.md](./references/fidelity-checks.md) when deciding what must stay logically faithful and what may change.
- Read [reference-deck-learning.md](./references/reference-deck-learning.md) when the user provides internal reference decks.
- Read [external-design-lessons.md](./references/external-design-lessons.md) when the user asks for broader craft improvement or when title hierarchy, redundancy, and page control are weak.
- Read [web-presentation-rules.md](./references/web-presentation-rules.md) when implementing slide containers, scaling behavior, playback constraints, or mobile degradation for web-based presentations.
- Read [typography-rules.md](./references/typography-rules.md) when title fit, body measure, or bilingual robustness is at risk.
- Read [layout-patterns.md](./references/layout-patterns.md) and [page-archetypes.md](./references/page-archetypes.md) before writing page specs.
- Read [bilingual-toggle-pattern.md](./references/bilingual-toggle-pattern.md) before implementing the language switcher.
- Read [visual-parsing-playbook.md](./references/visual-parsing-playbook.md) when the source is a PDF, screenshot set, or otherwise depends on visual parsing and slicing.

## Trigger Examples

- `Use $deck-web-rebuilder to turn this investor deck into a bilingual web version without losing the original logic.`
- `Use $deck-web-rebuilder to rebuild this keynote as an interactive slide site with navigation, deep links, and PDF export.`
- `Use $deck-web-rebuilder to study this PPTX first, clean up the assets, redraw the diagrams, and then make a faithful web deck.`
