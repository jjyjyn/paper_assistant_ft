#!/usr/bin/env python3
"""Run generation-based evaluation for a LoRA adapter on JSONL datasets."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

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


def generate_prediction(
    model: Any,
    tokenizer: Any,
    instruction: str,
    input_text: str,
    max_new_tokens: int,
) -> str:
    import torch

    user_prompt = build_user_prompt(instruction, input_text)
    messages = [{"role": "user", "content": user_prompt}]

    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt",
    )

    if torch.cuda.is_available():
        inputs = inputs.to("cuda")

    with torch.no_grad():
        output_ids = model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    new_tokens = output_ids[0, inputs.shape[-1] :]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


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
    lines.append(f"- adapter_path: `{summary['adapter_path']}`")
    lines.append(f"- base_model_path: `{summary['base_model_path']}`")
    lines.append("")
    lines.append("## By Task Type")
    lines.append("")
    for task_type, metrics in summary["by_task_type"].items():
        lines.append(
            f"- {task_type}: count={metrics['count']}, "
            f"exact_match_rate={metrics['exact_match_rate']:.4f}, "
            f"avg_char_f1={metrics['avg_char_f1']:.4f}"
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
        lines.append(row["prediction"])

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    model = PeftModel.from_pretrained(base_model, args.adapter_path)
    if torch.cuda.is_available():
        model = model.to("cuda")
    model.eval()

    rows: list[dict[str, Any]] = []
    task_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for record in records:
        prediction = generate_prediction(
            model=model,
            tokenizer=tokenizer,
            instruction=record["instruction"],
            input_text=record["input"],
            max_new_tokens=args.max_new_tokens,
        )

        row = {
            "id": record["id"],
            "source_case_id": record.get("source_case_id", ""),
            "task_type": record["task_type"],
            "instruction": record["instruction"],
            "input": record["input"],
            "reference": record["output"],
            "prediction": prediction,
            "exact_match": exact_match(prediction, record["output"]),
            "char_f1": char_f1_score(prediction, record["output"]),
        }
        rows.append(row)
        task_buckets[row["task_type"]].append(row)

    def summarize(bucket: list[dict[str, Any]]) -> dict[str, Any]:
        count = len(bucket)
        exact_matches = sum(1 for row in bucket if row["exact_match"])
        avg_char_f1 = sum(row["char_f1"] for row in bucket) / count if count else 0.0
        return {
            "count": count,
            "exact_match_rate": exact_matches / count if count else 0.0,
            "avg_char_f1": avg_char_f1,
        }

    summary = {
        "dataset_name": dataset_path.stem,
        "dataset_path": str(dataset_path),
        "base_model_path": args.base_model,
        "adapter_path": args.adapter_path,
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "max_new_tokens": args.max_new_tokens,
        "overall": summarize(rows),
        "by_task_type": {
            task_type: summarize(bucket)
            for task_type, bucket in sorted(task_buckets.items())
        },
        "worst_examples": [
            {
                "id": row["id"],
                "task_type": row["task_type"],
                "source_case_id": row["source_case_id"],
                "char_f1": row["char_f1"],
            }
            for row in sorted(rows, key=lambda item: item["char_f1"])[:5]
        ],
    }

    save_jsonl(output_jsonl, rows)
    save_json(output_summary, summary)
    save_markdown(output_md, rows, summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
