#!/usr/bin/env python3
"""Validate v1 jsonl dataset files."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List

REQUIRED_FIELDS = {"id", "task_type", "instruction", "input", "output", "source_case_id"}
VALID_TASKS = {
    "contribution_extraction",
    "method_comparison",
    "experiment_interpretation",
    "defense_followup",
}


def read_jsonl(path: Path) -> List[Dict[str, str]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"{path}:{i} invalid json: {e}") from e
            rows.append(row)
    return rows


def validate(rows: List[Dict[str, str]], name: str) -> None:
    seen_ids = set()
    task_counter = Counter()

    for idx, row in enumerate(rows, start=1):
        missing = REQUIRED_FIELDS - set(row.keys())
        if missing:
            raise ValueError(f"{name} row {idx} missing fields: {sorted(missing)}")

        if row["id"] in seen_ids:
            raise ValueError(f"{name} duplicate id: {row['id']}")
        seen_ids.add(row["id"])

        if row["task_type"] not in VALID_TASKS:
            raise ValueError(f"{name} row {idx} invalid task_type: {row['task_type']}")

        for f in ("instruction", "input", "output"):
            if not isinstance(row[f], str) or not row[f].strip():
                raise ValueError(f"{name} row {idx} invalid {f}: empty")

        task_counter[row["task_type"]] += 1

    print(f"[{name}] rows={len(rows)}")
    for task in sorted(VALID_TASKS):
        print(f"[{name}] {task}={task_counter[task]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/processed/train_v1.jsonl")
    parser.add_argument("--val", default="data/processed/val_v1.jsonl")
    args = parser.parse_args()

    train_rows = read_jsonl(Path(args.train))
    val_rows = read_jsonl(Path(args.val))

    validate(train_rows, "train")
    validate(val_rows, "val")
    print("Dataset check passed.")


if __name__ == "__main__":
    main()
