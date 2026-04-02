# Deck Design System Template

Copy this template into `35-strategy/deck-design-system.md`, then fill in project-specific decisions. Do not start from a blank page.

Also mirror the same decisions into `35-strategy/deck-design-system.json` using `schemas/deck-design-system.schema.json`.

## 1. Rhetorical Context

- theme:
- occasion:
- speaker:
- audience:
- persuasion job:
- tone keywords:

## 2. Canvas Rules

- base canvas: `1440 x 810` or `1280 x 720`
- aspect ratio: `16:9`
- viewport policy: fit whole slide inside the viewport without native browser scroll
- overflow policy: hide overflow at the slide level
- scaling model: container-synchronized sizing
- preferred units: `cqi`, `cqw`, `cqh`, fallback `vmin`

## 3. CSS Token Template

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

  --line-height-display: 1.1;
  --line-height-title: 1.1;
  --line-height-body: 1.6;
  --line-height-caption: 1.35;

  --font-weight-display: 700;
  --font-weight-title: 700;
  --font-weight-body: 400;
  --font-weight-emphasis: 600;

  --spacing-4: 0.4cqi;
  --spacing-8: 0.8cqi;
  --spacing-12: 1.2cqi;
  --spacing-16: 1.6cqi;
  --spacing-20: 2cqi;
  --spacing-24: 2.4cqi;
  --spacing-32: 3.2cqi;
  --spacing-40: 4cqi;

  --color-background: var(--project-background);
  --color-surface: var(--project-surface);
  --color-text-primary: var(--project-text-primary);
  --color-accent: var(--project-accent);
  --color-muted: var(--project-muted);
}
```

## 4. Color Slot Semantics

- `background`: full canvas field or chapter field
- `surface`: cards, notes, secondary panels
- `text-primary`: all primary reading copy
- `accent`: one main emphasis color for proof, key action, or section signals
- `muted`: labels, supporting captions, subdued guide rails

Use slot semantics first. Pick literal colors only after the rhetorical direction is fixed.

## 5. Typography Contract

- display style:
- title style:
- subtitle style:
- body style:
- caption and label style:
- body max inline size:
- caption max inline size:
- allowed font weights:

Line-height defaults:

- display: `1.1`
- title: `1.1`
- body: `1.6`
- caption: `1.35`

## 6. Title Wrapping Rules

Use these rules verbatim unless the deck has a strong reason to override them.

```css
.slide-title {
  max-inline-size: 72ch;
  min-inline-size: var(--title-min-width, 55%);
  text-wrap: balance;
  hyphens: none;
  line-height: 1.1;
}

.slide-title[data-lang="zh"],
.slide-title[data-lang="en"] {
  min-inline-size: var(--title-min-width, 55%);
}
```

Hard rules:

- ordinary slides: titles max 2 lines and should prefer 1 line when possible
- covers and section dividers: titles max 3 lines
- treat the title as a slide-level headline band rather than a local card label
- ordinary slides should usually keep the title region above `60%` of the slide width
- never set the title region below `55%` of the slide width just to force dramatic wrapping
- fallback order: `rewrite -> restack -> widen-title-region -> shrink-last`

## 7. Grid and Layout

- column count: `8`
- gutter:
- outer margins:
  - mobile: `16px`
  - tablet: `24px`
  - desktop: `32px`
- content max width: `1280px`
- title band default posture:
- title band min width ratio:
- title band min height:
- dominant title region width:
- common content patterns:

Negative space policy:

- target blank ratio:
- counterweight rule:
- asymmetry vs symmetry:

## 8. Page Chrome

- top navigation:
- slide counter:
- language toggle placement:
- deep-link style:
- chapter markers:

## 9. Bilingual Policy

- default mode: `toggle`
- side-by-side allowed only on:
- English title word limit:
- Chinese title limit:
- fallback order:
- language switching animation:

## 10. Motion and Mobile

- motion level:
- reduced motion behavior:
- mobile degradation order:
  1. scale slide
  2. trim decoration
  3. tighten spacing
  4. rewrite or reflow only as last resort

## 11. Do / Don't

Do:

- one dominant visual anchor per slide
- let diagrams and proof objects carry the argument
- use whitespace as a compositional tool with a visible counterweight

Don't:

- narrow title columns for drama
- repeat agenda after cover navigation already orients
- flatten logic-heavy pages into generic card rows
- let bilingual switching change the structural width of the title region
