# paper_assistant_ft

基于 Qwen 的中文论文精读与实验解析助手微调项目。

## 固定技术路线

- LLaMA-Factory
- Qwen3-4B-Instruct
- LoRA SFT

## 固定工作流

- 本地开发（VSCode + Codex）只改本地仓库
- 服务器执行（环境、训练、推理、日志、checkpoint）
- 通过 `git` 或 `rsync/scp` 手动同步

## 目录结构

- `configs/`: 训练配置、数据配置、推理配置
- `scripts/`: 环境初始化、数据处理、训练、评测脚本
- `data/raw/`: 原始数据（论文、标注草稿、问答原始文本）
- `data/processed/`: 可直接用于训练/评测的数据集
- `logs/`: 训练日志、错误日志、实验记录
- `outputs/`: 训练产物、导出模型、推理输出
- `docs/`: 项目计划、过程记录、面试与答辩笔记

## Day 1 重点

1. 补齐记录体系：`docs/project_plan.md`、`docs/progress_log.md`、`docs/interview_notes.md`
2. 跑通服务器基础环境初始化流程
3. 确认本地到服务器同步流程可执行

