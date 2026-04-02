# Layout Patterns

Use these terms in `page-specs.md` and `page-specs.json`. Do not invent new layout pattern names.

## Pattern Library

### `HERO-FULL`

- use for: covers, chapter dividers, image-led showcase pages
- reading path: headline first, hero proof second
- title width: at least `60%` of the slide width
- warning: do not hide weak copy behind a decorative full-bleed image

### `SPLIT-50`

- use for: balanced compare-and-explain pages
- reading path: left and right panels should feel equal in hierarchy
- title width: use the full text panel, not a narrow nested box
- warning: do not make both halves fight for primary attention

### `SPLIT-60-40`

- use for: image-led proof, diagram plus note, showcase with insight panel
- reading path: 60% side proves, 40% side interprets
- title width: follow the wider text column, usually `55%+` of canvas
- warning: the side note should explain, not duplicate the hero

### `HEADLINE-PROOF`

- use for: executive summary, analytical framing, benchmark proof
- reading path: headline and lede set the claim, proof object carries evidence below
- title width: wide headline region with at most two lines
- warning: avoid a second proof layer such as extra stat pills that repeat the same point

### `GRID-2COL`

- use for: controlled comparisons, paired arguments, dual examples
- reading path: left-to-right or top-left to top-right
- title width: unaffected by the column split; keep the title in its own wide region
- warning: not a fallback for diagrams, flows, or timelines

### `GRID-3COL`

- use for: three-way feature breakdown, triads, compact example strips
- reading path: one scan across all three columns
- title width: separate from the grid
- warning: if the page is logic-heavy, this usually becomes generic cardification

### `TIMELINE-H`

- use for: roadmap, chronology, staged rollout, sequential process
- reading path: horizontal progression with explicit ordering
- title width: generous, then hand off attention to the rail
- warning: never replace sequence logic with an unordered card strip

### `DIAGRAM-CENTER`

- use for: overlap diagrams, matrices, frameworks, central proof figures
- reading path: centered proof first, annotations second
- title width: wide title block above or beside the proof object
- warning: avoid surrounding the diagram with too many equal-weight notes

## Selection Notes

- choose the pattern from the slide's rhetorical job, not from a desire for variety
- if the source argument depends on sequence, ranking, or structure, prefer a diagram, timeline, or matrix over cards
- if the slide needs one dominant visual anchor, do not choose a grid pattern unless the grid itself is the anchor
