# Stage Artifacts

Use these artifacts as gates between stages. Do not skip forward when a required artifact is missing or still vague.

## `00-source/input-profile.md`

Profile the source before analysis starts.

Include:

- source file types
- selected input mode: `polish`, `reverse-engineer`, or `editorial-compose`
- source-of-truth order
- normalization plan
- expected parsing risks
- note on whether visual parsing is primary or secondary for this project

## `00-source/visual-regions.json`

Store the visual parse for the source pages.

Recommended structure:

- top-level deck id or source id
- one entry per page or slide
- region list per page with:
  - region id
  - semantic type
  - approximate bounding box
  - likely group id
  - likely z-order
  - confidence
  - optional slice path
  - optional relation type for diagrams or structured galleries
  - optional primitive count
  - optional label-anchor strategy
  - optional `must_show_full_frame`
  - optional crop tolerance
  - optional alignment group id

This file should show that the rendered pages were actually analyzed, not only OCR'd.

## `00-source/composition-graph.json`

Capture authoring intent on top of the visual parse.

For each detected group, scaffold, or composite, include:

- `group_id`
- `source_slide`
- `member_object_ids` or `member_region_ids`
- `group_intent`
  - `semantic-composite`
  - `layout-scaffold`
  - `content-bearing`
  - `presentation-chrome`
- `evidence_source`
  - `rendered-only`
  - `object-structure`
  - `both`
- `confidence`
- `rebuild_policy`
  - `preserve-as-group`
  - `collapse-to-grid`
  - `redraw-as-svg`
  - `convert-to-css-layout`
  - `ignore`
- notes

This file should distinguish visual grouping from construction scaffolding.

## `10-understanding/deck-brief.md`

Capture the deck-level understanding in concise prose.

Include:

- topic
- speaker or organization
- intended audience
- occasion or setting
- persuasion goal
- overall tone
- one short summary of the deck's message
- one short note on what the audience should think, feel, or do after the deck

## `12-reference-study/reference-deck-notes.md`

Create this whenever the user provides internal reference decks. It can also be used with `none provided` as a minimal note when no references exist.

Include:

- reference files reviewed
- deck-shell rules learned
- recurring page archetypes
- text-image rules worth copying
- anti-patterns to avoid
- what should transfer to the target deck

Also write `12-reference-study/reference-deck-notes.yaml` using the structure in [reference-deck-learning.md](./reference-deck-learning.md).

## `20-logic/visual-structure-map.md`

Decode every slide's visual structures before classifying assets or planning layout.
Use `references/ppt-structure-decoder.md` as the decision guide.

Include for each slide:

- slide number and title or role
- list of detected structure types
- position and semantic role of each structure
- rebuild decision per structure
  - `keep-as-image`
  - `redraw-as-SVG`
  - `css-layout`
  - `html-table`
  - `live-text-layer`
- one-line reason per decision

Do not proceed to `asset-register.md`, `layout-spine.md`, or `page-specs.md` until every pilot slide has an entry.

## `20-logic/storyline.md`

Turn the deck into a structured narrative.

Include:

- the deck arc
- a slide-by-slide role table
- logic breaks or redundancy
- important text-image relationships
- important image-image or diagram relationships
- any claims that rely on proof, sequencing, contrast, or hierarchy

Recommended slide table columns:

- source slide
- slide role
- main point
- supporting evidence
- visual role
- relationship notes

## `20-logic/authoring-intent.md`

Turn slide-level structure decoding into deck-level authoring rules.

Include:

- repeated use of format-only groups
- recurring semantic composites
- pseudo-table patterns
- semantic table patterns
- connector and z-order conventions
- which slides depend heavily on authoring hacks
- what those hacks should become in the web rebuild

## `20-logic/confidence-report.md`

Track what is known and what is inferred.

Include:

- high-confidence relationships
- medium-confidence relationships
- low-confidence relationships
- which slides are safe to redraw freely
- which slides should be preserved conservatively
- any follow-up checks needed before layout or redraw

## `30-assets/asset-register.md`

Treat the visual inventory as a cleaning task.

Recommended columns:

- asset id
- source slide
- asset type
- semantic role
- action
- reason
- translation needed
- redraw notes
- source region id
- confidence
- fit policy
- must show full frame

Use these actions:

- `keep`
- `crop`
- `redraw`
- `translate`
- `remove`

## `30-assets/asset-lineage.json`

Keep every extracted or sliced asset traceable.

Recommended fields:

- asset id
- source slide
- source region ids
- original file path
- derived slice path
- semantic role
- chosen action
- redraw flag
- confidence
- fit policy
- must show full frame
- visible area minimum percent
- focal region hint

## `35-strategy/rebuild-strategy.md`

Define the rules before layout work starts.

Include:

- fidelity mode
- style direction
- what must not change
- what may change
- target tone
- density target
- motion level
- bilingual mode
- any planned merge or split decisions with justification

## `35-strategy/deck-design-system.md`

