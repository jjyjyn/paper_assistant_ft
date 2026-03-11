# Case 测试变更日志（Data Preparation）

这个文档用于持续记录你每次修改 `data/raw/paper_cases_v1.json` 后，对训练样本产生了什么影响。  
目标是让你后续能清楚讲出“我改了什么、为什么改、改完模型会学到什么”。

---

## 记录 #001（2026-03-11）

### 1. 本次测试目标

- 验证：手工修改单个原始 case 后，是否会稳定映射到对应的 4 条任务样本。
- 目标 case：`case_004`（Token Pruning for Efficient Chinese LLM Inference）

### 2. 你做了哪些修改（原始 case 层）

- 修改文件：`data/raw/paper_cases_v1.json`
- 修改点：
1. `result` 字段从“单句指标结论”扩展为“指标 + 适用场景补充（超长文/一般问答）+ 边界提醒”。
2. `limitations` 字段从“单句局限”扩展为“局限 + 更容易出问题的场景（跨段落/跨章节）”。

### 3. 重建与校验动作

执行命令（本地）：

```bash
python scripts/build_dataset_v1.py
python scripts/check_dataset_v1.py
python scripts/export_dataset_readable.py
```

### 4. 影响到哪些训练样本（映射层）

`source_case_id = case_004` 的 4 条样本均被更新（结构不变，文本内容更新）：

- `v1_0013`：`contribution_extraction`
- `v1_0014`：`method_comparison`
- `v1_0015`：`experiment_interpretation`
- `v1_0016`：`defense_followup`

### 5. 变化结论（你在复盘/面试可直接说）

1. 你改的是“原始知识素材”（raw case），不是直接改训练样本。
2. 一条 case 会扇出成四种任务视角；因此一处修改会同步影响四类能力。
3. 本次修改让样本从“只会报指标”升级为“会说明适用范围与风险边界”，更贴近答辩问答场景。
4. 样本字段结构保持稳定（`task_type/instruction/id/source_case_id` 不变），只有 `input/output` 内容随 case 文本变化。

### 6. 本次产物变更文件

- `data/raw/paper_cases_v1.json`
- `data/processed/train_v1.jsonl`
- `data/processed/train_v1_readable.json`
- `data/processed/train_v1_readable.md`

---

## 后续追加模板（每改一个 case 复制一段）

```md
## 记录 #00X（YYYY-MM-DD）

### 1. 本次测试目标
- 目标 case：
- 想验证的点：

### 2. 你做了哪些修改（原始 case 层）
- 修改文件：
- 修改字段：
1.
2.

### 3. 重建与校验动作
```bash
python scripts/build_dataset_v1.py
python scripts/check_dataset_v1.py
python scripts/export_dataset_readable.py
```

### 4. 影响到哪些训练样本（映射层）
- id：
- task_type：

### 5. 变化结论（复盘口径）
1.
2.
3.

### 6. 本次产物变更文件
- data/raw/...
- data/processed/...
```

