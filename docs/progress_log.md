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
