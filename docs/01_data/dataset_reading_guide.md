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

## v1 切分升级（2026-03-11）
- 当前使用 train/val/test 三分集：64/8/8。
- 切分粒度为 source_case_id（同一 case 不会同时出现在多个 split）。
- 读取建议：先看 train_v1_readable.md，再抽查 val/test 的 source_case_id 是否未在 train 出现。

## 当前数据分集结构（2026-03-11）
- 训练集：data/processed/train_v1.jsonl（唯一一套）
- 验证集：data/processed/val_v1.jsonl（唯一一套）
- 项目内测试集（in-domain）：data/processed/test_v1.jsonl
- 外部测试集（external eval）：data/external_eval/processed/external_eval_v1.jsonl

使用建议：
1. 训练调参主要看 train/val。
2. 阶段性汇报同时给出 test_v1 与 external_eval_v1 两组结果。
3. external_eval_v1 默认只评测，不参与训练。

