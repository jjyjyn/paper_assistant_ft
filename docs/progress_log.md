# 过程记录（Progress Log）

## 2026-03-10（Day 1）

### 完成事项

- 搭建项目文档体系和脚本骨架
- 打通本地与服务器同步链路
- 完成基础环境安装与依赖排查
- 识别学校服务器 GPU 节点稳定性风险

### 结论

- Day 1 目标达成
- 训练执行平台改为“优先租用 4090”

---

## 2026-03-11（Day 2）

### 今日目标

- 完成数据集第一版（schema + 样本 + 构建 + 校验）
- 为明天训练准备可直接执行的配置和脚本

### 今日新增文件

- `docs/dataset_schema.md`
- `data/raw/paper_cases_v1.json`
- `data/raw/seed_samples.md`
- `data/dataset_info.json`
- `data/processed/train_v1.jsonl`
- `data/processed/val_v1.jsonl`
- `scripts/build_dataset_v1.py`
- `scripts/check_dataset_v1.py`
- `configs/dataset_paper_assistant_v1.yaml`
- `configs/lora_sft_qwen25_3b_v1.yaml`
- `scripts/run_train_smoke.sh`

### 今日执行命令（本地）

```bash
python scripts/build_dataset_v1.py
python scripts/check_dataset_v1.py
```

### 结果

- 构建样本总数：80
- 训练集：72
- 验证集：8
- 四类任务分布：
  - train: 18/18/18/18
  - val: 2/2/2/2
- 数据校验：`Dataset check passed.`

### 关键说明

- v1 采用“结构化案例 + 模板扩展”方案，优先保证启动速度和任务覆盖。
- 后续会迭代加入人工高难样本，提高泛化质量。

### 下一步

1. 租用 4090 服务器并初始化环境
2. 执行 smoke 训练（50-100 step）
3. 根据显存/速度反馈调整训练超参

---

## 2026-03-11（文档增强）

### 触发原因

- 用户希望获得“可亲手操作、可面试复述”的完整闭环，而不是简略说明。

### 新增内容

- `docs/llm_finetune_end2end_playbook.md`
- `docs/day2_data_hands_on_lab.md`
- `docs/interview_notes_categorized.md`
- `docs/dataset_reading_guide.md`
- `docs/README_docs.md` 导航增强

### 目标

- 把“我会执行命令”升级为“我能讲清楚每一步为什么、怎么做、结果是什么”。

### 补充动作（数据准备分支）

- 新增 `docs/data_preparation/` 目录，作为数据准备专题分支。
- 新增 `case_004 -> v1_0015` 一一映射文档，解释 case 字段如何进入训练样本。

## 2026-03-11（case 测试记录补充）
- 新增 docs/data_preparation/case_test_log.md。
- 已记录 case_004 的修改内容、重建命令、以及对 v1_0013~v1_0016 的映射影响。
- 后续每次 case 修改都按模板追加，不覆盖历史记录。

## 2026-03-11（case_005 映射验证）
- 完成 case_005 的手工改写，并重建数据集（build/check/export）。
- 确认映射结果：source_case_id=case_005 共 4 条样本（train 3 条 + val 1 条）。
- 样本 ID：v1_0017, v1_0018, v1_0019, v1_0020。
- 结论：单个 raw case 改动可稳定传播到四类任务样本，数据闭环验证通过。

## 2026-03-11（阶段2-第3步：test集 + 防泄漏 + 数据定版）
- 已将数据切分策略从样本级改为 case 级（按 source_case_id 切分）。
- 新增 test 集产物：data/processed/test_v1.jsonl（及 readable 导出）。
- 切分结果：train/val/test = 64/8/8（对应 case 数 16/2/2）。
- 新增检查：三组间 id 不重叠、source_case_id 不重叠，防止数据泄漏。
- 运行结果：python scripts/check_dataset_v1.py -> Dataset check passed.

