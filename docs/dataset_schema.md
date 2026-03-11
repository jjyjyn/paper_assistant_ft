# Dataset Schema (v1)

## Goal

Build a supervised fine-tuning dataset for a Chinese paper reading assistant
with four fixed task types:

1. `contribution_extraction`
2. `method_comparison`
3. `experiment_interpretation`
4. `defense_followup`

## Sample format (JSONL)

Each line is a JSON object:

```json
{
  "id": "v1_0001",
  "task_type": "contribution_extraction",
  "instruction": "你是论文精读助手。请提取论文贡献点。",
  "input": "论文标题: ...\n摘要: ...",
  "output": "1) ...\n2) ...\n3) ...",
  "source_case_id": "case_001"
}
```

## Field rules

- `id`: unique sample id, `v1_XXXX`.
- `task_type`: one of the four fixed types.
- `instruction`: stable role/task instruction for this sample.
- `input`: paper context (title, problem, method, baseline, results, limits).
- `output`: high-quality target answer in Chinese.
- `source_case_id`: traceability id from raw case library.

## Quality requirements

- Output must be factual and grounded in given input.
- No hallucinated metrics or claims.
- Keep concise, structured, and interview-friendly wording.
- Avoid overly generic output; include concrete comparisons and numbers when provided.

## Split strategy (v1)

- Source library: `data/raw/paper_cases_v1.json`.
- Build method: template expansion for 4 tasks per case.
- Split: deterministic shuffle by seed (`20260311`), 90/10 train/val.

## Current v1 target

- Cases: 20
- Samples per case: 4
- Total samples: 80
- Expected split: train 72 / val 8
