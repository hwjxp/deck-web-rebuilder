# Layout-First Method

Use this during Step 6. Complete the layout skeleton for the pilot set before writing detailed slide copy or placing assets. Content is added into predefined zones after the skeleton is locked.

## Why Layout Comes Before Content

Filling content and layout simultaneously causes repeat failures:

- layout adapts to copy volume instead of slide purpose
- deck rhythm becomes inconsistent because each slide is solved locally
- body copy expands to fill space instead of being disciplined to a zone
- implementation drifts into per-slide exceptions and generic cardification

Layout-first forces three disciplines:

1. each slide's composition is decided by rhetorical job, not text length
2. the deck's visual rhythm is planned as a sequence
3. copy must shrink, sharpen, or split to fit the chosen structure

## Step 1: Write The Layout Spine First

Before writing page specs, write `40-rebuild/layout-spine.md`.

One line per slide:

```text
slide-01 | HERO-FULL      | cover         | one-line title over a calm hero field
slide-02 | HEADLINE-PROOF | framing       | claim on top, proof board below
slide-03 | DIAGRAM-CENTER | proof         | overlap diagram centered, notes secondary
slide-04 | SPLIT-60-40    | showcase      | hero sample left, insight rail right
slide-05 | HEADLINE-PROOF | decision-close | decisive ask above a compact close panel
```

Rules:

- use only names from `references/layout-patterns.md`
- assign exactly one layout pattern per slide
- choose the pattern from the slide's rhetorical job, not content volume
- check the spine as a sequence before proceeding

## Step 2: Draw The Zone Skeleton

For each slide, define the structural zones before filling content.

### Zone Vocabulary

Use these names consistently:

- `HERO-ZONE`
- `TITLE-ZONE`
- `CLAIM-ZONE`
- `STAT-ZONE`
- `VISUAL-ZONE`
- `INSIGHT-ZONE`
- `EVIDENCE-ZONE`
- `ANNOTATION-ZONE`
- `GRID-CELL`
- `DIVIDER-ZONE`

Each zone should have:

- its spatial role
- what kind of content it accepts
- its approximate percentage budget

## Step 3: Allocate Spatial Budgets

Every slide needs explicit spatial budgets before copy fill:

- `title_band_pct`
- `anchor_region_pct`
- `support_region_pct`
- `whitespace_reserve_pct`

Also define:

- one dominant visual anchor
- one dominant reading path
- max body block count
- bilingual copy budget
- group preservation strategy

Do this in `35-strategy/layout-plan.json` and explain the choices in `35-strategy/layout-rationale.md`.

## Step 4: Fill Content Into Zones

Only after the spine and layout plan are locked:

1. write the title as an assertion, not a topic label
2. fill `INSIGHT-ZONE`, `EVIDENCE-ZONE`, and `ANNOTATION-ZONE`
3. assign assets from `30-assets/asset-register.md` into `VISUAL-ZONE` or `HERO-ZONE`
4. cut or rewrite copy if it exceeds the zone budget

Never enlarge the zone just because the copy grew.

## Step 5: Validate Rhythm Before Building

Read the full `layout-spine.md` as a sequence and flag:

- three or more consecutive `HERO-FULL` slides
- four or more consecutive grid slides
- two consecutive `HEADLINE-PROOF` slides with the same exact posture and proof rhythm
- zero breathing slides in a long deck

If rhythm is weak, revise the spine before implementation.

## Pattern To Role Mapping

- `HERO-FULL`: cover, chapter break, emotional pacing, close
- `HEADLINE-PROOF`: single claim, bold finding, benchmark, key metric
- `SPLIT-50`: clean case-study split, before/after
- `SPLIT-60-40`: diagram plus interpretation, showcase plus insight
- `GRID-2COL`: structured comparison
- `GRID-3COL`: compact parallel feature triad
- `TIMELINE-H`: roadmap or sequence
- `DIAGRAM-CENTER`: venn, architecture, matrix, core proof figure

## Guardrail

If a slide has no dominant visual anchor, the layout is not done.

If a logic-heavy slide falls back to generic cards, the layout is not done.

If you are adjusting layout after writing body copy, the process has already slipped. Go back to the spine and zone budgets first.
