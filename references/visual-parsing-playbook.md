# Visual Parsing Playbook

Use this playbook whenever the source is not perfectly recoverable from object-layer data, or when rendered-slide understanding is needed to preserve composition and logic.

## Core Principle

Visual parsing is not optional. Even for `.pptx`, the rendered page is the ground truth for:

- composition
- grouping
- emphasis
- overlap
- visual rhythm
- text-image pairing

Object extraction helps, but the rendered page decides what the audience actually saw.

At the same time, object-layer clues help infer what the author was doing behind the scenes. Use both layers to distinguish audience-visible semantics from authoring scaffolds.

## Input Modes

Choose one mode early and write it into `00-source/input-profile.md`.

- `polish`
  - use when a structured deck already exists
  - primary goal: preserve story and logic while upgrading design and rebuilding for the web
- `reverse-engineer`
  - use when the source is a `.pdf`, screenshot set, or visually complete export
  - primary goal: recover structure, assets, and logic from rendered pages
- `editorial-compose`
  - use when only rough copy and assets exist
  - primary goal: organize the material into a coherent deck before styling

## Source-Of-Truth Order

Use this priority unless there is a documented reason to override it:

1. source object layer
2. rendered slide or page
3. OCR text
4. inference

Never let low-confidence OCR override a clearly visible diagram, grouping, or title treatment.

## Authoring Intent Layer

On top of visual regions, classify authoring intent:

- `semantic-composite`: multiple PPT objects acting as one proof object
- `layout-scaffold`: groups, invisible tables, or spacer shapes used only for alignment
- `content-bearing`: audience-facing card, block, table, or figure
- `presentation-chrome`: shell elements, dividers, or non-content framing

Write these decisions into `00-source/composition-graph.json`.

## Visual Region Types

At minimum, classify regions into:

- `headline-band`
- `proof-zone`
- `support-copy`
- `photo`
- `screenshot`
- `diagram`
- `chart`
- `table`
- `logo`
- `chrome`
- `decoration`

Each region record should keep:

- region id
- source page
- approximate bounding box
- semantic type
- likely group id
- likely z-order hint
- confidence
- slice path if exported

For image-heavy or logic-heavy regions, also capture:

- `relation_type` for diagram grammar such as `overlap`, `sequence`, `matrix`, `hierarchy`, or `gallery`
- `primitive_count` for the visible proof primitives such as circles, nodes, rows, or columns
- `label_anchor_strategy` for how labels connect to shapes or media
- `must_show_full_frame` when the source visibly presents the full artwork, board, or contact sheet
- `crop_tolerance` such as `none`, `safe-crop-only`, or `source-already-cropped`
- `focal_region_hint` when a crop is allowed but the subject must stay visible
- `alignment_group_id` when neighboring media are supposed to share a common height or baseline

## Slicing Strategy

When the source is PDF- or screenshot-only:

- slice reusable product visuals, screenshots, logos, and isolated diagram fragments
- do not slice decorative noise unless it clearly belongs to the deck shell
- prefer redrawing diagrams and charts once their logic is understood
- keep a traceable lineage record from source page -> region -> exported slice -> chosen action
- if a board, sheet, or character lineup is meant to be read as a whole, preserve it as a board-level region instead of slicing it into arbitrary fragments

## Confidence Rubric

- `high`
  - confirmed by object layer and rendered page
  - safe to redraw or restyle
- `medium`
  - confirmed visually but not structurally
  - safe to preserve with care, redraw only if the logic is understood
- `low`
  - inferred from partial evidence
  - keep conservative, inspect again, or escalate before free redesign

## Practical Tool Stack To Learn From

Use these as patterns and references, not as a promise that one tool solves everything.

