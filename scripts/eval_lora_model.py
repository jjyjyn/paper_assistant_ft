#!/usr/bin/env python3
"""Run generation-based evaluation for a LoRA adapter on JSONL datasets."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REQUIRED_PREFIXES = {
    "contribution_extraction": [
        "核心问题:",
        "方法要点:",
        "相对基线增益:",
        "局限性:",
    ],
    "method_comparison": [
        "对比对象:",
        "新方法机制:",
        "主要优势:",
        "量化结果:",
        "代价与风险:",
        "结论:",
    ],
    "experiment_interpretation": [
        "结论:",
        "原因:",
        "边界:",
        "建议:",
    ],
    "defense_followup": [
        "Q1:",
        "A1:",
        "Q2:",
        "A2:",
        "Q3:",
        "A3:",
    ],
}

SYSTEM_PROMPT_NO_THINK = (
    "你必须只输出最终答案。"
    "禁止输出任何思考过程、分析过程、推理痕迹，"
    "禁止输出 <think> 或 </think>。"
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def normalize_text(text: str) -> str:
    return "".join(text.split())


def char_f1_score(prediction: str, reference: str) -> float:
    pred_norm = normalize_text(prediction)
    ref_norm = normalize_text(reference)
    if not pred_norm and not ref_norm:
        return 1.0
    if not pred_norm or not ref_norm:
        return 0.0

    pred_counter = Counter(pred_norm)
    ref_counter = Counter(ref_norm)
    overlap = sum((pred_counter & ref_counter).values())
    if overlap == 0:
        return 0.0

    precision = overlap / sum(pred_counter.values())
    recall = overlap / sum(ref_counter.values())
    return 2 * precision * recall / (precision + recall)


def exact_match(prediction: str, reference: str) -> bool:
    return normalize_text(prediction) == normalize_text(reference)


def build_user_prompt(instruction: str, input_text: str) -> str:
    instruction = instruction.strip()
    input_text = input_text.strip()
    if instruction and input_text:
        return f"{instruction}\n\n{input_text}"
    return instruction or input_text


def strip_think_content(text: str) -> str:
    text = text.strip()
    if not text:
        return text

    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    if text.startswith("<think>"):
        return ""
    return text.strip()


def structure_ok(task_type: str, prediction: str) -> bool:
    prefixes = REQUIRED_PREFIXES.get(task_type)
    if not prefixes:
        return False

    lines = [line.strip() for line in prediction.splitlines() if line.strip()]
    if len(lines) != len(prefixes):
        return False

    for line, prefix in zip(lines, prefixes):
        if not line.startswith(prefix):
            return False
        if not line[len(prefix) :].strip():
            return False

    return True


def generate_prediction(
    model: Any,
    tokenizer: Any,
    instruction: str,
    input_text: str,
    max_new_tokens: int,
    disable_thinking: bool,
) -> tuple[str, str, str]:
    import torch

    user_prompt = build_user_prompt(instruction, input_text)
    messages: list[dict[str, str]] = []
    if disable_thinking:
        messages.append({"role": "system", "content": SYSTEM_PROMPT_NO_THINK})
    messages.append({"role": "user", "content": user_prompt})

    chat_kwargs = {
        "add_generation_prompt": True,
        "tokenize": True,
        "return_tensors": "pt",
    }
    thinking_control_mode = "default"
    if disable_thinking:
        try:
            inputs = tokenizer.apply_chat_template(
                messages,
                enable_thinking=False,
                **chat_kwargs,
            )
            thinking_control_mode = "chat_template_enable_thinking_false"
        except TypeError:
            # Fallback for tokenizers without `enable_thinking` argument.
            messages[-1]["content"] = f"{messages[-1]['content']}\n\n/no_think"
            inputs = tokenizer.apply_chat_template(messages, **chat_kwargs)
            thinking_control_mode = "prompt_no_think_fallback"
    else:
        inputs = tokenizer.apply_chat_template(messages, **chat_kwargs)

    if torch.cuda.is_available():
        inputs = inputs.to("cuda")

    with torch.no_grad():
        output_ids = model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
            top_p=None,
            top_k=None,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    new_tokens = output_ids[0, inputs.shape[-1] :]
    raw_prediction = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    cleaned_prediction = strip_think_content(raw_prediction)
    return raw_prediction, cleaned_prediction, thinking_control_mode


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def save_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def save_markdown(path: Path, rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append(f"# Evaluation Report: {summary['dataset_name']}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- total: {summary['overall']['count']}")
    lines.append(f"- exact_match_rate: {summary['overall']['exact_match_rate']:.4f}")
    lines.append(f"- avg_char_f1: {summary['overall']['avg_char_f1']:.4f}")
    lines.append(f"- empty_prediction_rate: {summary['overall']['empty_prediction_rate']:.4f}")
    lines.append(f"- raw_think_rate: {summary['overall']['raw_think_rate']:.4f}")
    lines.append(f"- cleaned_changed_rate: {summary['overall']['cleaned_changed_rate']:.4f}")
    lines.append(f"- structure_ok_rate: {summary['overall']['structure_ok_rate']:.4f}")
    lines.append(f"- disable_thinking: {summary['disable_thinking']}")
    lines.append(f"- thinking_control_modes: `{', '.join(summary['thinking_control_modes'])}`")
    lines.append(f"- adapter_path: `{summary['adapter_path']}`")
    lines.append(f"- base_model_path: `{summary['base_model_path']}`")
    lines.append("")
    lines.append("## By Task Type")
    lines.append("")
    for task_type, metrics in summary["by_task_type"].items():
        lines.append(
            f"- {task_type}: count={metrics['count']}, "
            f"exact_match_rate={metrics['exact_match_rate']:.4f}, "
            f"avg_char_f1={metrics['avg_char_f1']:.4f}, "
            f"empty_prediction_rate={metrics['empty_prediction_rate']:.4f}, "
            f"raw_think_rate={metrics['raw_think_rate']:.4f}, "
            f"structure_ok_rate={metrics['structure_ok_rate']:.4f}"
        )

    for idx, row in enumerate(rows, start=1):
        lines.append("")
        lines.append(f"## Sample {idx}")
        lines.append("")
        lines.append(f"- id: `{row['id']}`")
        lines.append(f"- source_case_id: `{row.get('source_case_id', '')}`")
        lines.append(f"- task_type: `{row['task_type']}`")
        lines.append(f"- exact_match: `{row['exact_match']}`")
        lines.append(f"- char_f1: `{row['char_f1']:.4f}`")
        lines.append(f"- prediction_is_empty: `{row['prediction_is_empty']}`")
        lines.append(f"- raw_has_think: `{row['raw_has_think']}`")
        lines.append(f"- cleaned_changed: `{row['cleaned_changed']}`")
        lines.append(f"- structure_ok: `{row['structure_ok']}`")
        lines.append(f"- thinking_control_mode: `{row['thinking_control_mode']}`")
        lines.append("")
        lines.append("### Instruction")
        lines.append(row["instruction"])
        lines.append("")
        lines.append("### Input")
        lines.append(row["input"])
        lines.append("")
        lines.append("### Reference")
        lines.append(row["reference"])
        lines.append("")
        lines.append("### Prediction")
        lines.append(row["prediction"] if row["prediction"] else "<EMPTY>")
        if row.get("raw_prediction") and row["raw_prediction"] != row["prediction"]:
            lines.append("")
            lines.append("### Raw Prediction")
            lines.append(row["raw_prediction"])

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def summarize_bucket(bucket: list[dict[str, Any]]) -> dict[str, Any]:
    count = len(bucket)
    exact_matches = sum(1 for row in bucket if row["exact_match"])
    avg_char_f1 = sum(row["char_f1"] for row in bucket) / count if count else 0.0
    empty_predictions = sum(1 for row in bucket if row["prediction_is_empty"])
    raw_think = sum(1 for row in bucket if row["raw_has_think"])
    cleaned_changed = sum(1 for row in bucket if row["cleaned_changed"])
    structure_ok_count = sum(1 for row in bucket if row["structure_ok"])
    return {
        "count": count,
        "exact_match_rate": exact_matches / count if count else 0.0,
        "avg_char_f1": avg_char_f1,
        "empty_prediction_rate": empty_predictions / count if count else 0.0,
        "raw_think_rate": raw_think / count if count else 0.0,
        "cleaned_changed_rate": cleaned_changed / count if count else 0.0,
        "structure_ok_rate": structure_ok_count / count if count else 0.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a LoRA adapter on a JSONL dataset.")
    parser.add_argument("--base-model", required=True, help="Base model path.")
    parser.add_argument("--adapter-path", required=True, help="LoRA adapter output directory.")
    parser.add_argument("--dataset", required=True, help="Evaluation dataset JSONL path.")
    parser.add_argument("--output-jsonl", required=True, help="Prediction JSONL output path.")
    parser.add_argument("--output-summary", required=True, help="Summary JSON output path.")
    parser.add_argument("--output-md", required=True, help="Readable markdown report output path.")
    parser.add_argument("--max-new-tokens", type=int, default=384)
    parser.add_argument("--limit", type=int, default=0, help="Optional limit for debugging.")
    parser.add_argument(
        "--disable-thinking",
        action="store_true",
        help="Try to disable model thinking output via chat template/prompt controls.",
    )
    parser.add_argument(
        "--run-tag",
        default="",
        help="Optional run tag for audit and report traceability.",
    )
    args = parser.parse_args()

    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    dataset_path = Path(args.dataset)
    output_jsonl = Path(args.output_jsonl)
    output_summary = Path(args.output_summary)
    output_md = Path(args.output_md)

    records = load_jsonl(dataset_path)
    if args.limit > 0:
        records = records[: args.limit]

    tokenizer = AutoTokenizer.from_pretrained(args.base_model, trust_remote_code=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    base_model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        torch_dtype=dtype,
        trust_remote_code=True,
    )
    if hasattr(base_model, "generation_config"):
        base_model.generation_config.do_sample = False
        for attr in ("temperature", "top_p", "top_k"):
            if hasattr(base_model.generation_config, attr):
                setattr(base_model.generation_config, attr, None)

    model = PeftModel.from_pretrained(base_model, args.adapter_path)
    if torch.cuda.is_available():
        model = model.to("cuda")
    model.eval()

    rows: list[dict[str, Any]] = []
    task_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for record in records:
        raw_prediction, prediction, thinking_control_mode = generate_prediction(
            model=model,
            tokenizer=tokenizer,
            instruction=record["instruction"],
            input_text=record["input"],
            max_new_tokens=args.max_new_tokens,
            disable_thinking=args.disable_thinking,
        )

        row = {
            "id": record["id"],
            "source_case_id": record.get("source_case_id", ""),
            "task_type": record["task_type"],
            "instruction": record["instruction"],
            "input": record["input"],
            "reference": record["output"],
            "raw_prediction": raw_prediction,
            "prediction": prediction,
            "exact_match": exact_match(prediction, record["output"]),
            "char_f1": char_f1_score(prediction, record["output"]),
            "prediction_is_empty": normalize_text(prediction) == "",
            "raw_has_think": "<think>" in raw_prediction or "</think>" in raw_prediction,
            "cleaned_changed": raw_prediction != prediction,
            "structure_ok": structure_ok(record["task_type"], prediction),
            "thinking_control_mode": thinking_control_mode,
        }
        rows.append(row)
        task_buckets[row["task_type"]].append(row)

    summary = {
        "dataset_name": dataset_path.stem,
        "dataset_path": str(dataset_path),
        "base_model_path": args.base_model,
        "adapter_path": args.adapter_path,
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "max_new_tokens": args.max_new_tokens,
        "disable_thinking": args.disable_thinking,
        "run_tag": args.run_tag,
        "thinking_control_modes": sorted({row["thinking_control_mode"] for row in rows}),
        "overall": summarize_bucket(rows),
        "by_task_type": {
            task_type: summarize_bucket(bucket)
            for task_type, bucket in sorted(task_buckets.items())
        },
        "worst_examples": [
            {
                "id": row["id"],
                "task_type": row["task_type"],
                "source_case_id": row["source_case_id"],
                "char_f1": row["char_f1"],
                "prediction_is_empty": row["prediction_is_empty"],
                "raw_has_think": row["raw_has_think"],
                "structure_ok": row["structure_ok"],
            }
            for row in sorted(rows, key=lambda item: (item["char_f1"], not item["prediction_is_empty"]))[:5]
        ],
    }

    save_jsonl(output_jsonl, rows)
    save_json(output_summary, summary)
    save_markdown(output_md, rows, summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
