# Docs 导航

这份文档是 `docs/` 目录的总入口。它不重复讲项目细节，只负责告诉你：哪些文档在什么位置、适合什么场景、推荐按什么顺序阅读。

## 1. docs 目录内部分层

`docs/` 里现在分成两类内容：

### 1.1 总控层

这些文件放在 `docs/` 根目录，负责记录项目阶段状态和跨阶段迁移信息：

- `project_plan.md`
- `progress_log.md`
- `interview_notes.md`
- `chat_migration_handoff_2026-03-11.md`
- `chat_migration_handoff_2026-03-12.md`
- `repo_structure_guide.md`
- `README_docs.md`

### 1.2 阶段层

这些子目录按主题拆分，不再把所有内容堆在根目录：

- `01_data/`
- `02_training/`
- `03_interview/`

## 2. 推荐阅读路径

### 2.1 第一次完整熟悉项目

1. `../README.md`
2. `repo_structure_guide.md`
3. `project_plan.md`
4. `progress_log.md`
5. `01_data/dataset_schema.md`
6. `02_training/day3_training_hands_on_lab.md`
7. `03_interview/teacher_question_bank.md`

### 2.2 只想快速知道项目现在做到哪

1. `project_plan.md`
2. `progress_log.md`
3. `interview_notes.md`

### 2.3 明天要答辩或给老师讲

1. `project_plan.md`
2. `interview_notes.md`
3. `03_interview/teacher_question_bank.md`
4. `03_interview/interview_notes_categorized.md`

### 2.4 要自己接着跑实验

1. `repo_structure_guide.md`
2. `02_training/environment_setup_guide.md`
3. `02_training/day3_training_hands_on_lab.md`
4. `../scripts/README.md`

## 3. 按主题查文档

### 3.1 数据

目录：`01_data/`

核心文件：

- `dataset_schema.md`
- `dataset_reading_guide.md`
- `data_cleaning_labeling_guide.md`
- `external_eval_guide.md`
- `day2_data_hands_on_lab.md`
- `day2_hands_on_checklist.md`

如果你要看“一个 raw case 是怎么变成训练样本的”，继续看：

- `01_data/data_preparation/README.md`
- `01_data/data_preparation/case_to_sample_mapping_case004.md`
- `01_data/data_preparation/case_test_log.md`

### 3.2 训练与环境

目录：`02_training/`

核心文件：

- `environment_setup_guide.md`
- `rental_server_guide.md`
- `day3_training_hands_on_lab.md`
- `llm_finetune_end2end_playbook.md`

### 3.3 面试与复盘

目录：`03_interview/`

核心文件：

- `teacher_question_bank.md`
- `interview_notes_categorized.md`

## 4. 根目录总控文档各自负责什么

### 4.1 `project_plan.md`

负责：

- 当前阶段目标
- 下一步行动
- 固定执行口径

适合在项目开始做事前先看。

### 4.2 `progress_log.md`

负责：

- 每次真实执行了什么
- 遇到了什么坑
- 是怎么定位和修掉的

适合做复盘和写实验过程。

### 4.3 `interview_notes.md`

负责：

- 压缩后的项目讲法
- 最短可复述版本
- 临近沟通前的快速复习

### 4.4 `chat_migration_handoff_*.md`

负责：

- 新开对话时的最小接手包
- 避免重复解释背景

## 5. docs 的使用原则

- 阶段计划先写 `project_plan.md`
- 实际执行结果回写 `progress_log.md`
- 能不能讲清楚，回写 `interview_notes.md` 或 `03_interview/`
- 历史记录不删，只追加和标记

## 6. 你最常用的三份文档

- 想知道现在到哪一步：`project_plan.md`
- 想知道这一路怎么做过来的：`progress_log.md`
- 想准备讲项目：`03_interview/teacher_question_bank.md`
