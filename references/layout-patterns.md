# Layout Patterns

Use these names in `40-rebuild/layout-spine.md`, `35-strategy/layout-plan.json`, and `40-rebuild/page-specs.*`. Do not invent new pattern names during implementation.

Every pattern below includes:

- what the pattern is for
- the zone skeleton
- when to use it
- when not to use it
- a minimal CSS skeleton showing only the structural layout

All skeletons assume a bounded slide canvas and use `--slide-width` / `--slide-height`.

## `HERO-FULL`

One dominant field, usually for a cover, chapter break, or high-emotion reveal.

- zone skeleton:
  - `HERO-ZONE`: full canvas background or full-frame hero field
  - `TITLE-ZONE`: one strong headline and optional short subtitle, overlaid or tightly docked
- use when:
  - the slide's job is pacing, tone, chapter transition, or a single memorable statement
  - one image or tonal field can hold the page
- do not use when:
  - the slide has multiple evidence objects
  - the copy needs dense explanation
- CSS skeleton:

```css
.hero-full {
  display: grid;
  grid-template-areas: "hero";
  width: var(--slide-width);
  height: var(--slide-height);
}
.hero-full .hero-zone { grid-area: hero; overflow: hidden; }
.hero-full .title-zone { grid-area: hero; place-self: center start; }
```

## `HEADLINE-PROOF`

A claim-first slide where the top sets the argument and the lower field proves it.

- zone skeleton:
  - `TITLE-ZONE` or `CLAIM-ZONE`: top band
  - `EVIDENCE-ZONE`: main proof object below
  - optional `ANNOTATION-ZONE`: compact explanation, not a second proof
- use when:
  - the audience must grasp one assertion quickly and then see the support
  - a single stat, benchmark, or proof board carries the slide
- do not use when:
  - the slide needs parallel comparison columns
  - the proof needs a left-right dialogue with notes
- CSS skeleton:

```css
.headline-proof {
  display: grid;
  grid-template-rows: 0.34fr 0.66fr;
  width: var(--slide-width);
  height: var(--slide-height);
}
.headline-proof .title-zone { display: flex; flex-direction: column; }
.headline-proof .evidence-zone { overflow: hidden; }
```

## `SPLIT-50`

An even split between two equal-status halves.

- zone skeleton:
  - `VISUAL-ZONE`: left half
  - `CONTENT-ZONE`: right half with `TITLE-ZONE` and `INSIGHT-ZONE`
- use when:
  - the two halves are intentionally balanced
  - the slide is a clean before/after, sample/explanation, or controlled case-study split
- do not use when:
  - one side is obviously more important than the other
  - the visual needs more room than the copy
- CSS skeleton:

```css
.split-50 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  width: var(--slide-width);
  height: var(--slide-height);
}
.split-50 .visual-zone { overflow: hidden; }
.split-50 .content-zone { display: flex; flex-direction: column; }
```

## `SPLIT-60-40`

A proof-led slide: one side proves, the other side interprets.

- zone skeleton:
  - `VISUAL-ZONE`: 60% proof field
  - `TITLE-ZONE`: top of the 40% interpretation rail
  - `INSIGHT-ZONE`: compact explanation below
  - optional `ANNOTATION-ZONE`: tightly docked notes
- use when:
  - diagrams, screenshots, galleries, or boards need more room than the text
  - the note rail must stay subordinate to the proof
- do not use when:
  - the explanation is longer than a compact side panel can hold
  - the page is actually a balanced comparison
- CSS skeleton:

```css
.split-60-40 {
  display: grid;
  grid-template-columns: 3fr 2fr;
  width: var(--slide-width);
  height: var(--slide-height);
}
.split-60-40 .visual-zone { overflow: hidden; }
.split-60-40 .content-zone { display: flex; flex-direction: column; }
```

## `GRID-2COL`

Two parallel cells under a shared title band.

- zone skeleton:
  - `TITLE-ZONE`: full-width top strip
  - `GRID-CELL`: left
  - `GRID-CELL`: right
- use when:
  - the slide genuinely compares two things on equal footing
  - the cells are structurally parallel
- do not use when:
  - the page is really a process, flow, or diagram
  - one column needs dramatically more content than the other
- CSS skeleton:

```css
.grid-2col {
  display: grid;
  grid-template-rows: auto 1fr;
  grid-template-columns: 1fr 1fr;
  width: var(--slide-width);
  height: var(--slide-height);
}
.grid-2col .title-zone { grid-column: 1 / -1; }
.grid-2col .grid-zone { display: contents; }
```

## `GRID-3COL`

Three compact peer cells under a shared title band.

- zone skeleton:
  - `TITLE-ZONE`: full-width top strip
  - `GRID-CELL`: three equal columns
- use when:
  - the slide presents three short, parallel points
  - each cell can stay compact and equal-weight
- do not use when:
  - the slide is logic-heavy
  - the cells need long body copy or mismatched media windows
- CSS skeleton:

```css
.grid-3col {
  display: grid;
  grid-template-rows: auto 1fr;
  grid-template-columns: repeat(3, 1fr);
  width: var(--slide-width);
  height: var(--slide-height);
}
.grid-3col .title-zone { grid-column: 1 / -1; }
.grid-3col .grid-zone { display: contents; }
```

## `TIMELINE-H`

An explicitly sequenced horizontal progression.

- zone skeleton:
  - `TITLE-ZONE`: top strip
  - `TIMELINE-ZONE`: nodes and connectors across the middle band
  - `ANNOTATION-ZONE`: short labels or notes below
- use when:
  - sequence is the argument
  - the audience must read left-to-right progression
- do not use when:
  - there are too many nodes
  - the labels are too long to remain legible
- CSS skeleton:

```css
.timeline-h {
  display: grid;
  grid-template-rows: auto 1fr auto;
  width: var(--slide-width);
  height: var(--slide-height);
}
.timeline-h .timeline-zone { display: grid; grid-auto-flow: column; }
.timeline-h .annotation-zone { display: grid; }
```

## `DIAGRAM-CENTER`

A centered proof object with surrounding labels or notes.

- zone skeleton:
  - `TITLE-ZONE`: top band
  - `VISUAL-ZONE`: centered diagram field
  - `ANNOTATION-ZONE`: below or beside the diagram
- use when:
  - the main proof is a single diagram, venn, matrix, or structure map
  - the page needs one unmistakable center of gravity
- do not use when:
  - the slide really compares parallel samples
  - the proof needs a strong left rail and right rail
- CSS skeleton:

```css
.diagram-center {
  display: grid;
  grid-template-rows: auto 1fr auto;
  width: var(--slide-width);
  height: var(--slide-height);
}
.diagram-center .visual-zone { place-self: center; overflow: visible; }
.diagram-center .annotation-zone { display: flex; flex-wrap: wrap; }
```

## Selection Rule

Choose a layout pattern from the slide's rhetorical job, not its content volume.

- if it is data or a single finding, prefer `HEADLINE-PROOF` or `DIAGRAM-CENTER`
- if it is narrative explanation around a proof object, prefer `SPLIT-60-40`
- if it is a clean comparison, prefer `GRID-2COL`
- if it is emotion, pacing, or chapter rhythm, prefer `HERO-FULL`
- if sequence is the point, prefer `TIMELINE-H`

Never invent a pattern not in this list. If a truly new pattern is needed, add it here first with its zone skeleton, usage rules, and CSS skeleton before using it anywhere else.
