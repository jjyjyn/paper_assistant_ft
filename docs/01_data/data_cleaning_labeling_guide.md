# 数据清洗与标注实操指南（你需要亲手做）

## 目标

把“会跑脚本”升级为“会做数据工程”的能力，后续面试能讲清楚：

- 我如何准备数据
- 我如何清洗数据
- 我如何定义标注标准
- 我如何验证数据可用于训练

## 一、你今天要亲手完成的动作

1. 运行构建脚本

```bash
python scripts/build_dataset_v1.py
```

2. 运行校验脚本

```bash
python scripts/check_dataset_v1.py
```

3. 人工抽检 10 条

- 从 `train_v1.jsonl` 抽 6 条
- 从 `val_v1.jsonl` 抽 2 条
- 从 `test_v1.jsonl` 抽 2 条
- 检查是否“输入可支撑输出、无幻觉、结构清晰”

4. 手动改 3 条样本

- 至少 1 条 `method_comparison`
- 至少 1 条 `experiment_interpretation`
- 至少 1 条 `defense_followup`

5. 记录修改原因

- 把每条修改写进 `docs/00_meta/progress_log.md`（原因 + 修改前后差异）

## 二、清洗规则（面试可直接讲）

### 1) 结构规则

- 每条都必须有：`id/task_type/instruction/input/output/source_case_id`
- `task_type` 必须属于四类固定任务

### 2) 事实规则

- output 只能引用 input 中给的信息
- 不能编造新指标、新基线、新实验结论

### 3) 表达规则

- 要有结构（条目/分点）
- 不写空话（例如“效果很好”），尽量引用具体结果

### 4) 分布规则

- 训练集、验证集、测试集都要覆盖四类任务
- 不允许某一类在 val 中为 0
- 不允许同一 `source_case_id` 跨 split 出现（防泄漏）

## 三、标注一致性（简单标准）

- 贡献提取：必须有“问题-方法-结果-局限”
- 方法对比：必须有“优势-代价”
- 实验解析：必须有“结论-原因-边界”
- 追问答辩：至少 3 组 Q/A，回答要可复述

## 四、你可以怎么讲这段经历

- “我不是只会调用训练命令，我能把原始案例转成可训练 JSONL，并做自动校验与人工抽检。”
- “我做了 case-level 切分，保证 train/val/test 都有四类任务，并拦截跨 split 泄漏。”
- “我记录了修改原因，保证数据改动可追踪，可复盘。”

## 五、清洗常见问题与处理（面试可直接讲）

1. 问题：输出里出现 input 没有的指标或结论（幻觉）
- 处理：回到 `data/raw/paper_cases_v1.json` 修正源信息；重跑 build/check，不直接手改 jsonl。

2. 问题：样本表达过于模板化，信息密度低
- 处理：在 raw case 的 `result/limitations` 补充可量化细节与边界条件，再重建样本。

3. 问题：同一论文案例跨 train/val/test（数据泄漏）
- 处理：使用 case-level split，并在 check 脚本里强制校验 `source_case_id` 不跨集合重复。

4. 问题：只在 in-domain 上效果好，外部泛化差
- 处理：保留独立 external_eval，不参与训练；汇报时同时给出 in-domain + external 结果。

