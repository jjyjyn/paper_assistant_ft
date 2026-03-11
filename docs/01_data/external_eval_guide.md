# 外部评测集操作指南（external_eval）

## 1. 这套东西是干什么的

- 目的：提供一份独立于训练集的评测数据，用来判断模型是否真的泛化，而不是只记住训练模板。
- 路径：
  - 原始 case：`data/external_eval/raw/external_eval_cases_v1.json`
  - 评测样本：`data/external_eval/processed/external_eval_v1.jsonl`
  - 可读文件：`data/external_eval/processed/external_eval_v1_readable.{json,md}`

## 2. 你要执行的命令

在项目根目录执行：

```bash
python scripts/build_external_eval_v1.py
python scripts/check_external_eval_v1.py
```

## 3. 这两个脚本分别做什么

1. `build_external_eval_v1.py`
- 从 `external_eval_cases_v1.json` 生成 4 类任务样本：
  - contribution_extraction
  - method_comparison
  - experiment_interpretation
  - defense_followup
- 每个外部 case 会生成 4 条样本。
- 结果写入 `external_eval_v1.jsonl` 和 readable 文件。

2. `check_external_eval_v1.py`
- 检查字段完整性、task_type 合法性、每个 case 的四任务覆盖。
- 检查与主训练 raw cases 的 `case_id/title` 不重合（降低泄漏风险）。

## 4. 你后续如何扩展

1. 打开 `data/external_eval/raw/external_eval_cases_v1.json`
2. 追加新 case（保持字段一致）：
- `case_id`
- `title`
- `problem`
- `method`
- `baseline`
- `result`
- `limitations`
3. 重新执行 build + check。

## 5. 使用注意

1. 外部评测集原则上不参与训练，不要混入 `data/processed/train_v1.jsonl`。
2. 一旦开始汇报实验结果，尽量冻结 external_eval，不要频繁按结果回改。
3. 若你从真实论文补数据，优先保证“标题/问题表达风格”与训练集不同，提升外部评测有效性。
