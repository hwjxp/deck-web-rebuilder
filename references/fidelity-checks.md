# Fidelity Checks

Preserve meaning before preserving cosmetics.

## Source Of Truth

Use this order when facts conflict:

1. source object layer
2. rendered page
3. OCR text
4. inference

Never let a low-confidence inference overwrite a clear visual relationship from the rendered source.

## What Must Stay Faithful

- slide order unless there is a justified restructure
- each slide's main claim or job
- required proof points and numbers
- essential text-image relationships
- diagram logic, flow direction, sequence, and grouping
- comparison logic, before-after logic, and hierarchy
- audience-facing tone when that tone is part of persuasion

## What May Change

- typography
- spacing
- color system
- decorative shapes
- repeated icons
- weak screenshots that can be replaced by clearer crops or redraws
- non-semantic visual filler

## Relation Types To Preserve

Check these relation types explicitly:

- claim to evidence
- heading to support
- image to caption
- step to step
- before to after
- problem to solution
- comparison A to comparison B
- container to nested item
- chart label to chart mark
- shape-drawn composite to unified visual
- transparent-border table to CSS layout scaffold
- layered composition to live text-over-image structure
- connector arrow to its original directionality and semantic role

## Diagram Rules

When redrawing diagrams:

- describe the logic in words before drawing
- keep directionality intact
- preserve the diagram grammar itself: overlap stays overlap, matrices stay matrices, grouped rows stay grouped rows
- do not silently change the number of primary proof primitives unless the simplification is documented
- keep labels attached to the correct node or edge
- preserve grouping and emphasis
- simplify visuals only after confirming the simplification does not erase meaning

## Image Fit Rules

- if the source visibly shows a full artwork, board, character sheet, or contact sheet, default to preserving the full frame
- use cropping only when the crop is justified and the focal subject remains intact
- never let CSS defaults crop away meaningful content from tables, sheets, or lineup boards
- when the source compares peer visuals side by side, keep their media windows consistent enough that the comparison still feels intentional

## Bilingual Rules

- translate intent, not only wording
- keep corresponding blocks aligned across languages
- do not hide important qualifiers in one language only
- if one language expands, re-layout the page instead of shrinking text until it becomes unreadable

## QA Prompt

When reviewing a rebuilt slide, ask:

- Does it still make the same argument?
- Is every necessary visual relationship still present?
- Would a reader infer the same sequence, grouping, and emphasis as in the source?
- Did the redesign improve clarity without changing the deck's actual claim?
- Does the page establish a clear focal point and reading path within two seconds?
- Does the typography create authority and hierarchy instead of merely fitting text on the page?
- Does the composition feel authored and persuasive, or just clean and serviceable?
- If you hide all text, is there still one obvious visual landing point, or does the page lose its center of gravity?
- Is the content field visibly denser than the empty field, or has whitespace turned into an unsupported dead zone?
- Looking only at size and weight, can you tell title, subtitle, and body apart within two seconds?
- When switching languages, do the corresponding blocks stay structurally aligned instead of causing a major jump in page balance?
- If part of the page was reconstructed from incomplete evidence, is that redraw still conservative enough to avoid inventing a new claim?
- Does a diagram still use the same proof grammar as the source, or was an overlap, matrix, or sequence flattened into a different structure?
- Are all image-led proof objects still fully visible where the source showed them fully, without bottom clipping or edge loss?
- On comparison rows, strips, or sample grids, do peer media still align in height and baseline so the page reads as one system?
