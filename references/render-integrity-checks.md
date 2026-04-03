# Render Integrity Checks

A slide can be logically correct on paper and still fail after rendering. Run this pass on pilot slides and again on the full deck.

## Required Checks Per Slide

- title line count
- text overlap or collision
- clipping at top, bottom, left, and right
- content occlusion by images, badges, or floating panels
- media window consistency for peer cards or strips
- diagram semantics for logic-heavy slides
- language toggle stability

## Title Checks

- compare rendered line count with the page spec
- compare rendered line count with the source when the page spec says to preserve source posture
- if the source divider was single-line, do not accept a wrapped rebuild unless justified

## Media Checks

- if the source shows the full image, verify the full image is still visible
- if the slide contains a contact sheet, board, or lineup, verify no meaningful bottom or edge content is clipped
- if peer cards compare parallel samples, verify equal media window height and aligned copy baselines

## Diagram Checks

- compare the rebuilt diagram grammar with the source
- overlap should remain overlap
- matrices should remain matrices
- galleries should not become unrelated floating cards
- labels should stay attached to the right proof object

## Overlap And Occlusion Checks

- no text should sit under another text block
- no image should hide slide copy unless the overlap is intentional and documented
- no badge, chip, or rail should cover proof content

## Language Checks

- test at least both `zh` and `en`
- confirm the language toggle does not cause new overlap, new clipping, or a title-width collapse

## Suggested Render Audit Structure

Use `50-qa/render-audit.json` with entries like:

```json
{
  "slides": [
    {
      "slide_id": "slide-03",
      "checked_languages": ["zh", "en"],
      "title_line_counts": { "zh": 1, "en": 1 },
      "title_wrap_status": "pass",
      "overlap_status": "pass",
      "clipping_status": "pass",
      "occlusion_status": "pass",
      "media_uniformity_status": "n/a",
      "diagram_semantics_status": "pass",
      "notes": ""
    }
  ]
}
```

## Tooling Notes

- capture slides after the deck's own controller has activated the target slide, not by assuming hash navigation alone is enough
- if a deck has interactive chrome, wait for the presentation runtime before capturing
- use Playwright or an equivalent browser tool for repeatable screenshots and DOM inspection

## Useful Official References

- [MDN: text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap)
- [MDN: aspect-ratio](https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio)
