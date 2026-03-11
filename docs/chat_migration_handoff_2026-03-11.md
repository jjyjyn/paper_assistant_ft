# Chat Migration Handoff (2026-03-11)

## 1. Purpose

Use this file when the current chat is close to token limit.
Open a new Codex chat and paste the migration package below so work can continue without context loss.

## 2. Copy-Paste Package for New Chat

Paste everything between the two lines into the first message of the new chat.

```text
你继续维护项目：paper_assistant_ft（本地路径 D:\llm_train\paper_assistant_ft）。

固定约束（不要改）：
1) 题目：基于 Qwen 的中文论文精读与实验解析助手微调项目。
2) 路线：LLaMA-Factory + Qwen3-4B-Instruct + LoRA SFT。
3) 工作流：本地开发 + 服务器执行 + 手动同步（git / rsync / scp）。
4) 目标：5 天 first usable，6-7 天 resume-ready。
5) docs 体系必须持续更新：docs/progress_log.md, docs/project_plan.md, docs/interview_notes.md。

当前代码与数据状态（已完成）：
1) 数据主链路已完成：
- raw 基础案例库：data/raw/paper_cases_v1.json
- build 脚本：scripts/build_dataset_v1.py
- check 脚本：scripts/check_dataset_v1.py
- readable 导出：scripts/export_dataset_readable.py

2) 当前 split 方案已升级为 case-level 三分：
- train: data/processed/train_v1.jsonl（64）
- val: data/processed/val_v1.jsonl（8）
- test: data/processed/test_v1.jsonl（8）
- 防泄漏检查：id 与 source_case_id 跨 split 重复会直接报错

3) 外部评测链路已建立：
- external raw: data/external_eval/raw/external_eval_cases_v1.json
- build: scripts/build_external_eval_v1.py
- check: scripts/check_external_eval_v1.py
- external test: data/external_eval/processed/external_eval_v1.jsonl（32）
- overlap 检查：external 与主训练 raw 在 case_id/title 上做去重校验

4) docs 侧已有数据学习与复盘材料：
- docs/dataset_schema.md
- docs/dataset_reading_guide.md
- docs/data_cleaning_labeling_guide.md
- docs/llm_finetune_end2end_playbook.md
- docs/day2_data_hands_on_lab.md
- docs/data_preparation/case_test_log.md
- docs/external_eval_guide.md

5) 关键结论：
- 现在是 “1 套 train + 1 套 val + 2 套 test（in-domain + external）”。
- 阶段 2（数据第一版）已经达到可训练标准，下一步是训练与评测闭环。

你现在要做的事（按顺序）：
1) 先检查本地仓库状态与最近提交，给我一句确认。
2) 给出“今天执行清单”（只保留高优先动作，不要泛泛而谈）。
3) 从训练前准备开始，逐条带我执行，并在每一步解释“我在做什么、为什么这样做、做完如何验收”。
4) 每完成一个动作就同步告诉我要不要更新 docs（要给出具体文件与建议内容）。
5) 若涉及服务器命令，按“可复制粘贴”的最小命令块给出。

额外要求：
1) 我不是只要结果，我要能讲给老师/面试官听；解释要落在“原理 + 操作 + 验收 + 常见坑”。
2) 不要删旧笔记，新增内容按 Day/主题分类追加。
3) 如果你建议改方案，要先说明 tradeoff，再执行。
```

## 3. Optional Quick Check Before Migration

Run these in local terminal before opening a new chat:

```powershell
cd D:\llm_train\paper_assistant_ft
git status
git log --oneline -n 10
```

Expected: clean working tree or only known local edits.

## 4. What To Send After First Message (if needed)

If Codex in new chat asks for state, paste:

```text
补充状态：
1) 数据已完成 train/val/test + external_eval；
2) 已有 build/check/export/external check 脚本；
3) 现在进入训练前准备与训练执行阶段；
4) 请你直接按“可执行命令 + 验收标准 + 文档更新点”推进。
```

## 5. Notes

- Do not paste passwords/tokens/API keys into chat.
- Keep this handoff file updated when phase changes (Phase 2 -> Phase 3 -> Phase 4).
