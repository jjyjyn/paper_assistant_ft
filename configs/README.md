# configs 目录说明

`configs/` 只放配置文件，不放执行日志和临时记录。

## 当前文件

- `dataset_paper_assistant_v1.yaml`
  - 数据集相关配置
- `lora_sft_qwen25_3b_v1.yaml`
  - 早期用于跑通闭环的 LoRA SFT 配置
- `lora_sft_qwen_v1_full.yaml`
  - 当前 `v1 full` 主训练配置

## 使用顺序

1. 先确认 `data/dataset_info.json` 注册的数据集名称
2. 再检查这里的训练配置是否引用了正确的数据集
3. 先用 `scripts/run_train_smoke.sh` 做冒烟
4. 冒烟通过后再用 `scripts/run_train_full.sh`

## 维护原则

- 配置文件只描述参数，不记录实验结论
- 重大配置变更需要在 `docs/project_plan.md` 和 `docs/progress_log.md` 留痕
- 不同阶段的配置文件尽量保留，不覆盖历史版本
