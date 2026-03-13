# paper_assistant_ft

基于 Qwen 的中文论文精读与实验解析助手微调项目。当前仓库已经完成 `v1` 数据构建、LoRA SFT 训练、baseline 评测、`no-think` 推理控制验证，以及面试复盘文档沉淀。

## 1. 当前状态

- 当前阶段：`2.5-3 大模型微调任务` 已完成阶段性闭环
- 当前主模型：`Qwen3-4B + LoRA SFT`
- 当前主适配器：`outputs/qwen_lora_v1_full`
- 当前最佳有效评测目录：`outputs/evals/qwen_lora_v1_full_2026-03-13_082359_nothink`
- 当前最佳结果：
  - `test avg_char_f1 = 0.6698`
  - `external avg_char_f1 = 0.6990`
  - `raw_think_rate = 0.0`
  - `empty_prediction_rate = 0.0`
  - `structure_ok_rate = 1.0`

这一版项目的核心工程结论不是“继续盲目重训”，而是已经验证出主问题曾经集中在推理阶段的 `<think>` 输出污染；在 `no-think` 生效后，模型内容质量显著恢复。

## 2. 仓库怎么读

如果你第一次进仓库，按这个顺序读：

1. `README.md`
2. `docs/repo_structure_guide.md`
3. `docs/project_plan.md`
4. `docs/progress_log.md`
5. `docs/01_data/dataset_schema.md`
6. `docs/02_training/day3_training_hands_on_lab.md`
7. `docs/03_interview/teacher_question_bank.md`

如果你只是要快速知道“项目现在到哪一步了”，只看这 4 份：

1. `README.md`
2. `docs/project_plan.md`
3. `docs/progress_log.md`
4. `docs/interview_notes.md`

如果你要直接执行训练或评测，优先看：

1. `scripts/README.md`
2. `docs/02_training/environment_setup_guide.md`
3. `docs/02_training/day3_training_hands_on_lab.md`

## 3. 顶层目录总览

| 路径 | 作用 | 先看什么 |
| --- | --- | --- |
| `configs/` | 训练与数据配置文件 | `configs/README.md` |
| `data/` | 原始数据、训练集、评测集、数据注册 | `data/README.md` |
| `docs/` | 计划、日志、训练手册、面试复盘 | `docs/README_docs.md` |
| `logs/` | 训练日志与运行日志，默认不进 Git | `logs/README.md` |
| `outputs/` | 评测结果、checkpoint、推理输出，默认不进 Git | `outputs/README.md` |
| `scripts/` | 数据构建、校验、训练、评测、同步脚本 | `scripts/README.md` |

## 4. 仓库结构

```text
paper_assistant_ft/
├─ README.md
├─ .gitignore
├─ configs/
├─ data/
├─ docs/
├─ logs/
├─ outputs/
└─ scripts/
```

更细的目录说明见：

- `docs/repo_structure_guide.md`
- `configs/README.md`
- `data/README.md`
- `logs/README.md`
- `scripts/README.md`
- `outputs/README.md`

## 5. 一条完整工作流

### 5.1 数据阶段

1. 在 `data/raw/` 准备原始论文案例
2. 用 `scripts/build_dataset_v1.py` 构建 `train/val/test`
3. 用 `scripts/check_dataset_v1.py` 做字段与分布校验
4. 用 `scripts/build_external_eval_v1.py` 构建 external eval
5. 用 `scripts/check_external_eval_v1.py` 做外部评测集校验

### 5.2 训练阶段

1. 在 `configs/` 选择训练配置
2. 先运行 `scripts/run_train_smoke.sh`
3. Smoke 通过后运行 `scripts/run_train_full.sh`
4. 训练产物默认写入 `outputs/`

### 5.3 评测阶段

1. 运行 `scripts/run_eval_v1.sh`
2. 评测目录写入 `outputs/evals/<run_name>/`
3. 重点看：
   - `test_v1_summary.json`
   - `external_eval_v1_summary.json`
   - `test_v1_report.md`
   - `external_eval_v1_report.md`
   - `*_predictions.jsonl`

### 5.4 复盘阶段

1. 计划与下一步：`docs/project_plan.md`
2. 实际执行日志：`docs/progress_log.md`
3. 可直接复述的讲法：`docs/interview_notes.md`
4. 老师/面试追问：`docs/03_interview/teacher_question_bank.md`

## 6. 当前关键产物

### 6.1 数据

- 原始案例：`data/raw/paper_cases_v1.json`
- 训练集：`data/processed/train_v1.jsonl`
- 验证集：`data/processed/val_v1.jsonl`
- 测试集：`data/processed/test_v1.jsonl`
- 外部评测集：`data/external_eval/processed/external_eval_v1.jsonl`

当前冻结口径：

- train / val / test = `64 / 8 / 8`
- external eval = `32`
- 四类任务均衡分布

### 6.2 配置

- 数据注册：`data/dataset_info.json`
- 早期配置：`configs/lora_sft_qwen25_3b_v1.yaml`
- 当前 full 配置：`configs/lora_sft_qwen_v1_full.yaml`

### 6.3 评测结果

默认情况下，`outputs/` 和 `logs/` 被 `.gitignore` 忽略，不会自动进仓库。只有需要保留为复盘证据的评测目录，才会通过 `git add -f` 强制加入版本库。

当前重点关注的评测目录：

- `outputs/evals/qwen_lora_v1_full_2026-03-12_212350`
- `outputs/evals/qwen_lora_v1_full_2026-03-12_220922`
- `outputs/evals/qwen_lora_v1_full_2026-03-12_222803`
- `outputs/evals/qwen_lora_v1_full_2026-03-13_082359_nothink`

## 7. 文档体系

### 7.1 总控文档

- `docs/project_plan.md`
- `docs/progress_log.md`
- `docs/interview_notes.md`
- `docs/chat_migration_handoff_2026-03-12.md`

### 7.2 阶段文档

- 数据：`docs/01_data/`
- 训练：`docs/02_training/`
- 面试：`docs/03_interview/`

### 7.3 文档总入口

- `docs/README_docs.md`
- `docs/repo_structure_guide.md`

## 8. 提交与同步约定

- 本地仓库根目录固定为：`D:\llm_train\paper_assistant_ft`
- 默认在本地 `cmd` 执行 `git add / commit / push`
- 服务器若 `git pull` 失败，优先用 `scp` 同步脚本或结果目录
- 服务器评测结果若要入库，先拉回本地，再 `git add -f outputs/...`

## 9. 你接下来最常用的入口

- 想看项目全貌：`docs/repo_structure_guide.md`
- 想知道现在做到哪：`docs/project_plan.md`
- 想看每轮实验怎么演进：`docs/progress_log.md`
- 想直接跑：`scripts/README.md`
- 想准备答辩：`docs/03_interview/teacher_question_bank.md`
