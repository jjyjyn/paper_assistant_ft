# outputs 目录说明

`outputs/` 保存训练与评测产物。这个目录默认被 `.gitignore` 忽略，所以运行结果不会自动进仓库。

## 1. 为什么默认忽略

- 训练输出体积大
- 评测目录增长快
- 大多数中间结果不值得长期版本化

只有需要作为“关键实验证据”保留的结果，才会手动：

```cmd
git add -f outputs\...
```

## 2. 当前结构

```text
outputs/
└─ evals/
```

当前已保留的重点评测目录包括：

- `qwen_lora_v1_full_2026-03-11_234402`
- `qwen_lora_v1_full_2026-03-12_120624`
- `qwen_lora_v1_full_2026-03-12_180125`
- `qwen_lora_v1_full_2026-03-12_220922`
- `qwen_lora_v1_full_2026-03-12_222803`
- `qwen_lora_v1_full_2026-03-13_082359_nothink`

## 3. 单次评测目录里有什么

以 `outputs/evals/<run_name>/` 为例，通常包含：

- `test_v1_summary.json`
- `test_v1_report.md`
- `test_v1_predictions.jsonl`
- `external_eval_v1_summary.json`
- `external_eval_v1_report.md`
- `external_eval_v1_predictions.jsonl`

## 4. 这些文件怎么读

### 4.1 `*_summary.json`

看整体指标，适合先判断这轮值不值得深看。

重点字段：

- `avg_char_f1`
- `exact_match_rate`
- `empty_prediction_rate`
- `raw_think_rate`
- `structure_ok_rate`
- `disable_thinking`
- `run_tag`

### 4.2 `*_report.md`

看面向人的报告，适合做复盘和答辩展示。

### 4.3 `*_predictions.jsonl`

看逐样本明细，适合排查坏样本。

重点字段：

- `reference`
- `prediction`
- `raw_prediction`
- `char_f1`
- `exact_match`
- `prediction_is_empty`
- `raw_has_think`
- `structure_ok`

## 5. 当前最重要的一轮

当前最重要的目录是：

- `outputs/evals/qwen_lora_v1_full_2026-03-13_082359_nothink`

原因：

- 这是 `no-think` 真正生效的一轮
- `raw_think_rate = 0.0`
- `structure_ok_rate = 1.0`
- 它是本阶段最能代表“问题定位到位并验证修复”的证据
