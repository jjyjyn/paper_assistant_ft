# paper_assistant_ft

基于 Qwen 的中文论文精读与实验解析助手微调项目。

## 固定技术路线

- LLaMA-Factory
- Qwen3-4B-Instruct（执行上可先用 Qwen2.5-3B 跑通闭环）
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
- `docs/`: 项目计划、过程记录、面试答辩笔记、租服务器指南

## 文档导航

- `docs/project_plan.md`: 阶段目标、明日清单、完成标准
- `docs/progress_log.md`: 每日执行与复盘
- `docs/interview_notes.md`: Why 与 Q&A
- `docs/rental_server_guide.md`: 租服务器建议（4090 是否够用、成本和时长估算）

## 当前状态

- Day 1：已完成（环境与仓库跑通 + 文档体系完成）
- Day 2：待执行（数据 schema、样本与数据构建脚本）
