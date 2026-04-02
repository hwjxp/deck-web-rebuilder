#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
PAGE_SPECS_JSON = Path("40-rebuild/page-specs.json")
DESIGN_SYSTEM_JSON = Path("35-strategy/deck-design-system.json")
PAGE_SCHEMA = SKILL_ROOT / "schemas/page-spec.schema.json"
DESIGN_SCHEMA = SKILL_ROOT / "schemas/deck-design-system.schema.json"


def load_json_file(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_workspace_json(workspace: Path, relative_path: Path) -> Any:
    path = workspace / relative_path
    if not path.exists():
        raise FileNotFoundError(path)
    return load_json_file(path)


def maybe_validate_with_jsonschema(data: Any, schema_path: Path) -> list[str]:
    try:
        import jsonschema
    except ImportError:
        return []

    schema = load_json_file(schema_path)
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"{'/'.join(str(bit) for bit in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path))
    ]


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\W_]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def english_word_count(text: str) -> int:
    return len([part for part in re.split(r"\s+", text.strip()) if part])


def chinese_char_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def text_blocks_for_slide(slide: dict[str, Any]) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    title = slide.get("title", {}).get("text", {})
    takeaway = slide.get("takeaway", {})
    for lang in ("en", "zh"):
        if title.get(lang):
            blocks.append((f"title.{lang}", title[lang]))
        if takeaway.get(lang):
            blocks.append((f"takeaway.{lang}", takeaway[lang]))
    for block in slide.get("body_blocks", []):
        copy = block.get("copy", {})
        for lang in ("en", "zh"):
            if copy.get(lang):
                blocks.append((f"{block.get('id', 'block')}.{lang}", copy[lang]))
    return blocks
