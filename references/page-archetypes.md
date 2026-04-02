# Page Archetypes

Use archetypes as reusable slide blueprints. Every slide in `page-specs.json` must declare one.

## Archetype Library

### `cover`

- layout pattern: `HERO-FULL`
- best for: cover, title slide, big chapter opener
- anchor: hero image or chapter field
- density: low
- title region: `60-75%` of canvas width
- anti-patterns: duplicate agenda underneath, crowded meta badges, decorative grid filler

### `section-divider`

- layout pattern: `HERO-FULL`
- best for: chapter boundaries
- anchor: tonal field, line, or single motif
- density: low
- title region: wide and calm
- anti-patterns: body copy that turns the divider into a normal page

### `diagram-plus-insight`

- layout pattern: `SPLIT-60-40` or `DIAGRAM-CENTER`
- best for: frameworks, overlap logic, evidence diagrams
- anchor: one centered or dominant proof object
- density: medium
- title region: full text band above or beside the proof
- anti-patterns: diagram plus stat pills plus repeated conclusion blocks

### `timeline`

- layout pattern: `TIMELINE-H`
- best for: roadmap, phased launch, historical sequence
- anchor: timeline rail
- density: medium to high
- title region: wide headline before the sequence
- anti-patterns: unordered cards, inconsistent node weight, stacked long-scroll mobile fallback

### `comparison-matrix`

- layout pattern: `GRID-2COL` or `DIAGRAM-CENTER`
- best for: structured comparisons and keep/reject evaluations
- anchor: matrix or controlled side-by-side comparison
- density: medium
- title region: wide, separate from the matrix
- anti-patterns: too many highlight colors, three or more equal emphasis zones

### `proof-strip`

- layout pattern: `HEADLINE-PROOF`
- best for: proof pages where a main example or evidence band carries the slide
- anchor: proof strip, gallery rail, or main metric cluster
- density: medium
- title region: top-aligned, max two lines
- anti-patterns: disconnected helper cards under a floating headline

### `showcase`

- layout pattern: `SPLIT-60-40` or `HERO-FULL`
- best for: product samples, illustration showcases, style samples
- anchor: one hero sample
- density: low to medium
- title region: close to the hero, not detached
- anti-patterns: several equal-sized samples with no primary image

### `decision-close`

- layout pattern: `SPLIT-60-40` or `HEADLINE-PROOF`
- best for: closing asks, governance questions, approval gates
- anchor: decision panel or numbered ask cluster
- density: medium
- title region: large closing question or statement
- anti-patterns: ending the deck with a weak summary grid or repeating proof from earlier slides

## Mapping Notes

- `cover` and `section-divider` are the only archetypes allowed to live on mood and scale alone
- logic-heavy slides should usually choose `diagram-plus-insight`, `timeline`, or `comparison-matrix`
- if a slide cannot name one dominant visual anchor, the archetype choice is not finished yet
