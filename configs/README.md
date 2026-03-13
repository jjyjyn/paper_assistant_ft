# configs 目录说明

`configs/` 只放配置文件，不放执行日志和临时记录。

## 1. 当前结构

```text
configs/
├─ README.md
├─ datasets/
└─ train/
```

### 1.1 `datasets/`

- `datasets/paper_assistant_v1.yaml`
  - 数据构建与校验相关的快捷配置（Day2 口径）

### 1.2 `train/`

- `train/lora_sft_qwen25_3b_v1.yaml`
  - 早期 smoke 闭环训练配置
- `train/lora_sft_qwen_v1_full.yaml`
  - 当前 `v1 full` 主训练配置

## 2. 使用顺序

1. 先确认 `data/dataset_info.json` 的数据集注册名
2. 再检查 `configs/train/` 下训练配置是否引用了正确数据集
3. 先跑 `scripts/train/run_train_smoke.sh`
4. Smoke 通过后跑 `scripts/train/run_train_full.sh`

## 3. 兼容说明

- `scripts/train/run_train_smoke.sh` 和 `scripts/train/run_train_full.sh` 已支持旧配置路径兼容映射
- 旧路径仍可被脚本自动映射：
  - `configs/lora_sft_qwen25_3b_v1.yaml`
  - `configs/lora_sft_qwen_v1_full.yaml`
- 但后续文档与开发统一以新路径为准：
  - `configs/train/lora_sft_qwen25_3b_v1.yaml`
  - `configs/train/lora_sft_qwen_v1_full.yaml`

## 4. 维护原则

- 配置文件只描述参数，不记录实验结论
- 重大配置变更同步记录到：
  - `docs/00_meta/project_plan.md`
  - `docs/00_meta/progress_log.md`
- 不同阶段配置尽量保留，不覆盖历史版本
