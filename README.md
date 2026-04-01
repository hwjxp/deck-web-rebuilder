# Deck Web Rebuilder

`deck-web-rebuilder` is a Codex skill for turning existing presentation decks into faithful, interactive web presentations without losing the original message, slide logic, or essential text-image relationships.

The workflow is intentionally top-down:

1. Read the entire deck first.
2. Understand the theme, audience, occasion, and persuasion goal.
3. Build the storyline and slide logic.
4. Clean and classify visual assets.
5. Decide fidelity and style strategy.
6. Rebuild the deck for the web.
7. Run visual and logical QA before delivery.

This skill is designed for `.ppt`, `.pptx`, `.key`, and exported `.pdf` sources, especially when the rebuilt output needs:

- faithful slide-by-slide web conversion
- bilingual copy support
- navigation and deep links
- diagram redraws
- animation
- PDF export

## Repository Layout

```text
deck-web-rebuilder/
├── SKILL.md
├── README.md
├── .gitignore
├── agents/
│   └── openai.yaml
├── references/
│   ├── artifacts.md
│   ├── fidelity-checks.md
│   └── style-judgment.md
└── scripts/
    ├── check_stage_gates.py
    └── prepare_rebuild_workspace.sh
```

## What The Skill Enforces

- no slide-by-slide editing before full-deck understanding
- storyline before layout
- layout before content fill
- asset handling as structured data cleaning
- preservation of necessary logic and rhetorical intent
- stage gates before rebuild
- visual QA and logical QA before handoff

## Quick Start

Prepare a rebuild workspace:

```bash
bash scripts/prepare_rebuild_workspace.sh /path/to/input-deck.pptx
```

Check whether the analysis stage artifacts are complete enough to continue:

```bash
python3 scripts/check_stage_gates.py /path/to/workspace
```

## Core References

- `SKILL.md`: main operating instructions
- `references/artifacts.md`: required stage outputs and gate rules
- `references/style-judgment.md`: how to infer visual direction from context
- `references/fidelity-checks.md`: what must remain faithful during rebuild

## Publishing

This repository contains the reusable skill itself. The generated web decks belong in separate task workspaces created per input presentation.
