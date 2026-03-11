#!/usr/bin/env python3
"""Validate external evaluation dataset and check overlap risks."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List

REQUIRED_FIELDS = {
    "id",
    "task_type",
    "instruction",
    "input",
    "output",
    "source_case_id",
    "split",
}
VALID_TASKS = {
    "contribution_extraction",
    "method_comparison",
    "experiment_interpretation",
    "defense_followup",
}


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", "", text)
    return text


def read_json(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_jsonl(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
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


def validate_external_rows(rows: List[Dict[str, str]]) -> None:
    seen_ids = set()
    task_counter = Counter()
    case_tasks = defaultdict(set)

    for idx, row in enumerate(rows, start=1):
        missing = REQUIRED_FIELDS - set(row.keys())
        if missing:
            raise ValueError(f"external row {idx} missing fields: {sorted(missing)}")

        if row["id"] in seen_ids:
            raise ValueError(f"external duplicate id: {row['id']}")
        seen_ids.add(row["id"])

        if row["task_type"] not in VALID_TASKS:
            raise ValueError(f"external row {idx} invalid task_type: {row['task_type']}")

        if row["split"] != "external_test":
            raise ValueError(f"external row {idx} split must be external_test")

        for f in ("instruction", "input", "output", "source_case_id"):
            if not isinstance(row[f], str) or not row[f].strip():
                raise ValueError(f"external row {idx} invalid {f}: empty")

        task_counter[row["task_type"]] += 1
        case_tasks[row["source_case_id"]].add(row["task_type"])

    for case_id, tasks in case_tasks.items():
        if tasks != VALID_TASKS:
            missing = sorted(VALID_TASKS - tasks)
            raise ValueError(f"external case {case_id} task coverage invalid: missing={missing}")

    print(f"[external] rows={len(rows)}")
    print(f"[external] cases={len(case_tasks)}")
    for task in sorted(VALID_TASKS):
        print(f"[external] {task}={task_counter[task]}")


def validate_no_case_overlap(
    external_cases: List[Dict[str, str]],
    train_cases: List[Dict[str, str]],
) -> None:
    ext_ids = {x["case_id"] for x in external_cases}
    train_ids = {x["case_id"] for x in train_cases}
    case_overlap = ext_ids & train_ids
    if case_overlap:
        raise ValueError(f"case_id overlap detected: {sorted(case_overlap)}")

    ext_titles = {normalize_text(x["title"]) for x in external_cases}
    train_titles = {normalize_text(x["title"]) for x in train_cases}
    title_overlap = ext_titles & train_titles
    if title_overlap:
        raise ValueError(
            "title overlap detected between external/train raw cases "
            f"(count={len(title_overlap)})"
        )

    print("[external] overlap check passed (case_id/title)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--external_cases",
        default="data/external_eval/raw/external_eval_cases_v1.json",
    )
    parser.add_argument("--train_cases", default="data/raw/paper_cases_v1.json")
    parser.add_argument(
        "--external_jsonl",
        default="data/external_eval/processed/external_eval_v1.jsonl",
    )
    args = parser.parse_args()

    external_cases = read_json(Path(args.external_cases))
    train_cases = read_json(Path(args.train_cases))
    external_rows = read_jsonl(Path(args.external_jsonl))

    validate_external_rows(external_rows)
    validate_no_case_overlap(external_cases, train_cases)
    print("External eval check passed.")


if __name__ == "__main__":
    main()
