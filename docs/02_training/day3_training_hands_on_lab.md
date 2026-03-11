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

---

## 10. 补充：一次真实通过的 Smoke 训练应长什么样

### 真实结果样例

- 模型：`Qwen3-4B`
- 训练时长：约 `24.39s`
- `train_loss`: `2.1789`
- `train_samples_per_second`: `2.624`
- `train_steps_per_second`: `0.328`
- `epoch`: `1.0`

### 你应该重点看什么

- 是否打印 `Training completed.`
- 是否打印 `Smoke training finished.`
- 是否生成 checkpoint
- 是否有明显的：
  - OOM
  - 路径错误
  - tokenizer / template 错误
  - 模型初始化错误

### 本项目这次的 smoke 产物

- `outputs/qwen25_3b_lora_v1_smoke/`
- `outputs/qwen25_3b_lora_v1_smoke/checkpoint-8/`

### 如何向老师解释“为什么这次 smoke 算成功”

- “因为它不是只跑到一半，而是完整走完了数据读取、模型加载、训练、checkpoint 保存和训练收尾。”
- “而且它是在真实 Qwen3 路线上跑通的，不是退回到旧模型凑出来的成功。”
- “所以这一步已经足够证明训练链路可用，后面可以合理进入 full。”

---

## 11. 补充：一次真实通过的 Full 训练应长什么样

### 真实结果样例

- 模型：`Qwen3-4B`
- 训练时长：约 `65.01s`
- `train_loss`: `1.6737`
- `train_samples_per_second`: `2.953`
- `train_steps_per_second`: `0.369`
- `epoch`: `3.0`
- 中间日志：
  - `epoch = 1.25` 时 `loss = 2.1071`
  - `epoch = 2.5` 时 `loss = 1.4035`

### 本项目这次的 full 产物

- `outputs/qwen_lora_v1_full/`
- `outputs/qwen_lora_v1_full/training_loss.png`

### 你应该重点看什么

- 是否打印 `Full training finished.`
- 是否成功写出 `training_loss.png`
- 是否存在正式输出目录
- 训练过程中 loss 是否总体下降
- 是否没有出现：
  - OOM
  - 权重路径错误
  - tokenizer / template 错误
  - Qwen3 初始化兼容错误

### 为什么这次 full 只有约 65 秒仍然成立

- 因为当前 v1 数据规模本身较小，所以正式训练不会是几小时级别。
- 这不影响它作为“正式训练闭环”的有效性。
- 当前阶段 full 的主要价值是：
  - 验证正式配置可用
  - 获得正式训练目录与 loss 曲线
  - 为下一步评测和案例分析提供产物

### 你可以这样讲

- “这次 full 的重点不是堆算力，而是把正式训练配置真实跑完，拿到正式产物、日志和 loss 曲线。”
- “由于当前 v1 数据规模不大，所以 full 只用了约一分钟，但它已经足够证明 LoRA 微调闭环在这条 Qwen3 路线上成立。”
- “下一步我会把重点放在 in-domain 和 external 的评测，以及失败样例分析上，而不是盲目继续拉长训练时间。”

---

## 12. 流程 7：正式评测（test_v1 + external_eval_v1）

### 原理

- 训练完成不等于项目完成。
- 你至少要回答两个问题：
  - 模型在项目内分布上表现如何？
  - 模型离开当前分布后是否明显退化？
- 因此评测必须同时覆盖：
  - `test_v1`：项目内测试
  - `external_eval_v1`：独立外部分布测试

### 操作

```bash
cd ~/paper_assistant_ft
export MODEL_PATH=/root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B
export ADAPTER_PATH=outputs/qwen_lora_v1_full
bash scripts/run_eval_v1.sh
```

### 输出

- 目录形如：`outputs/evals/qwen_lora_v1_full_<timestamp>/`
- 每套数据都会生成：
  - `*_predictions.jsonl`
  - `*_summary.json`
  - `*_report.md`

### 当前指标口径

- `exact_match_rate`
- `avg_char_f1`
- 分任务统计
- 最差样例列表

### 怎么理解这些指标

- `exact_match_rate` 更严格，适合看模型是否能稳定复现目标格式和表述。
- `char_f1` 更宽松，适合看生成内容与参考答案的大致重合程度。
- 对这个项目来说，自动指标只能做第一层筛选。
- 真正能支撑你给老师汇报的，还需要：
  - 读 `report.md`
  - 抽高分样例
  - 抽低分样例
  - 总结失败模式

### 你可以这样讲

- “我没有把评测简化成一个准确率数字，而是同时保留了严格匹配、字符级重合度和逐条可读报告。”
- “这样做的目的不是追求某个漂亮分数，而是让结果既可快速比较，也能回到具体样例做失效分析。”

---

## 13. 补充：首轮评测为什么不能直接当最终结果

### 本项目首轮真实结果

- `test_v1`：
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.3804`
- `external_eval_v1`：
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.4090`

### 这是不是说明模型完全没学会

- 不能这样下结论。
- 因为首轮报告中一个非常明显的问题是：
  - 模型把 `<think>` 推理过程直接输出到了最终答案里
- 这会同时破坏：
  - 严格匹配
  - 字符级重合度
  - 人工阅读体验

### 两个代表性失败样例

1. `v1_0012`（`defense_followup`）
- 参考答案要求至少三组 `Q/A`
- 原始输出先给了长段思维链
- 在真正答案区只剩：
  - `以下是模拟答辩老师追问的三`
- 这属于“推理泄露 + 生成截断”的组合问题

2. `ext_v1_0007`（`experiment_interpretation`）
- 参考答案要求“结论-原因-边界-建议”
- 模型输出仍先进入 `<think>` 分析模式
- 说明当前问题不只发生在项目内测试，也影响 external

### 当前正确做法

- 不直接把首轮分数拿去汇报老师
- 先修正评测脚本，剥离 `<think>` 内容
- 再重跑一次 test/external
- 再基于清洗后的预测做最终样例分析

### 你可以这样讲

- “首轮评测不是白跑，它帮我定位到真正的问题不只是能力高低，而是输出控制失败。”
- “这类问题如果不先定位，后面即使继续堆训练轮数，也可能只是继续放大脏评测。”
