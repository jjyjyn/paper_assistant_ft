# data 目录说明

`data/` 保存从原始案例到训练集、测试集、外部评测集的完整数据链路。

## 目录结构

```text
data/
├─ dataset_info.json
├─ raw/
├─ processed/
└─ external_eval/
```

## 1. `raw/`

作用：保存原始案例和种子样本。

当前主要文件：

- `raw/paper_cases_v1.json`
- `raw/seed_samples.md`

这里的数据不直接用于训练，需要先经过脚本构建。

## 2. `processed/`

作用：保存训练、验证、测试数据，以及便于人工阅读的导出版本。

当前主要文件：

- `processed/train_v1.jsonl`
- `processed/val_v1.jsonl`
- `processed/test_v1.jsonl`
- `processed/*_readable.json`
- `processed/*_readable.md`

当前冻结口径：

- train / val / test = `64 / 8 / 8`

## 3. `external_eval/`

作用：保存外部评测集，确保与训练集分离。

结构：

```text
external_eval/
├─ raw/
└─ processed/
```

当前主要文件：

- `external_eval/raw/external_eval_cases_v1.json`
- `external_eval/processed/external_eval_v1.jsonl`
- `external_eval/processed/external_eval_v1_readable.json`
- `external_eval/processed/external_eval_v1_readable.md`

当前冻结口径：

- external eval = `32`

## 4. `dataset_info.json`

作用：给训练框架做数据集注册。训练配置会依赖这里的数据集名称和路径。

## 5. 数据是怎么生成的

### 5.1 主数据集

1. 原始输入：`raw/paper_cases_v1.json`
2. 构建脚本：`../scripts/data/build_dataset_v1.py`
3. 校验脚本：`../scripts/data/check_dataset_v1.py`
4. 导出可读版本：`../scripts/data/export_dataset_readable.py`

### 5.2 外部评测集

1. 原始输入：`external_eval/raw/external_eval_cases_v1.json`
2. 构建脚本：`../scripts/data/build_external_eval_v1.py`
3. 校验脚本：`../scripts/data/check_external_eval_v1.py`

兼容说明：

- 旧入口 `../scripts/build_dataset_v1.py` 等 wrapper 仍可运行
- 但后续文档与开发统一以 `scripts/data/` 为准

## 6. 读取建议

- 想看样本结构：先读 `../docs/01_data/dataset_schema.md`
- 想看怎么防泄漏：读 `../docs/01_data/dataset_reading_guide.md`
- 想看具体样例：读 `processed/*_readable.md`
