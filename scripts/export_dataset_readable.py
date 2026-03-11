#!/usr/bin/env python3
"""Export JSONL dataset to human-readable JSON and Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


def read_jsonl(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def write_pretty_json(path: Path, rows: List[Dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def write_markdown(path: Path, rows: List[Dict[str, str]], title: str) -> None:
    lines: List[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- Total samples: {len(rows)}")
    lines.append("")
    for i, row in enumerate(rows, start=1):
        lines.append(f"## {i}. {row.get('id', '-')}")
        lines.append("")
        lines.append(f"- task_type: `{row.get('task_type', '-')}`")
        lines.append(f"- source_case_id: `{row.get('source_case_id', '-')}`")
        lines.append("")
        lines.append("### instruction")
        lines.append("")
        lines.append("```text")
        lines.append(row.get("instruction", ""))
        lines.append("```")
        lines.append("")
        lines.append("### input")
        lines.append("")
        lines.append("```text")
        lines.append(row.get("input", ""))
        lines.append("```")
        lines.append("")
        lines.append("### output")
        lines.append("")
        lines.append("```text")
        lines.append(row.get("output", ""))
        lines.append("```")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def export_one(jsonl_path: Path, output_dir: Path) -> None:
    rows = read_jsonl(jsonl_path)
    stem = jsonl_path.stem
    write_pretty_json(output_dir / f"{stem}_readable.json", rows)
    write_markdown(output_dir / f"{stem}_readable.md", rows, title=f"{stem} readable view")
    print(f"Exported: {stem} ({len(rows)} samples)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/processed/train_v1.jsonl")
    parser.add_argument("--val", default="data/processed/val_v1.jsonl")
    parser.add_argument("--output_dir", default="data/processed")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    export_one(Path(args.train), output_dir)
    export_one(Path(args.val), output_dir)


if __name__ == "__main__":
    main()
