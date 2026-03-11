# Day 3 训练实操与复述手册（Phase 3）

> 目标：不是“我会跑命令”，而是“我能解释每个流程为什么这样做、怎么验收、哪里容易踩坑”。
> 环境搭建与版本固定问题，优先配合 `docs/02_training/environment_setup_guide.md` 一起看。

## 0. 你当前要达成的结果

- 结果 1：在 4090 服务器上稳定跑通 smoke 训练。
- 结果 2：在 smoke 通过后启动 full 训练并记录关键日志。
- 结果 3：把训练过程沉淀为可复述的工程闭环（可讲给老师/面试官）。

## 1. 全流程顺序（固定）

1. 服务器准备
2. 数据口径冻结与复核
3. 冒烟训练（smoke）
4. 基于 smoke 调参与风险收敛
5. 正式训练（full）
6. 训练记录与复盘输出

---

## 2. 流程 1：服务器准备

### 原理

- 训练失败最常见原因不是模型本身，而是环境和依赖不一致。
- 先把 CUDA / torch / LLaMA-Factory 跑通，能避免后续“计费中排错”。

### 操作

```bash
cd ~/paper_assistant_ft
bash scripts/server_rental_init.sh
```

### 验收

- `nvidia-smi` 能看到 GPU。
- `torch.cuda.is_available()` 为 True。
- `llamafactory-cli version` 有输出。

### 常见坑

- conda 环境未激活就直接跑训练。
- CUDA 版本和 torch wheel 不匹配。
- 磁盘空间不足导致中途写 checkpoint 失败。

### 你可以这样讲

- “我先做环境验收，再开训练，这一步是在控制失败成本和 GPU 计费风险。”

---

## 3. 流程 2：数据口径冻结与复核

### 原理

- 训练前必须固定数据口径，否则结果不可复现。
- 当前项目采用 case-level split，核心是防止同一论文案例跨集合泄漏。

### 操作

```bash
cd ~/paper_assistant_ft
python scripts/build_dataset_v1.py
python scripts/check_dataset_v1.py
python scripts/build_external_eval_v1.py
python scripts/check_external_eval_v1.py
```

### 验收

- 主数据：`train/val/test = 64/8/8`。
- 外部评测：`external_eval_v1 = 32`。
- 输出包含 `Dataset check passed.` 与 `External eval check passed.`。

### 常见坑

- 忘记重建数据，直接用旧文件开始训练。
- external_eval 被误混到训练集。
- 只看样本数量，不看 leakage 检查。

### 你可以这样讲

- “我在训练前先冻结数据口径，并用脚本把泄漏风险前置拦截。”

---

## 4. 流程 3：冒烟训练（smoke）

### 原理

- smoke 的作用是验证训练链路，不是追求最终指标。
- 先用短任务发现路径/配置/OOM 问题，比直接 full 更省钱。

### 操作

```bash
cd ~/paper_assistant_ft
export MODEL_PATH=/root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B
bash scripts/run_train_smoke.sh
```

备注：脚本已支持自动探测模型目录，优先 Qwen3-4B，回退 Qwen2.5-3B。

### 验收

- 训练能完整启动并结束。
- `outputs/` 下有日志与 checkpoint。
- 无 OOM、无路径错误、无数据字段错误。

### 常见坑

- `MODEL_PATH` 路径错误。
- 直接在错误目录执行脚本。
- 忘记先跑数据 check，导致训练中才报字段错误。

### 你可以这样讲

- “smoke 是我在正式训练前的技术闸门，目的是低成本验证链路完整性。”

---

## 5. 流程 4：基于 smoke 调参与风险收敛

### 原理

- 调参不是盲调，先看显存和吞吐，再改 batch/accum/cutoff_len。
- 目标是稳定训练，而不是盲目追大 batch。

### 操作

- 优先调整参数：
  - `per_device_train_batch_size`
  - `gradient_accumulation_steps`
  - `cutoff_len`
- 记录每次改动前后：
  - 显存峰值
  - step 时间
  - 是否 OOM

### 验收

- 训练过程无 OOM。
- 速度稳定，无明显吞吐抖动。
- loss 曲线可观察且不异常发散。

### 常见坑

- 一次改太多参数，无法定位因果。
- 只看 train loss，不看 val 趋势。

### 你可以这样讲

- “我把调参当作受控实验，每次只改关键变量并记录前后对比。”

---

## 6. 流程 5：正式训练（full）

### 原理

- full 训练在 smoke 通过后进行，目的是拿到可汇报的主模型产物。
- 正式训练配置应独立于 smoke，避免误覆盖。

### 操作

```bash
cd ~/paper_assistant_ft
export MODEL_PATH=/root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B
bash scripts/run_train_full.sh
```

对应配置：`configs/lora_sft_qwen_v1_full.yaml`

### 验收

- 输出目录：`outputs/qwen_lora_v1_full`。
- 有可读取的日志、checkpoint、loss 曲线。
- 训练未中断，关键超参有记录。

### 常见坑

- 沿用 smoke 输出目录导致结果混淆。
- 训练中断后未保存环境信息，难以复现。

### 你可以这样讲

- “正式训练我用独立配置和输出目录，确保实验结果可追踪、可复现。”

---

## 7. 流程 6：训练记录与复盘输出

### 原理

- 项目价值不只在跑通，还在于你能给出可审计的工程记录。

### 你要记录到文档的最小集

1. 训练环境：GPU、torch、llamafactory 版本
2. 数据口径：train/val/test/external 的文件与数量
3. 训练配置：核心超参 + 模型路径
4. 训练结果：loss 变化、最佳 checkpoint、异常与修复
5. 结论：下一轮改进计划

建议更新文件：
- `docs/progress_log.md`
- `docs/project_plan.md`
- `docs/interview_notes.md`

---

## 8. 60 秒口头复述模板（可直接背）

“我的流程是先把训练环境和数据口径固定，再用 smoke 低成本验证训练链路，确认无路径和显存问题后再启动 full 训练。训练过程中我重点记录 loss、吞吐和异常日志，所有改动都回写文档，保证实验可复现。评测上我会同时看 in-domain test 和 external_eval，避免只在单一分布上得出乐观结论。”

---

## 9. 补充：模型预下载与 GPU 开机前检查

### 原理

- 大模型下载不应占用付费 GPU 时间。
- 真正省钱的做法是：无卡模式完成模型预下载，GPU 模式只跑训练。

### 操作

无卡模式完成后，至少确认：

```bash
du -sh /root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B
ls -lh /root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B/config.json
ls -lh /root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B/tokenizer_config.json
```

GPU 开机后再执行：

```bash
python - <<'PY'
import torch
print("cuda:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("gpu:", torch.cuda.get_device_name(0))
PY
```

### 验收

- 模型目录约 `7.6G`
- 配置文件存在
- `cuda: True`
- GPU 名称包含 `RTX 4090`

### 你可以这样讲

- “我把模型下载前移到无卡模式，把 GPU 时间专门留给训练，这样既节省成本，也让训练窗口更纯净。”
