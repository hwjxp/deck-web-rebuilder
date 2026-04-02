# External Design Lessons

Use this note when the user asks for broader craft improvement beyond the source deck and internal references.

## Transferable Lessons

- Typography should define hierarchy, focus attention, and preserve glanceable reading order. Use a stable scale and vertical rhythm instead of relying on accidental line breaks to create drama.
- Smaller text and tertiary labels should stay secondary. Do not shrink core headings or key conclusions just to fit a rigid layout box.
- Strong product and proposal interfaces should be understandable at a glance. Let type, color, and composition guide attention before the viewer starts reading line by line.
- Images and decorative shapes should stay only when they add informational or rhetorical value. Remove visuals that lengthen the page without improving understanding.
- Offer one clear overview or index system. Repeating a second full contents page is rarely useful unless it reframes the story in a new way.
- Balance whitespace with information density. Spacious pages still need a held composition, not a floating title above a disconnected row of cards.
- Before implementation, turn the visual direction into a reusable design contract. A deck-level `DESIGN.md` or `deck-design-system.md` helps the agent keep theme, type, shell, spacing, and do/don't rules consistent across pages.

## Source Links

- Google for Developers, Typography: [developers.google.com/cars/design/automotive-os/design-system/typography](https://developers.google.com/cars/design/automotive-os/design-system/typography)
- Google Design Library, Robinhood and Material: [design.google/library/robinhood-investing-material](https://design.google/library/robinhood-investing-material)
- Nielsen Norman Group, Images on Mobile: [nngroup.com/videos/mobile-images](https://www.nngroup.com/videos/mobile-images/?lm=supporting-multiple-location-users&pt=article)
- Nielsen Norman Group, Site Map Usability report listing: [media.nngroup.com/media/reports/free/Site_Map_Usability_2nd_Edition.pdf](https://media.nngroup.com/media/reports/free/Site_Map_Usability_2nd_Edition.pdf)
- VoltAgent `awesome-design-md`: [github.com/VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

## How To Apply Them To Deck Rebuilds

- First fix heading width and line-break behavior before fine-tuning font size.
- Remove repeated agenda pages when cover navigation already orients the viewer.
- Let diagrams, timelines, and comparison structures carry the main argument; use copy only to interpret or sharpen the takeaway.
- During QA, explicitly mark pages that feel empty, duplicated, or overexplained and redesign them before scaling the system to the full deck.