- [PyMuPDF](https://pymupdf.io/)
  - strong for text, bounding boxes, links, and image extraction from PDF
- [pdfplumber](https://github.com/jsvine/pdfplumber)
  - strong for low-level PDF objects, tables, lines, and debugging page geometry
- [Adobe PDF Extract API](https://developer.adobe.com/document-services/docs/overview/legacy-documentation/pdf-extract-api/howtos/extract-api/)
  - useful for structured extraction plus figure and table renditions
- [Google Document AI Layout Parser](https://docs.cloud.google.com/document-ai/docs/layout-parse-chunk)
  - useful for layout hierarchy, tables, images, and chunked document understanding
- [Azure Document Intelligence Layout](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout?view=doc-intel-4.0.0)
  - useful for page layout across PDFs and images
- [PaddleOCR PP-StructureV3](https://www.paddleocr.ai/main/en/version3.x/algorithm/PP-StructureV3/PP-StructureV3.html)
  - useful for OCR plus layout detection, tables, formulas, and chart-oriented structure recovery
- [LayoutParser](https://layout-parser.github.io/)
  - useful as a modular document-layout analysis framework
- [DocLayNet](https://research.ibm.com/publications/doclaynet-a-large-human-annotated-dataset-for-document-layout-segmentation)
  - useful as a reference dataset for document layout segmentation
- [SAM 2](https://github.com/facebookresearch/sam2)
  - useful for region segmentation and candidate slicing
- [OmniParser](https://github.com/microsoft/OmniParser)
  - useful inspiration for turning screenshots into structured regions, especially UI-like pages

## Authoring And Layout References Worth Internalizing

- [Microsoft Support: Group or ungroup shapes, pictures, or other objects](https://support.microsoft.com/en-us/office/group-or-ungroup-shapes-pictures-or-other-objects-a7374c35-20fe-4e0a-9637-7de7d844724b)
  - reminder that PowerPoint groups are authoring conveniences first, not guaranteed semantic units
- [Microsoft Support: Use the Selection pane to manage objects in documents](https://support.microsoft.com/en-gb/office/use-the-selection-pane-to-manage-objects-in-documents-a6b2fd3e-d769-46c1-9b9c-b94e04a72550)
  - useful for understanding stacking order, hiding, and object-level ordering signals
- [Microsoft Support: Change the look of a table](https://support.microsoft.com/en-us/office/change-the-look-of-a-table-a18cbaa8-e681-455f-a99f-a2378fe5ff06)
  - useful when deciding whether a detected table is audience-facing data or just a scaffold
- [MDN: grid-template-areas](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-template-areas)
  - strong reference for rebuilding spatial intent with named zones instead of coordinate-by-coordinate positioning
- [MDN: object-fit](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit)
  - useful for making media-fit decisions explicit instead of letting image cropping happen accidentally
- [MDN: text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap)
  - useful for title discipline, especially when protecting single-line or balanced titles in bounded slides

## Recommended Combined Pipeline

### For `.pptx`

1. extract object-layer text, notes, images, and coordinates
2. render every slide visually
3. compare object regions with the rendered slide
4. classify groups, connectors, and tables by authoring intent
5. keep a region map, composition graph, and confidence report
6. then model logic and rebuild

### For `.pdf`

1. extract text and images with a PDF tool
2. render each page
3. classify layout and region types visually
4. annotate diagram grammar and media fit constraints
5. slice reusable assets
6. redraw diagrams only after their logic is described in words

### For screenshots

1. treat the screenshot as the composition truth
2. detect regions and OCR text
3. mark diagram primitives, full-frame media, and safe-crop candidates separately
4. slice reusable assets
5. infer layout and hierarchy conservatively
6. mark low-confidence areas instead of inventing structure

## Red Flags

- title area inferred only from OCR without looking at the full page
- diagrams treated as ordinary images without logic notes
- overlap or venn relationships reduced to disconnected shapes
- contact sheets, boards, or image strips cropped with no record of what was lost
- gallery cards rebuilt with inconsistent media windows even though the source compares them side by side
- transparent-border tables rebuilt as visible HTML tables
- format-only groups preserved as semantic containers
- semantic composite groups flattened into unrelated DOM blocks
- low-confidence charts redrawn too early
- multiple slices exported with no lineage back to source page
- decorative fragments preserved while true proof objects are lost
