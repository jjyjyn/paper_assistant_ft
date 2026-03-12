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

---

## 14. 补充：你应该怎么自己看评测报告

### 第一步：先看 summary，不要急着下结论

当前首轮结果：

- `test_v1`
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.3804`
- `external_eval_v1`
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.4090`

正确读法：

- `exact_match_rate` 是最严格指标，只要输出里混入 `<think>`、格式多一行、顺序不同，都会直接记为不完全匹配。
- `avg_char_f1` 更像“内容重合度”，能反映模型有没有答到一些关键内容，但无法区分“答得像”和“答得干净”。
- 因此，当 `exact_match = 0` 但 `char_f1` 还有 `0.38~0.41` 时，更合理的解释通常不是“完全不会”，而是：
  - 内容学到了一部分
  - 输出格式或答案通道出了问题

### 第二步：再看 worst_examples

`worst_examples` 的作用不是让你背编号，而是帮助你定位“最典型的失败模式”。

这次首轮评测里，最值得先看的 3 个样例是：

1. `test_v1 / v1_0012 / defense_followup`
- 目标：至少输出 3 组 `Q/A`
- 实际：先输出长段 `<think> ... </think>`，最后只剩一句残缺文本
- 说明：这是“推理泄露 + 最终答案截断”

2. `test_v1 / v1_0062 / method_comparison`
- 目标：输出结构化方法对比
- 实际：模型长时间停留在“我现在需要帮助用户分析……”这种自我分析句式
- 说明：模型知道任务方向，但没有稳定落到目标模板

3. `external_eval_v1 / ext_v1_0007 / experiment_interpretation`
- 目标：按“结论-原因-边界-建议”作答
- 实际：同样先输出 `<think>` 推理，再把正式答案污染掉
- 说明：这个问题不是只发生在 in-domain，external 上也有

### 第三步：看报告时要回答的不是“对不对”，而是“错在哪”

建议你每看一个低分样例，都按这 4 个问题判断：

1. 模型有没有抓住任务方向
2. 模型有没有输出到正确格式
3. 错误是事实错、结构错，还是 `<think>` 污染
4. 这是单点样例问题，还是系统性问题

### 你可以这样讲

- “我看评测报告时，不是只盯着分数，而是先判断它是知识错误、格式错误，还是评测污染。”
- “这次最关键的发现不是某一道题答错了，而是很多样例都把 `<think>` 一起输出了，所以我先修评测口径，再谈模型能力。”
## 15. 补充：坏结果为什么也是有效项目经历

### 你这次项目里，坏结果的价值在哪里

- 你不是只跑出一个低分，然后停下。
- 你已经完成了：
  - 数据准备
  - 环境搭建
  - smoke 训练
  - full 训练
  - 首轮评测
  - 失败样例定位
- 这已经是一个完整的 LoRA 微调闭环。

### 这次首轮评测该怎么讲

- `test_v1`
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.3804`
- `external_eval_v1`
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.4090`

正确讲法不是“模型彻底失败”，而是：

- 这轮结果首先暴露了输出控制问题。
- 报告里大量样例都把 `<think>` 一起输出了。
- 部分样例还出现了答案截断和结构不稳定。
- 所以这一轮评测首先是“故障定位轮”，不是“最终能力打分轮”。

### 你应该优先能讲清楚的 3 个样例

1. `v1_0012`
- 任务：输出至少 3 组 `Q/A`
- 问题：先输出 `<think>`，最后答案被截断成“以下是模拟答辩老师追问的三”
- 解释：模型有方向，但最终答案通道坏了

2. `v1_0062`
- 任务：结构化方法对比
- 问题：模型一直停留在自我分析，没有稳定落到目标模板
- 解释：属于模板收束失败，不是纯知识错误

3. `ext_v1_0007`
- 任务：按“结论-原因-边界-建议”解释结果
- 问题：external 上仍出现 `<think>` 泄露
- 解释：说明这是系统性输出控制问题，不是某几个 in-domain 样例偶发

