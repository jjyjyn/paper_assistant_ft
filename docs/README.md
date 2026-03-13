# Docs 导航

这份文档是 `docs/` 目录的总入口。它只负责一件事：告诉你文档现在怎么分层、每类文档该去哪找、按什么顺序读最省时间。

## 1. docs 目录现在怎么分

### 1.1 入口层

- `README.md`
  - 当前这份导航

### 1.2 总控层：`00_meta/`

这里放跨阶段、跨主题的总控材料：

- `00_meta/project_plan.md`
- `00_meta/progress_log.md`
- `00_meta/repo_structure_guide.md`
- `00_meta/repo_physical_refactor_plan.md`
- `00_meta/handoffs/chat_migration_handoff_2026-03-11.md`
- `00_meta/handoffs/chat_migration_handoff_2026-03-12.md`

### 1.3 阶段层

- `01_data/`
- `02_training/`
- `03_interview/`

其中：

- `01_data/` 放数据准备、清洗、schema、external eval
- `02_training/` 放环境、训练执行、租服、端到端手册
- `03_interview/` 放面试讲法、追问题库、分类复盘

## 2. 推荐阅读顺序

### 2.1 第一次完整熟悉项目

1. `../README.md`
2. `00_meta/repo_structure_guide.md`
3. `00_meta/repo_physical_refactor_plan.md`
4. `00_meta/project_plan.md`
5. `00_meta/progress_log.md`
6. `01_data/dataset_schema.md`
7. `02_training/day3_training_hands_on_lab.md`
8. `03_interview/teacher_question_bank.md`

### 2.2 只想知道项目做到哪了

1. `00_meta/project_plan.md`
2. `00_meta/progress_log.md`
3. `03_interview/interview_notes_quick.md`

### 2.3 明天要答辩或给老师讲

1. `00_meta/project_plan.md`
2. `03_interview/interview_notes_quick.md`
3. `03_interview/teacher_question_bank.md`
4. `03_interview/interview_notes_categorized.md`

### 2.4 要继续接着跑实验

1. `00_meta/repo_structure_guide.md`
2. `00_meta/repo_physical_refactor_plan.md`
3. `02_training/environment_setup_guide.md`
4. `02_training/day3_training_hands_on_lab.md`
5. `../scripts/README.md`

## 3. 按主题找文档

### 3.1 数据

目录：`01_data/`

核心文件：

- `01_data/dataset_schema.md`
- `01_data/dataset_reading_guide.md`
- `01_data/data_cleaning_labeling_guide.md`
- `01_data/external_eval_guide.md`
- `01_data/day2_data_hands_on_lab.md`
- `01_data/day2_hands_on_checklist.md`

如果你要看“一个 raw case 怎么变成训练样本”，继续看：

- `01_data/data_preparation/README.md`
- `01_data/data_preparation/case_to_sample_mapping_case004.md`
- `01_data/data_preparation/case_test_log.md`

### 3.2 训练与环境

目录：`02_training/`

核心文件：

- `02_training/environment_setup_guide.md`
- `02_training/rental_server_guide.md`
- `02_training/day3_training_hands_on_lab.md`
- `02_training/llm_finetune_end2end_playbook.md`

### 3.3 面试与复盘

目录：`03_interview/`

核心文件：

- `03_interview/interview_notes_quick.md`
- `03_interview/interview_notes_categorized.md`
- `03_interview/teacher_question_bank.md`

## 4. 总控文档各自负责什么

### 4.1 `00_meta/project_plan.md`

负责：

- 当前阶段目标
- 下一步动作
- 固定执行口径

### 4.2 `00_meta/progress_log.md`

负责：

- 每次真实执行了什么
- 遇到了什么坑
- 是怎么定位和修掉的

### 4.3 `03_interview/interview_notes_quick.md`

负责：

- 压缩后的项目讲法
- 最短可复述版本
- 临近沟通前的快速复习

### 4.4 `00_meta/handoffs/chat_migration_handoff_*.md`

负责：

- 新开对话时的最小接手包
- 避免重复解释背景

### 4.5 `00_meta/repo_structure_guide.md`

负责：

- 当前真实仓库结构怎么读
- 各目录分别负责什么

### 4.6 `00_meta/repo_physical_refactor_plan.md`

负责：

- 后续物理迁移怎么继续做
- 哪些目录值得下一批再重构

## 5. docs 的维护规则

- 阶段计划先写 `00_meta/project_plan.md`
- 实际执行结果回写 `00_meta/progress_log.md`
- 能不能讲清楚，回写 `03_interview/interview_notes_quick.md` 或 `03_interview/`
- 历史记录不删，只追加和标记

## 6. 当前最常用的三份文档

- 想知道现在到哪一步：`00_meta/project_plan.md`
- 想知道这一路怎么做过来的：`00_meta/progress_log.md`
- 想准备讲项目：`03_interview/teacher_question_bank.md`
