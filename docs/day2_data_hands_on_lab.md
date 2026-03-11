# Day 2 实操实验单（你亲手做，按步骤打卡）

> 本文档是“动手版”。每一步都要执行、截图或记录结果。

## Step 0. 进入项目目录

```powershell
cd D:\llm_train\paper_assistant_ft
```

预期：

- 终端路径是 `...paper_assistant_ft`

---

## Step 1. 重新构建数据

```powershell
python scripts/build_dataset_v1.py
```

预期输出（数量可能一致）：

- `Built samples: 80`
- `Train samples: 64`
- `Val samples: 8`
- `Test samples: 8`

你要记录：

- 构建时间
- 样本数量

---

## Step 2. 运行数据校验

```powershell
python scripts/check_dataset_v1.py
```

预期输出：

- `Dataset check passed.`
- train/val/test 四类任务都有数量

你要记录：

- 每类任务在 train/val/test 的数量

---

## Step 3. 导出可读版

```powershell
python scripts/export_dataset_readable.py
```

输出文件：

- `data/processed/train_v1_readable.md`
- `data/processed/val_v1_readable.md`
- `data/processed/test_v1_readable.md`

---

## Step 4. 人工抽检（必须）

打开 `train_v1_readable.md` 抽检 6 条；`val_v1_readable.md` 抽检 2 条；`test_v1_readable.md` 抽检 2 条。

逐条回答：

1. output 是否完全基于 input？
2. 有没有空话或模板痕迹过重？
3. 结构是否清晰（分点、结论-原因-边界）？

---

## Step 5. 手工修改 3 条样本（必须）

要求：

- 覆盖三类任务（至少）
- 每条都说明修改原因

推荐修改位置：

- `data/raw/paper_cases_v1.json`（推荐，源头修改）

不推荐：

- 直接改 `train_v1.jsonl`（短期可行，但难维护）

---

## Step 6. 重跑并对比（必须）

```powershell
python scripts/build_dataset_v1.py
python scripts/check_dataset_v1.py
python scripts/export_dataset_readable.py
```

对比内容：

- 修改前后同一条样本的 output
- 是否更具体、更可解释

---

## Step 7. 写复盘记录（必须）

写入 `docs/progress_log.md`：

1. 你改了哪 3 条（case_id）
2. 为什么改
3. 改完效果
4. 下次还想改哪里

---

## Step 8. 面试表达训练（必须）

用 6 句话总结今天：

1. 今天目标  
2. 我怎么构建数据  
3. 我怎么做校验  
4. 我改了哪些样本  
5. 改动带来什么提升  
6. 下一步训练怎么做

这 6 句话你写完发我，我帮你打磨成“能背”的面试版本。
