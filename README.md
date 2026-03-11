# paper_assistant_ft

基于 Qwen 的中文论文精读与实验解析助手微调项目。

## 固定技术路线

- LLaMA-Factory
- Qwen3-4B-Instruct（执行上先用 Qwen2.5-3B 跑通闭环）
- LoRA SFT

## 固定工作流

- 本地开发（VSCode + Codex）只改本地仓库
- 服务器执行（环境、训练、推理、日志、checkpoint）
- 通过 `git` 或 `rsync/scp` 手动同步

## 目录结构

- `configs/`: 训练配置、数据配置、推理配置
- `scripts/`: 环境初始化、数据处理、训练、评测脚本
- `data/raw/`: 原始数据（结构化案例、标注草稿）
- `data/processed/`: 可直接训练/评测的 JSONL
- `logs/`: 训练日志、错误日志、实验记录
- `outputs/`: checkpoint、导出模型、推理输出
- `docs/`: 项目计划、过程记录、面试笔记、租服指南

## 文档导航

- `docs/project_plan.md`: 阶段目标与执行清单
- `docs/progress_log.md`: 每日进展与复盘
- `docs/interview_notes.md`: Why 与答辩追问
- `docs/dataset_schema.md`: 数据集字段与规则
- `docs/rental_server_guide.md`: 租 4090 执行指南

## Day 2 产物（已完成）

- 数据 schema：`docs/dataset_schema.md`
- 原始案例库：`data/raw/paper_cases_v1.json`（20 case）
- 数据构建脚本：`scripts/build_dataset_v1.py`
- 数据校验脚本：`scripts/check_dataset_v1.py`
- 训练数据：
  - `data/processed/train_v1.jsonl`（72）
  - `data/processed/val_v1.jsonl`（8）
- LLaMA-Factory 数据注册：`data/dataset_info.json`
- 训练配置：`configs/lora_sft_qwen25_3b_v1.yaml`
- 冒烟训练脚本：`scripts/run_train_smoke.sh`
