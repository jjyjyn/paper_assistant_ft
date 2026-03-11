# Docs 导航（按阶段读，不要乱翻）

## 1. 根目录这 5 个文件是总控层

- `project_plan.md`
  - 当前阶段、下一步动作、固定口径
- `progress_log.md`
  - 每天做了什么、遇到什么问题、如何修掉
- `interview_notes.md`
  - 最短可复述答法，适合临近沟通前快速看
- `chat_migration_handoff_2026-03-11.md`
  - 开新对话窗口时的迁移包
- `README_docs.md`
  - 当前这份导航

说明：
- 这 5 份放在根目录，是因为它们承担“总控”和“迁移”职责。
- 其他材料已经按阶段拆到子目录，不再全部堆在根目录。

## 2. 推荐阅读顺序（第一次完整过项目）

1. `project_plan.md`
2. `progress_log.md`
3. `01_data/dataset_schema.md`
4. `01_data/data_cleaning_labeling_guide.md`
5. `02_training/environment_setup_guide.md`
6. `02_training/day3_training_hands_on_lab.md`
7. `03_interview/teacher_question_bank.md`

如果你是明天要给老师讲项目，最少读这 4 份：

1. `project_plan.md`
2. `01_data/data_cleaning_labeling_guide.md`
3. `02_training/environment_setup_guide.md`
4. `03_interview/teacher_question_bank.md`

## 3. 按阶段分类

### 3.1 数据准备与清洗：`docs/01_data/`

- `dataset_schema.md`
  - 训练样本字段定义、split 口径、防泄漏规则
- `dataset_reading_guide.md`
  - train/val/test/external 该怎么看
- `data_cleaning_labeling_guide.md`
  - 清洗规则、标注标准、常见问题与处理
- `day2_data_hands_on_lab.md`
  - Day 2 你亲手做数据的完整实验单
- `day2_hands_on_checklist.md`
  - Day 2 打卡版清单
- `external_eval_guide.md`
  - 外部评测集怎么构建、怎么用、怎么冻结

### 3.2 数据映射与案例复盘：`docs/01_data/data_preparation/`

- `README.md`
  - 这个子目录是干什么的
- `case_to_sample_mapping_case004.md`
  - raw case 如何映射成训练样本
- `case_test_log.md`
  - 每次改 case 后，样本层面发生了什么变化

### 3.3 环境与训练执行：`docs/02_training/`

- `environment_setup_guide.md`
  - 服务器环境怎么配、这次踩了哪些坑、最后固定了哪些版本
- `rental_server_guide.md`
  - 为什么租 4090、怎么控成本、磁盘怎么选
- `day3_training_hands_on_lab.md`
  - 从数据冻结到 smoke/full 的逐步训练手册
- `llm_finetune_end2end_playbook.md`
  - 从任务定义到面试讲述的完整闭环手册

### 3.4 面试与老师追问：`docs/03_interview/`

- `interview_notes_categorized.md`
  - 按主题归档的复习材料
- `teacher_question_bank.md`
  - 按阶段分组的高压追问问答

## 4. 老师最可能怎么问，你该看哪份

- 问“你到底做了什么项目”：
  - `project_plan.md`
  - `03_interview/teacher_question_bank.md`
- 问“数据怎么来的，质量怎么保证”：
  - `01_data/data_cleaning_labeling_guide.md`
  - `01_data/data_preparation/case_to_sample_mapping_case004.md`
  - `01_data/data_preparation/case_test_log.md`
- 问“为什么这样切分，怎么防泄漏”：
  - `01_data/dataset_schema.md`
  - `01_data/dataset_reading_guide.md`
- 问“服务器环境和依赖怎么配，遇到什么坑”：
  - `02_training/environment_setup_guide.md`
- 问“为什么先 smoke 再 full”：
  - `02_training/day3_training_hands_on_lab.md`
  - `03_interview/teacher_question_bank.md`

## 5. 文档维护规则

- 旧记录不删，只追加
- 关键口径变更时，先更新 `project_plan.md`
- 实际执行与踩坑，追加到 `progress_log.md`
- 面试能不能讲清楚，回写到 `interview_notes.md` 或 `03_interview/teacher_question_bank.md`

## 6. 兼容说明

- 早期日志里会出现旧路径，例如 `docs/day2_data_hands_on_lab.md`
- 现在的新路径是 `docs/01_data/day2_data_hands_on_lab.md`
- 这是因为文档后来按阶段重组了；历史记录保留，当前导航以本文件为准
