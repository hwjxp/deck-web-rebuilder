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

- author against one explicit "normal size" for the deck and scale from that baseline uniformly
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

## 4. Runtime And Navigation

Playback should feel like a presentation runtime, not a stitched set of independent pages.

Implementation defaults:

- give every slide a stable ID and deep-link target
- preserve keyboard navigation and direct slide jumps as first-class interactions
- keep sequential reveal logic explicit in markup instead of burying it in arbitrary delays
- when the shell can resize independently of the window, trigger a layout recomputation after the container changes size

If the deck offers overview or scroll-preview modes, treat them as alternate views of the same presentation state, not as a second document model.

## 5. Mobile Degradation Ladder

Mobile treatment should protect the deck model in this order:

1. scale the entire slide proportionally
2. reduce or hide decorative chrome
3. tighten spacing and secondary copy
4. reflow layout only when the slide would otherwise become illegible

Even after reflow:

- keep one slide within one viewport whenever feasible
- do not turn the deck into a long vertically scrolling page
- preserve the slide's dominant reading path and logical anchor

## 6. PDF And Print Export

PDF export is part of the product, not an afterthought.

Implementation defaults:

- provide a print entry path that activates deck-specific print styles
- use `@media print` to remove interactive chrome that should not appear in exported pages
- use `@page` when page size, orientation, or print margins need explicit control
- verify whether fragments should print incrementally or fully expanded, and choose one behavior deliberately
- if speaker notes are carried into export, choose whether they overlay the slide or print on separate pages

Do not assume the screen layout automatically becomes a good PDF.

## 7. Motion And Reduced Motion

Build-order and transitions may strengthen a slide, but they must degrade safely.

Implementation defaults:

- keep reveal steps, emphasis motion, and slide transitions tied to rhetorical purpose
- provide a reduced-motion mode using `@media (prefers-reduced-motion: reduce)`
- in reduced-motion mode, replace large movement with instant state changes, fades, or no animation
- test that fragment order and comprehension still hold when non-essential motion is removed

Avoid motion that is required just to understand where content moved.

## 8. Large-Deck Performance

Large decks often carry many screenshots, boards, or full-slide images. Protect initial load and navigation smoothness.

Implementation defaults:

- use `srcset` and `sizes` for heavy raster assets that need resolution switching
- lazy-load images and iframes that are not part of the initial viewport or current slide
- keep currently visible slide assets eager enough to avoid a blank first impression
- when rendering many off-screen slides or overview cards, `content-visibility: auto` is acceptable on non-active slide wrappers if paired with `contain-intrinsic-size`
- do not use `content-visibility` on the active slide in a way that breaks measurement, focus, or capture flows

Performance optimizations must not change slide semantics, visible crop, or accessibility.

## 9. QA Checks

When reviewing the generated deck, verify:

- no browser-native vertical scrollbar appears during playback
- each slide remains fully visible inside the viewport
- scale, type, and spacing shrink together instead of falling out of sync
- no major layout block depends on fixed-pixel absolute coordinates
- mobile fallback still feels like a slide, not a document
- print export produces intentional page sizing, margins, and fragment behavior
- reduced-motion mode still preserves slide logic and navigation clarity
- heavy later slides do not delay first paint of the opening sequence unnecessarily

## 10. Static Heuristics

When adding automated checks, look for:

- `aspect-ratio: 16 / 9`
- viewport-bound sizing tokens such as `100vh`, `100dvh`, `100svh`, `100vw`, `100dvw`, or `100svw`
- `overflow: hidden` for playback
- `container-type`
- at least some container-query or slide-relative units
- `@media print` for export handling
- `@media (prefers-reduced-motion: reduce)` for motion downgrade
- `loading=\"lazy\"` only on genuinely off-screen images or embeds
- `srcset` and `sizes` on oversized raster assets where resolution switching matters
- `content-visibility: auto` only on non-active slide wrappers or overview surfaces
- no widespread `left`, `top`, `width`, or `height` declarations in large fixed `px` values for main layout blocks

## Useful Official References

- [reveal.js: Presentation Size](https://revealjs.com/presentation-size/)
- [reveal.js: PDF Export](https://revealjs.com/pdf-export/)
- [reveal.js: Fragments](https://revealjs.com/fragments/)
- [MDN: CSS container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries)
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/%40media/prefers-reduced-motion)
- [MDN: Printing](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Media_queries/Printing)
- [MDN: @page](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40page)
- [MDN: content-visibility](https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility)
