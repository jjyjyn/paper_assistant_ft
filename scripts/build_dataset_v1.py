#!/usr/bin/env python3
"""Build v1 SFT dataset from structured paper cases.

Input:
  data/raw/paper_cases_v1.json

Outputs:
  data/processed/train_v1.jsonl
  data/processed/val_v1.jsonl
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Dict, List


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
        "instruction": "你是论文精读助手。请提取该论文的核心贡献，要求条目化且可用于答辩复述。",
        "input": make_input(case),
        "output": (
            "核心贡献可归纳为三点:\n"
            f"1) 针对“{case['problem']}”这一痛点，论文提出了可落地的解决框架。\n"
            f"2) 方法创新在于“{case['method']}”，相比常规方案具备更强任务适配性。\n"
            f"3) 实验上相对基线（{case['baseline']}）取得明确提升：{case['result']}。\n"
            f"同时作者也坦诚局限：{case['limitations']}，为后续改进留出方向。"
        ),
    }


def sample_comparison(case: Dict[str, str]) -> Dict[str, str]:
    return {
        "task_type": "method_comparison",
        "instruction": "你是方法对比助手。请对该方法与基线方法做结构化对比，突出“为何更好”和“代价是什么”。",
        "input": make_input(case),
        "output": (
            "方法对比如下:\n"
            f"- 对比对象: {case['baseline']}\n"
            f"- 新方法机制: {case['method']}\n"
            "- 主要优势: 更贴合任务关键瓶颈，能在检索/推理/解释链路上提升有效信息利用率。\n"
            f"- 量化结果: {case['result']}\n"
            f"- 代价与风险: {case['limitations']}\n"
            "- 结论: 该方法不是“无代价变好”，而是在性能与效率之间做了更优平衡。"
        ),
    }


def sample_experiment(case: Dict[str, str]) -> Dict[str, str]:
    return {
        "task_type": "experiment_interpretation",
        "instruction": "你是实验解析助手。请解释实验结果意味着什么，要求给出“结论-原因-边界”。",
        "input": make_input(case),
        "output": (
            f"结论: 结果“{case['result']}”说明该方法在目标任务上具备实质增益。\n"
            f"原因: 关键在于“{case['method']}”能够更好地缓解“{case['problem']}”。\n"
            f"边界: 作者给出的局限是“{case['limitations']}”，这意味着在资源受限或域迁移场景中收益可能下降。\n"
            "建议: 后续应补充效率对比与跨域验证，以确认方法的泛化稳定性。"
        ),
    }


def sample_followup(case: Dict[str, str]) -> Dict[str, str]:
    return {
        "task_type": "defense_followup",
        "instruction": "你是答辩追问助手。请模拟老师追问并给出高质量回答，至少包含3组问答。",
        "input": make_input(case),
        "output": (
            "Q1: 你的方法相对基线真正新增了什么？\n"
            f"A1: 新增点是“{case['method']}”，核心不是简单堆模块，而是针对“{case['problem']}”做了机制级改造。\n\n"
            "Q2: 实验提升是否足够支撑你的结论？\n"
            f"A2: 从结果“{case['result']}”看，提升具有一致性，但我会补充不同数据切分与统计显著性检验来增强结论可信度。\n\n"
            "Q3: 这个方法的短板是什么，怎么改？\n"
            f"A3: 已知短板是“{case['limitations']}”。下一步可通过轻量化设计、蒸馏或缓存机制降低额外开销。"
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
    parser.add_argument("--val_ratio", type=float, default=0.1, help="Validation ratio.")
    parser.add_argument("--seed", type=int, default=20260311, help="Random seed.")
    args = parser.parse_args()

    cases_path = Path(args.cases)
    with cases_path.open("r", encoding="utf-8") as f:
        cases = json.load(f)

    rows = build_samples(cases)
    # Stratified split by task_type to keep all task types in train/val.
    random.seed(args.seed)
    buckets = defaultdict(list)
    for row in rows:
        buckets[row["task_type"]].append(row)

    val_rows = []
    train_rows = []
    for task, task_rows in buckets.items():
        random.shuffle(task_rows)
        n_val = max(1, int(len(task_rows) * args.val_ratio))
        val_rows.extend(task_rows[:n_val])
        train_rows.extend(task_rows[n_val:])

    random.shuffle(train_rows)
    random.shuffle(val_rows)

    write_jsonl(Path(args.train_out), train_rows)
    write_jsonl(Path(args.val_out), val_rows)

    print(f"Loaded cases: {len(cases)}")
    print(f"Built samples: {len(rows)}")
    print(f"Train samples: {len(train_rows)} -> {args.train_out}")
    print(f"Val samples: {len(val_rows)} -> {args.val_out}")


if __name__ == "__main__":
    main()
