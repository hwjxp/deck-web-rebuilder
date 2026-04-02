# Typography Rules

Treat typography as a layout system, not as a final cosmetic pass.

## Title As Orientation

- titles usually belong to a slide-level headline band, not a small local card header
- on ordinary body slides, prefer a single-line title when it fits naturally
- use a balanced two-line title only when the copy genuinely needs it
- intentional stacked titles should be rare and justified by the slide role
- do not let the title region collapse into a decorative narrow column

## Hierarchy Limits

- keep ordinary slides to at most six live text styles:
  - eyebrow
  - title
  - subtitle
  - body
  - caption
  - label
- do not create extra in-between styles to solve local layout problems

## Title Rules

- ordinary slides: max 2 lines, but prefer 1 line
- covers and section dividers: max 3 lines
- English titles above roughly `18-22` words should be rewritten
- Chinese titles above roughly `24-28` characters should be rewritten
- if a title fits clearly on one line, do not force a second line for visual drama
- ordinary slides should usually keep the title region at `60-75%` of slide width
- do not use a narrow title column to force dramatic breaks
- fallback order: `rewrite -> restack -> widen-title-region -> shrink-last`
- avoid Chinese line starts with orphan punctuation when reflowing
- keep punctuation and emphasis spacing consistent across Chinese and English copy

## Body Rules

- body copy should usually stay between `60ch` and `72ch`
- captions and notes should stay shorter than body copy
- use unitless line-height values
- recommended line heights:
  - title: `1.05-1.15`
  - body: `1.4-1.6`
  - caption: `1.3-1.45`

## Weight Rules

- body defaults to regular or medium
- bold is for emphasis, not for building an entire hierarchy
- small labels and helper chips must remain tertiary
- never shrink key conclusions into caption-scale type just to preserve a layout
- normal body text should meet at least `4.5:1` contrast against its background

## Bilingual Fit Rules

- default to toggle mode, not side-by-side
- side-by-side bilingual layouts are allowed only on genuinely low-density slides
- English and Chinese title fitting should be evaluated independently
- language toggle must not change the width of the title region

## QA Questions

- can the viewer distinguish title, subtitle, and body within two seconds
- is the title container wide enough to look deliberate in both languages
- does the title behave like a slide-level orientation system instead of a local box label
- does the body measure still feel readable on large screens
- do captions stay secondary without becoming microscopic
