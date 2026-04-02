# Web Presentation Rules

Use this reference when the rebuilt output must remain a slide deck in the browser rather than drifting into a conventional web page.

## Positioning

The target is a web-based presentation:

- one source slide should usually map to one bounded web slide
- the browser should behave like a presentation player, not a scrolling document
- presenter-controlled sequence matters more than document-style responsiveness

## 1. Strict Slide Boundaries

Treat every slide as an isolated frame with hard edges.

Implementation defaults:

- use a dedicated slide container with `aspect-ratio: 16 / 9`
- constrain the container to the viewport using `max-width` and `max-height` logic
- suppress native browser scrolling during playback
- use `overflow: hidden` at the slide container level

If content does not fit, redesign the slide. Do not let the canvas silently grow taller like a web article.

## 2. Proportional Layout Reconstruction

Do not rebuild PPT layouts by copying raw coordinates into `left: 125px; top: 40px;`.

Preferred translation pattern:

- read the source slide as zones and proportions
- convert those zones into Grid or Flexbox structure
- express primary spatial relationships with `%`, `fr`, or named areas

Examples:

- a left text block and right image block that occupy a 40/60 split should become `grid-template-columns: 4fr 6fr`
- a top summary band and bottom evidence rail should become grid rows, not stacked arbitrary divs

Use `position: absolute` only for local overlays such as callout arrows, badge chips, or labels inside a stable parent zone.

## 3. Synchronized Slide Scaling

Typography and spacing must scale with the slide canvas, not with the browser window as if they belonged to a normal page.

Preferred approach:

- declare the slide or canvas as a CSS container with `container-type: size` or `inline-size`
- use container-query units such as `cqi`, `cqw`, `cqh`, `cqmin`, or `cqmax`

Typical properties to scale this way:

- `font-size`
- `padding`
- `gap`
- `border-radius` when visually important

Fallback approach:

- if container queries are unavailable, document a slide-relative fallback such as disciplined `vmin` tokens
- do not fall back to large fixed `px` values for major type or spacing

## 4. Mobile Degradation Ladder

Mobile treatment should protect the deck model in this order:

1. scale the entire slide proportionally
2. reduce or hide decorative chrome
3. tighten spacing and secondary copy
4. reflow layout only when the slide would otherwise become illegible

Even after reflow:

- keep one slide within one viewport whenever feasible
- do not turn the deck into a long vertically scrolling page
- preserve the slide's dominant reading path and logical anchor

## 5. QA Checks

When reviewing the generated deck, verify:

- no browser-native vertical scrollbar appears during playback
- each slide remains fully visible inside the viewport
- scale, type, and spacing shrink together instead of falling out of sync
- no major layout block depends on fixed-pixel absolute coordinates
- mobile fallback still feels like a slide, not a document

## 6. Static Heuristics

When adding automated checks, look for:

- `aspect-ratio: 16 / 9`
- viewport-bound sizing tokens such as `100vh`, `100dvh`, `100svh`, `100vw`, `100dvw`, or `100svw`
- `overflow: hidden` for playback
- `container-type`
- at least some container-query or slide-relative units
- no widespread `left`, `top`, `width`, or `height` declarations in large fixed `px` values for main layout blocks
