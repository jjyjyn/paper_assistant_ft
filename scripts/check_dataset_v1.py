#!/usr/bin/env python3
"""Validate v1 jsonl dataset files."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
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
    case_tasks = defaultdict(set)

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
        case_tasks[row["source_case_id"]].add(row["task_type"])

    for case_id, tasks in case_tasks.items():
        if tasks != VALID_TASKS:
            missing = sorted(VALID_TASKS - tasks)
            raise ValueError(
                f"{name} case {case_id} task coverage invalid: missing={missing}"
            )

    print(f"[{name}] rows={len(rows)}")
    print(f"[{name}] cases={len(case_tasks)}")
    for task in sorted(VALID_TASKS):
        print(f"[{name}] {task}={task_counter[task]}")


def assert_no_overlap(
    rows_a: List[Dict[str, str]],
    rows_b: List[Dict[str, str]],
    name_a: str,
    name_b: str,
    field: str,
) -> None:
    set_a = {row[field] for row in rows_a}
    set_b = {row[field] for row in rows_b}
    overlap = set_a & set_b
    if overlap:
        sample = sorted(overlap)[:5]
        raise ValueError(
            f"Leakage detected between {name_a}/{name_b} on field={field}, "
            f"overlap_count={len(overlap)}, examples={sample}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/processed/train_v1.jsonl")
    parser.add_argument("--val", default="data/processed/val_v1.jsonl")
    parser.add_argument("--test", default="data/processed/test_v1.jsonl")
    args = parser.parse_args()

    train_rows = read_jsonl(Path(args.train))
    val_rows = read_jsonl(Path(args.val))
    test_rows = read_jsonl(Path(args.test))

    validate(train_rows, "train")
    validate(val_rows, "val")
    validate(test_rows, "test")

    # No duplicate IDs across splits.
    assert_no_overlap(train_rows, val_rows, "train", "val", "id")
    assert_no_overlap(train_rows, test_rows, "train", "test", "id")
    assert_no_overlap(val_rows, test_rows, "val", "test", "id")

    # No source case leakage across splits.
    assert_no_overlap(train_rows, val_rows, "train", "val", "source_case_id")
    assert_no_overlap(train_rows, test_rows, "train", "test", "source_case_id")
    assert_no_overlap(val_rows, test_rows, "val", "test", "source_case_id")

    print("Dataset check passed.")


if __name__ == "__main__":
    main()
