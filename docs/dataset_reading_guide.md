# train_v1 怎么看（阅读指南）

## 为什么 `train_v1.jsonl` 看起来“很横、很长”

- `jsonl` 是给训练程序读的格式：每一行就是一条完整样本。
- 这种格式适合流式读取和大规模训练，不适合人工精读。

## 每条样本字段是什么意思

- `id`：样本编号（如 `v1_0014`）
- `task_type`：任务类型（四类之一）
- `instruction`：指令（你希望模型做什么）
- `input`：输入上下文（论文信息）
- `output`：标准答案（你希望模型学会如何回答）
- `source_case_id`：来源案例编号（可追溯）

## 四类任务对应能力

- `contribution_extraction`：提炼论文贡献
- `method_comparison`：方法对比解释
- `experiment_interpretation`：实验结果解析
- `defense_followup`：答辩追问回答

## 可读方式（推荐）

先执行：

```bash
python scripts/export_dataset_readable.py
```

会生成：

- `data/processed/train_v1_readable.md`
- `data/processed/train_v1_readable.json`
- `data/processed/val_v1_readable.md`
- `data/processed/val_v1_readable.json`

建议你平时看 `*_readable.md`，训练时用 `*.jsonl`。
