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
- reduced-motion stability
- print or PDF export stability when export is a requirement

## Title Checks

- compare rendered line count with the page spec
- compare rendered line count with the source when the page spec says to preserve source posture
- if the source divider was single-line, do not accept a wrapped rebuild unless justified

## Media Checks

- if the source shows the full image, verify the full image is still visible
- if the slide contains a contact sheet, board, or lineup, verify no meaningful bottom or edge content is clipped
- if peer cards compare parallel samples, verify equal media window height and aligned copy baselines
- if responsive image sources are used, verify mobile and desktop both preserve the intended proof content
- if later-slide media are lazy-loaded, verify the slide is fully populated before capture or sign-off

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

## Motion Checks

- test normal motion and `prefers-reduced-motion: reduce`
- confirm reduced-motion mode preserves reveal order, emphasis, and navigation clarity
- confirm no essential proof depends on a transform or animation that disappears in reduced-motion mode

## Print And PDF Checks

- test the export path with print styles enabled
- confirm slide chrome, nav controls, and toggles are hidden or reformatted intentionally
- confirm page size, orientation, and margins match the deck contract
- confirm whether fragments print incrementally or fully expanded, and verify the actual export matches that decision
- if notes are included, confirm they appear in the chosen format and do not occlude core slide content

## Performance Checks

- first slide should render with its critical assets without waiting on off-screen slides
- later heavy slides should load in time for navigation without showing broken placeholders
- overview or thumbnail modes should not force all slide content to paint at once if the deck is asset-heavy

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
      "reduced_motion_status": "pass",
      "print_export_status": "n/a",
      "notes": ""
    }
  ]
}
```

## Tooling Notes

- capture slides after the deck's own controller has activated the target slide, not by assuming hash navigation alone is enough
- if a deck has interactive chrome, wait for the presentation runtime before capturing
- use Playwright or an equivalent browser tool for repeatable screenshots and DOM inspection
- when export matters, run at least one actual print-preview or PDF-export pass instead of trusting screen mode
- when reduced motion matters, emulate the media feature during capture to verify the downgraded experience

## Useful Official References

- [MDN: text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap)
- [MDN: aspect-ratio](https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio)
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/%40media/prefers-reduced-motion)
- [MDN: Printing](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Media_queries/Printing)
