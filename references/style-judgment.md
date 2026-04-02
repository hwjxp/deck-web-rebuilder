# Style Judgment

Choose the visual direction from the rhetorical situation, not from habit or trend.

If the user provides internal reference decks, treat them as a craft benchmark and a source of system cues.

## Inputs To Judge

Always infer style from these signals:

- theme: what the deck is actually about
- occasion: investor pitch, keynote, internal review, training, launch, board update, academic talk, sales, or demo
- speaker: founder, operator, designer, researcher, executive, or teacher
- audience: investors, customers, partners, internal leadership, engineers, or students
- job: inform, persuade, reassure, teach, align, or inspire
- reference decks: any internal exemplars that show the expected page shell, design maturity, or layout discipline

## Output To Decide

Decide these before layout:

- tonal direction
- visual intensity
- information density
- typography posture
- motion level
- image treatment
- chart treatment
- composition posture
- amount of negative space
- symmetry versus asymmetry
- page-level visual anchor strategy

## Practical Heuristics

- Use higher contrast and stronger pacing when the deck must persuade quickly.
- Use calmer structure and clearer labeling when the deck must teach or align.
- Use editorial restraint when the source material is serious, technical, or high-stakes.
- Use more expressive motion only when motion helps reveal sequence, emphasis, or cause and effect.
- Keep brand elements when trust or recognition matters. Remove decorative clutter when it dilutes the message.
- Decide what the page should feel like in one glance: decisive, analytical, premium, urgent, calm, or exploratory.
- Prefer one strong organizing idea per slide over several medium-strength visual tricks.
- Use larger scale contrast and cleaner empty space instead of piling on cards, borders, and helper labels.
- If a layout still looks like a default corporate template after content is removed, the composition is not strong enough yet.
- When reference decks are supplied, borrow their discipline of hierarchy, module reuse, and page framing before borrowing their surface styling.

## Quick Mapping

| Occasion | Font Weight Posture | Line Height | Negative Space | Symmetry | Color Use |
| --- | --- | --- | --- | --- | --- |
| Investor / Strategy | bold display `700`, body `400-500` | tight title `1.1`, body `1.45` | `40%+` if the slide is sparse | usually asymmetric, left-heavy | `<= 3` semantic colors |
| Product Keynote | stronger contrast between display and body | medium `1.3-1.5` | `20-30%` | centered hero allowed | brand color plus one highlight |
| Training / Education | regular to medium `400-600` | generous `1.55-1.65` | around `20%` | symmetric grid-led layouts | moderate saturation with section cues |
| Research / Technical | restrained weights, strong labels | standard `1.45-1.55` | `15-25%` | grid-led with clear proof zone | neutral palette plus one proof color |
| Internal Operating Review | medium `500`, low drama | standard `1.4-1.5` | `<= 15%` | left-aligned, table-friendly | monochrome plus one functional accent |

Write the chosen values into `deck-design-system.md` and `deck-design-system.json`. Do not stop at naming the occasion.

## Failure Modes

Avoid these style mistakes:

- choosing a fashionable look that fights the deck's job
- adding decorative motion that weakens logical clarity
- using a premium visual treatment for weak or noisy content instead of fixing the content
- forcing dense bilingual content into a layout designed for a single short language
- relying on generic card grids, safe SaaS styling, or repetitive section blocks when the story needs authored composition
- treating tidy alignment as sufficient even when the page has no focal point, no tension, and no persuasive visual rhythm
