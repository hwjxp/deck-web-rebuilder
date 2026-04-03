# Media Fit Rules

Treat image fitting as a semantic decision, not a CSS afterthought.

## Core Principle

The visible extent of an image is part of slide fidelity. If the source slide shows a full artwork, board, sheet, or contact strip, the rebuild must not crop it away accidentally.

MDN is explicit that `object-fit: contain` preserves the entire replaced element inside the box, while `object-fit: cover` fills the box by cropping if necessary. Use that difference deliberately, not by habit.

## Fit Policies

### `contain`

Use when:

- the source visibly presents the full artwork or board
- the asset is a sheet, lineup, matrix, or contact strip
- edge content carries meaning
- cropping would hide labels, limbs, faces, or comparison logic

### `safe-crop`

Use only when all of these are true:

- the focal subject is clear
- the crop does not remove meaningful comparison content
- the source already suggests a safe crop, or the crop is documented as intentional
- the page spec records the focal region or crop rationale

### `cover`

Use only when:

- the asset behaves like an ambient background field
- the source already crops the image or treats it as a texture
- no comparison logic or edge detail would be lost

Never use `cover` by default for diagrams, tables, character boards, or proof sheets.

## Alignment Rules

- if a row of peer cards or samples is supposed to compare like with like, use a consistent media window height
- if intrinsic source ratios differ, normalize the outer media window first, then fit the asset inside it
- prefer equal image windows plus aligned text baselines over letting each card invent its own height

## Crop Safety Questions

- does the source show the whole asset
- would cropping remove labels, captions, or character variants
- would the crop make a comparison row feel uneven
- does the page still read correctly if only the visible region is shown

If any answer is risky, default back to `contain` or reserve more layout space.

## Implementation Notes

- use `object-position` when a safe crop needs a stable focal point
- for boards and sheets, scale down the board before clipping it
- for sample strips, separate the media window from the text card so alignment can stay stable
- for diagrams masquerading as images, prefer redraw over crop

## QA Questions

- is the visible image area faithful to the source intent
- was any important bottom or edge content clipped away
- do peer media windows line up cleanly
- did a board, sheet, or lineup get treated like a decorative photo by mistake

## Useful Official References

- [MDN: object-fit](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit)
- [MDN: Replaced element properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Images/Replaced_element_properties)
- [MDN: object-position](https://developer.mozilla.org/en-US/docs/Web/CSS/object-position)
