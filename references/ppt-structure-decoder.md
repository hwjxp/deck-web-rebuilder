# PPT Visual Structure Decoder

Use this reference during Step 2 and Step 4. For every slide, decode its visual structures before classifying assets or planning layout. Write the results into `20-logic/visual-structure-map.md` and summarize deck-level patterns in `20-logic/authoring-intent.md`.

## How To Decode A Slide's Visual Structures

Look at the rendered slide image and the extracted shape or table data together. Never rely on extracted text alone because extracted text loses position, z-order, grouping, border visibility, and authoring hacks.

For each slide, answer these questions in order:

1. What is the primary visual object on this slide: image, drawn diagram, table, or text block?
2. Are there groups present? For each group, is it semantic, format-only, or mixed?
3. Are there tables? If so, are their borders visible, invisible, or only serving alignment?
4. What reading order is implied by position, scale, grouping, and visual weight?

Then write the results into `00-source/composition-graph.json` and `20-logic/visual-structure-map.md`.

## Structure Type 1: Format-Only Group

### What It Looks Like

Multiple shapes or text boxes are grouped so the author could move or align them together, but each item remains semantically independent.

### How To Identify It

- grouped items have no shared boundary, connector, or fused visual silhouette
- each item still makes sense on its own
- the group looks like a spacing or alignment convenience rather than one object

### Rebuild Rule

Treat each item independently. Rebuild the spatial relationship with semantic HTML plus CSS layout. Do not preserve the group as if it were one semantic unit.

Default rebuild policy in `composition-graph.json`: `collapse-to-grid` or `convert-to-css-layout`

## Structure Type 2: Semantic Composite Group

### What It Looks Like

Multiple shapes combine into one visual object or one proof diagram:

- chevron sequence
- venn or overlap diagram
- ring process
- funnel
- pyramid
- custom timeline
- synthetic icon made from multiple primitive shapes

### How To Identify It

- shapes overlap or lock together visually
- removing one piece breaks the logic or silhouette
- the group encodes sequence, hierarchy, containment, comparison, or flow

### Rebuild Rule

Treat the entire group as one visual unit. Do not translate it into a bullet list. Record the semantic type and redraw it as SVG or preserve it as one exported asset when SVG redraw is not yet safe.
Do not try to re-express a complex PPT-built composite as a pile of ad hoc CSS boxes just because the source was made from primitive shapes.

Default rebuild policy in `composition-graph.json`: `redraw-as-svg` or `preserve-as-group`

## Structure Type 3: Transparent-Border Table

### What It Looks Like

A real PPT table exists in the object layer, but the rendered slide shows clean alignment with no visible grid. The table is acting as a hidden scaffold.

### How To Identify It

- table exists in the PPT data
- rendered slide shows no meaningful table borders
- borders are transparent, white-on-white, or visually absent
- the content would read like free-floating aligned blocks if extracted

### Rebuild Rule

Do not rebuild this as an HTML `<table>`. Convert the rows and columns into CSS Grid or Flexbox, preserving proportions and alignment but not exposing invisible scaffolding to the audience.
If the table is only a layout hack, the web rebuild should inherit the alignment result, not the hidden construction method.

Default rebuild policy in `composition-graph.json`: `convert-to-css-layout`

## Structure Type 4: Semantic Table

### What It Looks Like

A real data table with visible row and column logic, explicit headers, and audience-facing tabular meaning.

### How To Identify It

- visible borders, separators, or cell bands exist in the render
- header styling indicates structured data
- the audience is meant to compare rows and columns

### Rebuild Rule

Render as an HTML `<table>` when possible. Preserve headers, alignment, and comparative meaning. Do not add borders that the source did not show.

Default rebuild policy in `composition-graph.json`: `preserve-as-group` or `convert-to-css-layout` only if semantics are preserved

## Structure Type 5: Layered Composition

### What It Looks Like

Multiple objects overlap, and the z-order itself carries meaning:

- text over an image
- annotation over a chart
- translucent overlay over a photo
- reading surface behind text

### How To Identify It

- objects share the same area
- stacking is visually intentional
- flattening them would lose legibility or rhetorical emphasis

### Rebuild Rule

Preserve the stacking logic with live HTML text layers and explicit z-order. Do not flatten layered compositions into a single raster unless there is no other safe path.

Default rebuild policy in `composition-graph.json`: `preserve-as-group` or `convert-to-css-layout`

## Structure Type 6: Semantic Connector

### What It Looks Like

Lines or arrows created with PowerPoint connectors that indicate sequence, causality, dependency, or relation.

### How To Identify It

- the object layer exposes a connector or line
- rendered arrows clearly point from one item to another
- removing the connector would erase logic, not just decoration

### Rebuild Rule

Do not treat connectors as dividers. Record the relationship in `20-logic/storyline.md` and preserve directionality in the redraw.

Default rebuild policy in `composition-graph.json`: `redraw-as-svg`

## Grouping Dichotomy

Every detected group must be classified one of these ways before rebuild:

- `semantic-composite`
- `layout-scaffold`
- `content-bearing`
- `presentation-chrome`

If you cannot tell, lower confidence and rebuild conservatively.

## Pseudo-Table Detection

Distinguish these two cases explicitly:

- `pseudo-table`: looks like a table in object data, but only aligns content
- `semantic-table`: row and column relationships are audience-facing meaning

Never auto-convert a pseudo-table into a visible HTML table.

## Output: `20-logic/visual-structure-map.md`

For each slide, record:

```markdown
## Slide [N] — [title or role]

Visual structures detected:
- [structure type] at [position]: [what it represents]
- [structure type] at [position]: [what it represents]

Rebuild decisions:
- [structure type] -> [keep-as-image | redraw-as-svg | css-layout | html-table | live-text-layer]
- reason: [one sentence]
```

## Output: `00-source/composition-graph.json`

For every group or scaffold you detect, record:

- `group_id`
- `source_slide`
- `member_object_ids` or `member_region_ids`
- `group_intent`: `semantic-composite`, `layout-scaffold`, `content-bearing`, or `presentation-chrome`
- `evidence_source`: `rendered-only`, `object-structure`, or `both`
- `confidence`
- `rebuild_policy`: `preserve-as-group`, `collapse-to-grid`, `redraw-as-svg`, `convert-to-css-layout`, or `ignore`
- `notes`

Do not proceed to asset classification or layout planning until this structure pass is complete for the pilot set.