## 2026-03-11（外部评测集闭环补齐）
- 新增外部评测原始集：data/external_eval/raw/external_eval_cases_v1.json（8 cases）。
- 新增脚本：build_external_eval_v1.py / check_external_eval_v1.py。
- 产物：external_eval_v1.jsonl + readable.json + readable.md（共32样本）。
- 校验结果：External eval check passed（含与主训练case标题/ID防重合）。

## 2026-03-11（数据分集口径确认）
- 已确认当前口径：1 套 train + 1 套 val + 2 套 test（test_v1 + external_eval_v1）。
- 目的：同时覆盖同分布评测与外部泛化评测，减少单一测试结论偏差。

## 2026-03-11 Chat Migration Prep
- Added migration handoff document: `docs/chat_migration_handoff_2026-03-11.md`.
- Document includes: fixed constraints, current dataset/eval status, next-step execution order, and paste-ready prompt block for starting a new Codex chat.
- Goal: avoid token-limit context loss and continue directly from Phase 2 -> Phase 3 (training).

## 2026-03-11（新会话迁移后：Phase 3 训练前准备）

### 本轮目标

- 在新对话窗口无上下文丢失地接续阶段 3。
- 完成训练前可执行性复核，并把训练入口补齐到“一条 smoke + 一条 full”。

### 本轮执行命令（本地）

```bash
python scripts/build_dataset_v1.py
python scripts/check_dataset_v1.py
python scripts/build_external_eval_v1.py
python scripts/check_external_eval_v1.py
```

### 本轮结果

- 主数据构建与校验通过：`train/val/test = 64/8/8`。
- 外部评测构建与校验通过：`external_eval_v1 = 32`。
- 数据链路状态：可复现、可训练、可评测。

### 本轮代码/配置更新

- 更新：`scripts/run_train_smoke.sh`
  - 模型自动探测顺序改为优先 Qwen3-4B，回退 Qwen2.5-3B。
  - 增加 `BASE_CONFIG` 可覆盖参数，便于复用 smoke 脚本。
- 新增：`configs/lora_sft_qwen_v1_full.yaml`
  - 正式训练配置入口（默认 3 epoch，保留输出目录）。
- 新增：`scripts/run_train_full.sh`
  - 正式训练启动脚本，与 smoke 保持同一模型探测逻辑。

### 本轮文档同步

- 更新：`docs/project_plan.md`（Phase 3 状态与执行清单对齐）。
- 更新：`docs/README_docs.md`（加入 Day3 手册导航）。
- 更新：`docs/llm_finetune_end2end_playbook.md`（补 full 训练入口）。
- 更新：`docs/interview_notes.md`（新增 Phase 3 高频追问）。
- 新增：`docs/day3_training_hands_on_lab.md`（按“原理+操作+验收+常见坑”沉淀）。

### 关键结论（阶段口径）

1. 当前已从“训练待启动”推进到“训练执行准备完成”。
2. 训练执行顺序固定为：`server init -> data check -> smoke -> full`。
3. 文档需要持续记录：每次训练的配置、日志路径、loss 变化、失败原因与修复。

## 2026-03-11（训练前文档完备性审计与修正）

### 审计目标

- 检查“训练前准备”是否已可对外稳定复述（保研/面试场景）。
- 检查 docs 是否存在旧口径（72/8、90/10）导致前后冲突。

### 发现与修正

1. `docs/dataset_schema.md`
- 旧口径：90/10 train/val 与 72/8。
- 修正：case-level `64/8/8` + external_eval `32`，并补充防泄漏说明。

2. `docs/day2_data_hands_on_lab.md`
- 旧口径：Step 1 仍写 train 72 / val 8。
- 修正：更新为 train 64 / val 8 / test 8；抽检改为 train/val/test = 6/2/2。

3. `docs/data_cleaning_labeling_guide.md`
- 补充：train/val/test 覆盖要求与 `source_case_id` 防泄漏规则。
- 新增：清洗常见问题与处理（幻觉、模板化、泄漏、外部泛化不足）。

### 结论

- 当前“训练前准备 + 数据准备 + 清洗问题 + 面试追问”四块内容已成体系。
- 剩余工作重心转到：服务器执行 smoke/full，并把真实训练日志继续回填到 docs。
