# 仓库结构总说明

这份文档只回答一件事：`paper_assistant_ft` 这个仓库每一层分别放什么、为什么这样放、遇到问题该先看哪里。

## 1. 顶层结构

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

## 2. 顶层目录逐个解释

### 2.1 `configs/`

用途：保存训练配置和数据配置，尽量只放“声明式”文件，不放实验日志。

当前主要文件：

- `dataset_paper_assistant_v1.yaml`
- `lora_sft_qwen25_3b_v1.yaml`
- `lora_sft_qwen_v1_full.yaml`

适合放在这里的内容：

- LLaMA-Factory 数据集注册相关配置
- LoRA、batch size、epoch、输出路径等训练配置

不适合放在这里的内容：

- shell 命令
- 运行日志
- 手工复盘记录

目录说明见：`configs/README.md`

### 2.2 `data/`

用途：保存从“原始案例”到“训练/评测 JSONL”的全链路数据。

结构：

```text
data/
├─ dataset_info.json
├─ raw/
├─ processed/
└─ external_eval/
```

其中：

- `raw/`：原始案例、种子样本
- `processed/`：训练、验证、测试集
- `external_eval/`：外部评测数据
- `dataset_info.json`：供训练框架读取的数据注册文件

目录说明见：`data/README.md`

### 2.3 `scripts/`

用途：保存所有“可执行动作”。

这里的脚本分四类：

1. 数据构建与校验
2. 训练与评测
3. 服务器初始化与同步
4. 辅助导出

目录说明见：`scripts/README.md`

### 2.4 `outputs/`

用途：保存训练结果、评测结果、预测输出。

注意：

- `outputs/` 默认在 `.gitignore` 中
- 只有明确要保留为证据的结果，才用 `git add -f` 强制提交

目录说明见：`outputs/README.md`

### 2.5 `logs/`

用途：保存运行过程日志。

注意：

- `logs/` 默认不进 Git
- `logs/README.md` 会保留，用来说明目录用途
- 这里适合放原始执行日志，不适合放整理后的结论
- 结论应该回写到 `docs/progress_log.md`

### 2.6 `docs/`

用途：保存“人看的内容”，包括计划、日志、训练手册和面试复盘。

结构：

```text
docs/
├─ README_docs.md
├─ repo_structure_guide.md
├─ project_plan.md
├─ progress_log.md
├─ interview_notes.md
├─ chat_migration_handoff_*.md
├─ 01_data/
├─ 02_training/
└─ 03_interview/
```

目录说明见：`docs/README_docs.md`

## 3. 根目录文件各自干什么

### 3.1 `README.md`

作用：给第一次进仓库的人看，告诉他：

- 这是个什么项目
- 现在做到哪一步
- 仓库从哪开始读
- 各主目录分别干什么

### 3.2 `.gitignore`

作用：控制哪些运行产物默认不进版本库。

当前要点：

- `outputs/` 默认忽略
- `logs/` 默认忽略
- Python 缓存默认忽略

## 4. 你最常见的工作路径

### 4.1 如果你在做数据

1. 看 `data/README.md`
2. 看 `docs/01_data/dataset_schema.md`
3. 改 `data/raw/`
4. 跑 `scripts/build_dataset_v1.py`
5. 跑 `scripts/check_dataset_v1.py`

### 4.2 如果你在做训练

1. 看 `scripts/README.md`
2. 看 `configs/README.md`
3. 先 smoke：`scripts/run_train_smoke.sh`
4. 再 full：`scripts/run_train_full.sh`

### 4.3 如果你在做评测

1. 看 `scripts/run_eval_v1.sh`
2. 输出会到 `outputs/evals/<run_name>/`
3. 重点先看 `*_summary.json`
4. 再看 `*_report.md`
5. 最后看 `*_predictions.jsonl`

### 4.4 如果你在做复盘或面试准备

1. 看 `docs/project_plan.md`
2. 看 `docs/progress_log.md`
3. 看 `docs/interview_notes.md`
4. 看 `docs/03_interview/teacher_question_bank.md`

## 5. 哪些文件是“代码”，哪些是“项目资产”

### 5.1 代码与脚本

- `scripts/*.py`
- `scripts/*.sh`
- `configs/*.yaml`

### 5.2 数据资产

- `data/raw/*`
- `data/processed/*`
- `data/external_eval/*`

### 5.3 过程资产

- `docs/project_plan.md`
- `docs/progress_log.md`
- `docs/interview_notes.md`
- `docs/chat_migration_handoff_*.md`

### 5.4 实验资产

- `outputs/evals/*`
- `logs/*`

## 6. 为什么当前结构是这样

这套结构遵循一个简单原则：

- 机器执行的东西放 `scripts/` 和 `configs/`
- 数据资产放 `data/`
- 运行产物放 `outputs/` 和 `logs/`
- 需要长期复述、复盘、迁移的内容放 `docs/`

这样拆分的好处是：

1. 改脚本时不会混进复盘内容
2. 看数据时不需要翻训练手册
3. 面试准备时可以直接进入 `docs/03_interview/`
4. 服务器运行结果可以按需回收，不污染主代码区

## 7. 当前推荐的阅读入口

- 看仓库总貌：`README.md`
- 看目录解释：`docs/repo_structure_guide.md`
- 看文档地图：`docs/README_docs.md`
- 看脚本地图：`scripts/README.md`
- 看数据地图：`data/README.md`
- 看配置地图：`configs/README.md`
- 看日志目录说明：`logs/README.md`
- 看输出地图：`outputs/README.md`
