# Stage Artifacts

Use these artifacts as gates between stages. Do not skip forward when a required artifact is missing or still vague.

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

Use these actions:

- `keep`
- `crop`
- `redraw`
- `translate`
- `remove`

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

## `40-rebuild/page-specs.md`

Write one section per destination slide.

Include for each slide:

- source slide number
- destination slide id
- slide role
- core takeaway
- required copy blocks
- required assets
- target layout pattern
- proportional spatial map
- animation intent
- bilingual treatment
- mobile degradation plan
- fidelity notes

Do not move into implementation until every source slide has a page spec.

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

## Minimum Gate

Before generating final HTML, confirm these files exist and are meaningful:

- `10-understanding/deck-brief.md`
- `12-reference-study/reference-deck-notes.md`
- `20-logic/storyline.md`
- `30-assets/asset-register.md`
- `35-strategy/rebuild-strategy.md`
- `35-strategy/deck-design-system.md`
- `40-rebuild/page-specs.md`
- `40-rebuild/pilot-selection.md`

Use `scripts/check_stage_gates.py <workspace-dir>` for a quick validation pass.
