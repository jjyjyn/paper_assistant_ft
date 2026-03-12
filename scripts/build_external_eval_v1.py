#!/usr/bin/env python3
"""Build external evaluation dataset (v1) from independent cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

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


BUILDERS = [
    sample_contribution,
    sample_comparison,
    sample_experiment,
    sample_followup,
]


def build_samples(cases: List[Dict[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    idx = 1
    for case in cases:
        for fn in BUILDERS:
            row = fn(case)
            row["id"] = f"ext_v1_{idx:04d}"
            row["source_case_id"] = case["case_id"]
            row["split"] = "external_test"
            rows.append(row)
            idx += 1
    return rows


def write_jsonl(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_pretty_json(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def write_markdown(path: Path, rows: List[Dict[str, str]]) -> None:
    lines: List[str] = []
    lines.append("# external_eval_v1 readable view")
    lines.append("")
    lines.append(f"- Total samples: {len(rows)}")
    lines.append("")
    for i, row in enumerate(rows, start=1):
        lines.append(f"## {i}. {row['id']}")
        lines.append("")
        lines.append(f"- task_type: `{row['task_type']}`")
        lines.append(f"- source_case_id: `{row['source_case_id']}`")
        lines.append(f"- split: `{row['split']}`")
        lines.append("")
        lines.append("### instruction")
        lines.append("")
        lines.append("```text")
        lines.append(row["instruction"])
        lines.append("```")
        lines.append("")
        lines.append("### input")
        lines.append("")
        lines.append("```text")
        lines.append(row["input"])
        lines.append("```")
        lines.append("")
        lines.append("### output")
        lines.append("")
        lines.append("```text")
        lines.append(row["output"])
        lines.append("```")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cases",
        default="data/external_eval/raw/external_eval_cases_v1.json",
        help="Path to external case file.",
    )
    parser.add_argument(
        "--out_jsonl",
        default="data/external_eval/processed/external_eval_v1.jsonl",
        help="Output jsonl path.",
    )
    parser.add_argument(
        "--out_readable_json",
        default="data/external_eval/processed/external_eval_v1_readable.json",
        help="Readable json output path.",
    )
    parser.add_argument(
        "--out_readable_md",
        default="data/external_eval/processed/external_eval_v1_readable.md",
        help="Readable markdown output path.",
    )
    args = parser.parse_args()

    with Path(args.cases).open("r", encoding="utf-8") as f:
        cases = json.load(f)

    rows = build_samples(cases)
    write_jsonl(Path(args.out_jsonl), rows)
    write_pretty_json(Path(args.out_readable_json), rows)
    write_markdown(Path(args.out_readable_md), rows)

    print(f"Loaded external cases: {len(cases)}")
    print(f"Built external samples: {len(rows)}")
    print(f"Output jsonl: {args.out_jsonl}")


if __name__ == "__main__":
    main()