### 你可以这样和老师说

- “我这次项目的重点不是只拿一次漂亮分数，而是完整走通数据、训练、评测、错误分析和修正闭环。”
- “首轮结果不好并不意味着项目失败，因为我已经从具体失败样例里定位到了 `<think>` 泄露、答案截断和格式不稳定这些可修复问题。”
- “对一个第一次自己做大模型微调的人来说，这一步经验非常关键，因为它说明我不是只会跑脚本，而是会做结果解释和故障定位。”

## 16. 补充：如果第二轮重跑后结果完全一样，该怎么处理

### 先做什么，不要先猜

- 不要一上来就说“模型没变化”。
- 先核对产物本身。

建议最少核对：

- 新旧 `test_v1_summary.json`
- 新旧 `external_eval_v1_summary.json`
- 新旧 `report.md`

如果这几份文件连哈希都一样，那说明问题已经不是“效果接近”，而是“评测产物逐字相同”。

### 这次项目里的真实结论

- 第二轮评测目录和首轮不同，但关键产物哈希完全一致。
- 新报告里仍然能直接看到 `<think>` 出现在 `Prediction` 区域。
- 因此更合理的解释是：
  - 第二轮没有真正把新的清洗逻辑应用到结果产物
  - 或者服务器实际上仍在运行旧版评测脚本

### 正确的工程处理顺序

1. 确认服务器上的评测脚本是否已经更新
2. 确认重跑前是否真的拉取了最新代码
3. 确认报告展示的是清洗后输出还是原始输出
4. 再决定是否进入第三轮评测

### 你可以这样讲

- “第二轮我没有只盯着控制台说‘已经重跑过了’，而是继续做了文件级核对，确认新旧产物其实逐字一致。”
- “这说明问题不只是模型本身，还可能是评测流程没有真正切换到新逻辑。对工程项目来说，能区分模型问题和流程问题同样重要。”

### 这次项目里最终查到的真实根因

- 不是模型问题。
- 是版本同步问题。

具体来说：

- 本地修复 `<think>` 清洗逻辑的提交在：
  - `536e214`
- 服务器能 `git pull` 到的远端分支仍停在：
  - `cf77f84`

所以第二轮服务器评测实际上还是在跑旧版 `scripts/eval_lora_model.py`。

这也是为什么第二轮会出现：

- 指标完全一样
- 报告完全一样
- `Prediction` 里仍然直接有 `<think>`
- `predictions.jsonl` 里也没有 `raw_prediction`

### 你可以这样讲

- “我后面把问题继续查到了版本同步层。不是我修了脚本却没有效果，而是服务器当时还在运行旧版评测脚本，因为修复提交还没真正同步到远端分支和服务器工作区。” 


## 17. ????????????????????

### ??????????

- ??? / ????
  - `test_v1 avg_char_f1 ? 0.3804`
  - `external_eval_v1 avg_char_f1 ? 0.4090`
- ?????? `<think>` ???
  - `test_v1 avg_char_f1 ? 0.0050`
  - `external_eval_v1 avg_char_f1 = 0.0000`

### ????

- ????????????????
- ????????
  - ??????? `<think>` ??????
  - ????????????????????????????

### ????????

1. `Prediction`
- ?????????????

2. `Raw Prediction`
- ?????????
- ??????? `<think>`?? `Prediction` ???????????????????

### ??????????

1. `v1_0012`
- `Raw Prediction` ???
- `Prediction` ??????????????????
- ?????????????????????

2. `v1_0062`
- `Raw Prediction` ?????????
- `Prediction` ???
- ?????????????????????????

### ????????

- ??????????????????????????
- ????? `<think>` ??????????????????????????????????????
- ???????????????????????????????????

### ???????

1. ????????????????????
2. ????????????????
3. ?????????/????/???????????????????
4. ?????????????????????????????????