Translate the chosen style direction into a reusable design contract before implementation.

Include:

- visual theme and atmosphere
- color palette and semantic roles
- typography hierarchy and title behavior
- title-band defaults and no-wrap policy
- slide-shell and navigation rules
- slide boundary model and aspect ratio policy
- scaling model and preferred sizing units
- layout principles, spacing, and whitespace posture
- component patterns for cards, diagrams, callouts, and image frames
- depth and elevation rules
- do and don't rules
- responsive behavior
- mobile degradation order

The file should be concrete enough that another agent could build new slides in the same language without guessing.

Also write `35-strategy/deck-design-system.json` and validate it against `schemas/deck-design-system.schema.json`.

## `35-strategy/layout-rationale.md`

Explain the layout decisions before implementation begins.

Include:

- why each major slide family uses its chosen pattern
- how the deck rhythm alternates dense and spacious pages
- which slides preserve source line-count posture
- which slides require strict media alignment
- which slides must preserve semantic composites as single proof units

## `35-strategy/layout-plan.json`

Store the structured layout plan for each slide before content fill.

Include for each slide:

- slide id
- layout pattern
- dominant reading path
- dominant visual anchor
- zone skeleton
- title band percent
- anchor region percent
- support region percent
- whitespace reserve percent
- max body block count
- copy budget in English and Chinese
- group preservation rules
- diagram redraw policy
- layout confidence

This file should exist before `page-specs.json` is finalized.

## `40-rebuild/layout-spine.md`

Write this before `page-specs.md`. One line per slide. Do not open `page-specs.md` until this file is complete and rhythm-validated.

Required columns per line:

- slide id
- layout pattern
- slide role
- one-line visual intent

Rules:

- layout pattern must be from `references/layout-patterns.md`
- validate rhythm before locking
- do not change a layout pattern after locking without updating `visual-structure-map.md`, `layout-plan.json`, and the corresponding page spec

## `40-rebuild/page-specs.md`

Write one section per destination slide.

Include for each slide:

- source slide number
- input mode
- destination slide id
- slide role
- layout pattern (must match `layout-spine.md`)
- zone skeleton
- core takeaway
- source of truth
- confidence level
- dominant reading path
- layout hypothesis
- title posture
- source title line-count strategy
- required copy blocks
- required assets
- target layout pattern
- proportional spatial map
- whitespace reserve
- copy budget
- group preservation rules
- diagram redraw policy
- diagram contract
- media layout contract
- animation intent
- render audit targets
- bilingual treatment
- mobile degradation plan
- fidelity notes

Do not move into implementation until every source slide has a page spec.

Also write `40-rebuild/page-specs.json` and validate it against `schemas/page-spec.schema.json`.

## `40-rebuild/pilot-selection.md`

Select the representative pilot slides before full-deck implementation.

Include:

- the five chosen source slides
- why each one was selected
- which page archetype each one represents
- what visual system risks the pilot is meant to validate

Do not scale to the whole deck until the pilot pages are reviewed.

## `50-qa/qa-report.md`

Check both visual quality and logical fidelity.

Include:

- layout issues found and fixed
- unresolved issues
- bounded-slide checks
- relationship checks
- bilingual checks
- navigation checks
- PDF export check
- final go or no-go note

## `50-qa/visual-checklist.md`

Keep a short, reusable checklist for:

- two-second hierarchy test
- squint / gravity test
- dead-zone check
- duplicate-proof check
- bilingual-fit check
- mobile deck-behavior check

## `50-qa/render-audit.json`

Keep a machine-readable record of the post-render integrity pass.

Recommended fields per slide:

- slide id
- checked languages
- title line counts
- title wrap status
- overlap status
- clipping status
- occlusion status
- media uniformity status
- diagram semantics status
- notes

## Minimum Gate

Before generating final HTML, confirm these files exist and are meaningful:

- `00-source/input-profile.md`
- `00-source/visual-regions.json`
- `00-source/composition-graph.json`
- `10-understanding/deck-brief.md`
- `12-reference-study/reference-deck-notes.md`
- `12-reference-study/reference-deck-notes.yaml`
- `20-logic/visual-structure-map.md`
- `20-logic/storyline.md`
- `20-logic/authoring-intent.md`
- `20-logic/confidence-report.md`
- `30-assets/asset-register.md`
- `30-assets/asset-lineage.json`
- `35-strategy/rebuild-strategy.md`
- `35-strategy/deck-design-system.md`
- `35-strategy/deck-design-system.json`
- `35-strategy/layout-rationale.md`
- `35-strategy/layout-plan.json`
- `40-rebuild/layout-spine.md`
- `40-rebuild/page-specs.md`
- `40-rebuild/page-specs.json`
- `40-rebuild/pilot-selection.md`
- `50-qa/render-audit.json`
- `50-qa/visual-checklist.md`

Use `scripts/check_stage_gates.py <workspace-dir>` for a quick validation pass.
