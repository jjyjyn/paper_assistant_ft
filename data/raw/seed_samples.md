# Seed Samples Notes (v1)

This file records manual review notes for the first dataset batch.

## Source

- Structured cases: `data/raw/paper_cases_v1.json` (20 cases)
- Expanded by script: `scripts/build_dataset_v1.py`

## Task coverage checklist

- [x] contribution_extraction
- [x] method_comparison
- [x] experiment_interpretation
- [x] defense_followup

## Quality checklist

- [x] Output grounded in input facts
- [x] Contains concrete metric/result wording when available
- [x] No fabricated baseline names or numbers
- [x] Structured answer style for interview retelling

## Notes

- v1 is template-generated for fast project bootstrap.
- Next iteration should add manually written hard examples:
  - ambiguous metric interpretation
  - contradictory ablation trends
  - multi-paper method confusion
