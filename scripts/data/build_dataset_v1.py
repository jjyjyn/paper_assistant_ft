#!/usr/bin/env python3
"""Build v1 SFT dataset from structured paper cases."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Set, Tuple

FINAL_ONLY_RULE = (
    "只输出最终答案，不要输出任何思考过程、分析过程、自我提示或 `<think>` / "
    "`</think>` 标记。不要解释你在做什么，不要补充题外话。"
)

CONTRIBUTION_TEMPLATE = "\n".join(
    [
        "请按固定结构概括论文贡献。",
        "输出必须严格只包含以下四行，标签和顺序不得改变：",
        "核心问题: ...",
        "方法要点: ...",
        "相对基线增益: ...",
        "局限性: ...",
        FINAL_ONLY_RULE,
    ]
)

COMPARISON_TEMPLATE = "\n".join(
    [
        "请对论文方法与基线做结构化对比。",
        "输出必须严格只包含以下六行，标签和顺序不得改变：",
        "对比对象: ...",
        "新方法机制: ...",
        "主要优势: ...",
        "量化结果: ...",
        "代价与风险: ...",
        "结论: ...",
        FINAL_ONLY_RULE,
    ]
)

EXPERIMENT_TEMPLATE = "\n".join(
    [
        "请解释实验结果的含义，不要只重复数字。",
        "输出必须严格只包含以下四行，标签和顺序不得改变：",
        "结论: ...",
        "原因: ...",
        "边界: ...",
        "建议: ...",
        FINAL_ONLY_RULE,
    ]
)

FOLLOWUP_TEMPLATE = "\n".join(
    [
        "请模拟答辩老师追问，给出 3 组问答。",
        "输出必须严格只包含以下六行，标签和顺序不得改变：",
        "Q1: ...",
        "A1: ...",
        "Q2: ...",
        "A2: ...",
        "Q3: ...",
        "A3: ...",
        FINAL_ONLY_RULE,
    ]
)


def make_input(case: Dict[str, str]) -> str:
    return (
        f"论文标题: {case['title']}\n"
        f"研究问题: {case['problem']}\n"
        f"核心方法: {case['method']}\n"
        f"对比基线: {case['baseline']}\n"
        f"实验结果: {case['result']}\n"
        f"局限性: {case['limitations']}"
    )


def sample_contribution(case: Dict[str, str]) -> Dict[str, str]:
    return {
        "task_type": "contribution_extraction",
        "instruction": CONTRIBUTION_TEMPLATE,
        "input": make_input(case),
        "output": "\n".join(
            [
                f"核心问题: {case['problem']}",
                f"方法要点: {case['method']}",
                f"相对基线增益: 相对 {case['baseline']}，{case['result']}",
                f"局限性: {case['limitations']}",
            ]
        ),
    }


def sample_comparison(case: Dict[str, str]) -> Dict[str, str]:
    return {
        "task_type": "method_comparison",
        "instruction": COMPARISON_TEMPLATE,
        "input": make_input(case),
        "output": "\n".join(
            [
                f"对比对象: {case['baseline']}",
                f"新方法机制: {case['method']}",
                "主要优势: 更直接对齐任务核心瓶颈，提升关键信息利用效率。",
                f"量化结果: {case['result']}",
                f"代价与风险: {case['limitations']}",
                "结论: 新方法带来明确收益，但收益与代价需要结合应用场景综合评估。",
            ]
        ),
    }


def sample_experiment(case: Dict[str, str]) -> Dict[str, str]:
    return {
        "task_type": "experiment_interpretation",
        "instruction": EXPERIMENT_TEMPLATE,
        "input": make_input(case),
        "output": "\n".join(
            [
                f"结论: {case['result']} 说明该方法在目标任务上取得了可观提升。",
                f"原因: 关键原因在于 {case['method']} 更直接缓解了 {case['problem']}",
                f"边界: {case['limitations']}",
                "建议: 后续应补充效率、鲁棒性和跨域验证，确认收益是否稳定成立。",
            ]
        ),
    }


def sample_followup(case: Dict[str, str]) -> Dict[str, str]:
    return {
        "task_type": "defense_followup",
        "instruction": FOLLOWUP_TEMPLATE,
        "input": make_input(case),
        "output": "\n".join(
            [
                "Q1: 你的方法相对基线真正新增了什么？",
                f"A1: 新增点是 {case['method']}，它针对 {case['problem']} 做了机制级改造，而不是简单复用已有流程。",
                "Q2: 实验提升是否足够支撑你的结论？",
                f"A2: 从结果 {case['result']} 看，提升方向是明确的，但仍应补充更多切分、显著性或误差分析来增强说服力。",
                "Q3: 这个方法的短板是什么，怎么改？",
                f"A3: 当前短板是 {case['limitations']}。下一步可从更稳的数据覆盖、结构约束或轻量化设计继续优化。",
            ]
        ),
    }


def build_samples(cases: List[Dict[str, str]]) -> List[Dict[str, str]]:
    builders = [
        sample_contribution,
        sample_comparison,
        sample_experiment,
        sample_followup,
    ]
    rows: List[Dict[str, str]] = []
    idx = 1
    for case in cases:
        for fn in builders:
            row = fn(case)
            row["id"] = f"v1_{idx:04d}"
            row["source_case_id"] = case["case_id"]
            rows.append(row)
            idx += 1
    return rows


def split_rows_by_case(
    rows: List[Dict[str, str]],
    val_ratio: float,
    test_ratio: float,
    seed: int,
) -> Tuple[
    List[Dict[str, str]],
    List[Dict[str, str]],
    List[Dict[str, str]],
    Set[str],
    Set[str],
    Set[str],
]:
    if not (0 <= val_ratio < 1):
        raise ValueError(f"val_ratio must be in [0, 1), got {val_ratio}")
    if not (0 <= test_ratio < 1):
        raise ValueError(f"test_ratio must be in [0, 1), got {test_ratio}")
    if val_ratio + test_ratio >= 1:
        raise ValueError(
            f"val_ratio + test_ratio must be < 1, got {val_ratio + test_ratio}"
        )

    case_ids = sorted({row["source_case_id"] for row in rows})
    if len(case_ids) < 3:
        raise ValueError("Need at least 3 cases for train/val/test split.")

    rng = random.Random(seed)
    rng.shuffle(case_ids)

    n_cases = len(case_ids)
    n_val = max(1, int(round(n_cases * val_ratio))) if val_ratio > 0 else 0
    n_test = max(1, int(round(n_cases * test_ratio))) if test_ratio > 0 else 0

    while n_val + n_test >= n_cases and n_test > 0:
        n_test -= 1
    while n_val + n_test >= n_cases and n_val > 0:
        n_val -= 1
    if n_val + n_test >= n_cases:
        raise ValueError("Invalid split ratios; no case left for train split.")

    val_case_ids = set(case_ids[:n_val])
    test_case_ids = set(case_ids[n_val : n_val + n_test])
    train_case_ids = set(case_ids[n_val + n_test :])

    train_rows = [row for row in rows if row["source_case_id"] in train_case_ids]
    val_rows = [row for row in rows if row["source_case_id"] in val_case_ids]
    test_rows = [row for row in rows if row["source_case_id"] in test_case_ids]

    rng.shuffle(train_rows)
    rng.shuffle(val_rows)
    rng.shuffle(test_rows)

    return train_rows, val_rows, test_rows, train_case_ids, val_case_ids, test_case_ids


def write_jsonl(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cases",
        default="data/raw/paper_cases_v1.json",
        help="Path to structured case json file.",
    )
    parser.add_argument(
        "--train_out",
        default="data/processed/train_v1.jsonl",
        help="Output training jsonl path.",
    )
    parser.add_argument(
        "--val_out",
        default="data/processed/val_v1.jsonl",
        help="Output validation jsonl path.",
    )
    parser.add_argument(
        "--test_out",
        default="data/processed/test_v1.jsonl",
        help="Output test jsonl path.",
    )
    parser.add_argument(
        "--val_ratio", type=float, default=0.1, help="Validation ratio at case level."
    )
    parser.add_argument(
        "--test_ratio", type=float, default=0.1, help="Test ratio at case level."
    )
    parser.add_argument("--seed", type=int, default=20260311, help="Random seed.")
    args = parser.parse_args()

    cases_path = Path(args.cases)
    with cases_path.open("r", encoding="utf-8") as f:
        cases = json.load(f)

    rows = build_samples(cases)
    (
        train_rows,
        val_rows,
        test_rows,
        train_case_ids,
        val_case_ids,
        test_case_ids,
    ) = split_rows_by_case(
        rows=rows,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
        seed=args.seed,
    )

    write_jsonl(Path(args.train_out), train_rows)
    write_jsonl(Path(args.val_out), val_rows)
    write_jsonl(Path(args.test_out), test_rows)

    print(f"Loaded cases: {len(cases)}")
    print(f"Built samples: {len(rows)}")
    print("Split strategy: case-level (no source_case_id leakage)")
    print(f"Train cases: {len(train_case_ids)}")
    print(f"Val cases: {len(val_case_ids)}")
    print(f"Test cases: {len(test_case_ids)}")
    print(f"Train samples: {len(train_rows)} -> {args.train_out}")
    print(f"Val samples: {len(val_rows)} -> {args.val_out}")
    print(f"Test samples: {len(test_rows)} -> {args.test_out}")


if __name__ == "__main__":
    main()
