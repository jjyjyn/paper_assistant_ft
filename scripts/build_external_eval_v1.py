#!/usr/bin/env python3
"""Build external evaluation dataset (v1) from independent cases.

Input:
  data/external_eval/raw/external_eval_cases_v1.json

Outputs:
  data/external_eval/processed/external_eval_v1.jsonl
  data/external_eval/processed/external_eval_v1_readable.json
  data/external_eval/processed/external_eval_v1_readable.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

TASKS = [
    "contribution_extraction",
    "method_comparison",
    "experiment_interpretation",
    "defense_followup",
]


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
        "instruction": "请提炼该工作最关键的三点贡献，要求分别覆盖问题、方法创新和结果价值。",
        "input": make_input(case),
        "output": (
            "核心贡献可归纳为三点:\n"
            f"1) 问题导向: 聚焦“{case['problem']}”这一高频痛点，并给出可落地方案。\n"
            f"2) 方法创新: 采用“{case['method']}”，在信息利用效率上优于常规路径。\n"
            f"3) 结果价值: 相比“{case['baseline']}”，实验显示“{case['result']}”。\n"
            f"同时需注意作者给出的边界条件“{case['limitations']}”。"
        ),
    }


def sample_comparison(case: Dict[str, str]) -> Dict[str, str]:
    return {
        "task_type": "method_comparison",
        "instruction": "请做结构化方法对比，说明新方法为何更优，以及代价和风险。",
        "input": make_input(case),
        "output": (
            "方法对比如下:\n"
            f"- 对比对象: {case['baseline']}\n"
            f"- 新方法机制: {case['method']}\n"
            "- 主要优势: 对目标瓶颈更有针对性，通常能提高有效证据利用率和推理稳定性。\n"
            f"- 量化结果: {case['result']}\n"
            f"- 代价与风险: {case['limitations']}\n"
            "- 结论: 该方法体现的是“性能-成本-鲁棒性”之间的再平衡，而非无代价提升。"
        ),
    }


def sample_experiment(case: Dict[str, str]) -> Dict[str, str]:
    return {
        "task_type": "experiment_interpretation",
        "instruction": "请用“结论-原因-边界”解释实验结果，并给出后续验证建议。",
        "input": make_input(case),
        "output": (
            f"结论: “{case['result']}”说明该方法在目标任务上具有可观收益。\n"
            f"原因: 收益主要来自“{case['method']}”，其机制上更直接缓解了“{case['problem']}”。\n"
            f"边界: “{case['limitations']}”提示该方法在特定场景下可能退化。\n"
            "建议: 进一步补充跨域实验与资源受限条件下的稳定性验证。"
        ),
    }


def sample_followup(case: Dict[str, str]) -> Dict[str, str]:
    return {
        "task_type": "defense_followup",
        "instruction": "请模拟答辩追问，给出 3 组高质量问答，聚焦创新性、证据充分性和局限改进。",
        "input": make_input(case),
        "output": (
            "Q1: 你相对基线的真正创新是什么？\n"
            f"A1: 创新点在于“{case['method']}”，它不是简单叠加模块，而是直接针对“{case['problem']}”的机制级改造。\n\n"
            "Q2: 你的实验是否足以支撑结论？\n"
            f"A2: 从结果“{case['result']}”看，收益方向明确；但仍需更多跨场景验证以增强结论外推性。\n\n"
            "Q3: 已知局限是什么，下一步怎么改？\n"
            f"A3: 当前主要局限是“{case['limitations']}”。下一步应优先做失效场景分析与针对性鲁棒性增强。"
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
