# 项目计划（Project Plan）

## 当前阶段

- 阶段 1：环境与仓库跑通（已完成）
- 阶段 2：数据集第一版制作（已完成）
- 阶段 3：LoRA 微调训练与评测闭环（已完成）
- 阶段 4：仓库结构整理与物理重构（进行中：已完成 docs 批次）

## 阶段状态

1. 环境与仓库跑通（Done）
- 本地/服务器同步链路已通
- LLaMA-Factory 可运行
- 已准备租用服务器执行方案

2. 数据集第一版（Done - v1）
- 已完成四类任务统一 schema
- 已完成结构化案例库 + 自动扩展脚本
- 主数据分集（case-level）：`train/val/test = 64/8/8`
- 外部评测分集：`external_eval_v1 = 32`（8 case x 4 任务）
- 已通过 build/check/export + 防泄漏校验

3. LoRA 微调训练与评测闭环（Done）
- 已完成训练前检查（主数据 + external_eval 校验全部通过）
- 已完成租用服务器环境重建与版本固定（无卡模式验证通过）
- 已完成 smoke 训练脚本升级：优先 `Qwen3-4B`，兼容回退 `Qwen2.5-3B-Instruct`
- 已新增正式训练入口：
  - `configs/lora_sft_qwen_v1_full.yaml`
  - `scripts/run_train_full.sh`
- 已完成 full 训练
- 已完成 baseline / clean / hardening / no-think 多轮评测
- 已完成 `no-think` 生效验证，最佳目录：
  - `outputs/evals/qwen_lora_v1_full_2026-03-13_082359_nothink/`

4. 仓库结构整理与物理重构（In Progress）
- 已完成根 README、目录 README、文档导航清理
- 已完成 docs 物理迁移第一批：
  - `docs/README.md`
  - `docs/00_meta/`
  - `docs/00_meta/handoffs/`
  - `docs/03_interview/interview_notes_quick.md`
- 下一步聚焦：
  - `scripts/` 命名空间拆分
  - `configs/` 分层
  - `data/processed/` 物理分层评估

## 今日执行清单（Phase 3 启动日）

1. 服务器准备
- 执行：`bash scripts/server_rental_init.sh`
- 验收：
  - `torch.cuda.is_available() == True`
  - `llamafactory-cli version` 正常输出

2. 数据口径冻结与复核
- 执行：
  - `python scripts/build_dataset_v1.py`
  - `python scripts/check_dataset_v1.py`
  - `python scripts/build_external_eval_v1.py`
  - `python scripts/check_external_eval_v1.py`
- 验收：
  - 主数据 `64/8/8`
  - external_eval `32`
  - 检查脚本均输出 `passed`

3. 冒烟训练（低成本验链路）
- 执行：
  - `export MODEL_PATH=/root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B`
  - `bash scripts/run_train_smoke.sh`
- 验收：
  - 训练完整启动并结束
  - `outputs/` 下出现日志和 checkpoint
  - 无 OOM/路径错误/字段错误

4. 正式训练（smoke 通过后）
- 执行：
  - `export MODEL_PATH=/root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B`
  - `bash scripts/run_train_full.sh`
- 验收：
  - loss 曲线可见且总体下降
  - `outputs/qwen_lora_v1_full` 产物完整

## 风险与应对

- 风险：学校服务器节点 GPU 不稳定
  - 应对：默认在租用 4090 上训练，学校节点仅做备份

- 风险：训练时间超预算
  - 应对：先 smoke 再 full；根据显存和吞吐调整 batch/accum/cutoff_len

- 风险：模型路径命名不一致（Qwen3/Qwen2.5 目录差异）
  - 应对：脚本自动探测；必要时手动设置 `MODEL_PATH`

## 阶段3固定口径（训练与汇报）

- 训练集：`data/processed/train_v1.jsonl`
- 验证集：`data/processed/val_v1.jsonl`
- 项目内测试集：`data/processed/test_v1.jsonl`
- 外部测试集：`data/external_eval/processed/external_eval_v1.jsonl`
- 原则：训练与早停只用 train/val；汇报必须同时给出 in-domain + external 两组结果

## 2026-03-11 补充：GPU Smoke Ready

- 当前状态不是“还在准备环境”，而是“训练前准备已经闭环”。
- 已完成的前置条件：
  - `paper_ft` 环境固定并通过 `pip check`
  - `check_dataset_v1.py` 通过
  - `check_external_eval_v1.py` 通过
  - `Qwen3-4B` 模型已下载到服务器本地
- 当前实测模型路径：
  - `/root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B`
- 当前实测模型目录：
  - `config.json` 存在
  - `tokenizer_config.json` 存在
  - 三个权重分片存在
  - 总大小约 `7.6G`
- 因此下一步不是继续下载或继续配环境，而是：
  - 切回 GPU 模式
  - 先做 `cuda` 验证
  - 直接执行 `bash scripts/run_train_smoke.sh`

## 2026-03-11 补充：Smoke Training Passed

- `Qwen3-4B` 已在 GPU 模式下完成一次真实 `smoke` 训练。
- 本次 `smoke` 关键结果：
  - `train_runtime = 24.392s`
  - `train_loss = 2.1789`
  - `train_samples_per_second = 2.624`
  - `train_steps_per_second = 0.328`
  - `epoch = 1.0`
- 训练成功写出：
  - `outputs/qwen25_3b_lora_v1_smoke/`
  - `outputs/qwen25_3b_lora_v1_smoke/checkpoint-8/`
- 结论：
  - 链路已通
  - `Qwen3-4B + LoRA + 当前数据集 + 当前环境` 可以稳定启动并完整结束
  - 下一步可进入 `full`

说明：
- `output_dir` 仍保留旧命名 `qwen25_3b_lora_v1_smoke`，这是配置文件历史命名遗留，不影响本次 `smoke` 的真实性和有效性。

## 2026-03-11 补充：Full Training Passed

- `Qwen3-4B` 已在 GPU 模式下完成一次真实 `full` 训练。
- 本次 `full` 关键结果：
  - `train_runtime = 65.0085s`
  - `train_loss = 1.6737`
  - `train_samples_per_second = 2.953`
  - `train_steps_per_second = 0.369`
  - `epoch = 3.0`
- 训练过程中记录到的代表性 loss：
  - `epoch = 1.25` 时，`loss = 2.1071`
  - `epoch = 2.5` 时，`loss = 1.4035`
- 训练成功写出：
  - `outputs/qwen_lora_v1_full/`
  - `outputs/qwen_lora_v1_full/training_loss.png`
- 结论：
  - 当前 `Qwen3-4B + LoRA + v1 数据集 + 当前环境` 已完成正式训练闭环
  - 这一步的价值不在于长时间刷算力，而在于拿到正式训练产物、loss 曲线和可复现日志
  - 下一步应从“训练是否能跑”转到“效果如何评估”和“失败案例如何复盘”

说明：
- 本次 `full` 只用时约 `65s`，是因为当前 v1 数据规模较小，不代表训练无效。
- 对当前阶段而言，这个 `full` 已足够证明：
  - 正式配置可运行
  - 输出目录、日志、loss 曲线都可稳定产出
  - 该项目已经从“训练前准备”推进到“正式训练已完成，待评测/待分析”

## 2026-03-11 补充：Evaluation Ready

- 仓库已补充正式评测入口：
  - `scripts/eval_lora_model.py`
  - `scripts/run_eval_v1.sh`
- 评测覆盖两套数据：
  - `data/processed/test_v1.jsonl`
  - `data/external_eval/processed/external_eval_v1.jsonl`
- 评测输出包括：
  - 逐条预测 `*.jsonl`
  - 汇总指标 `*_summary.json`
  - 可读报告 `*_report.md`
- 当前评测口径：
  - `exact_match_rate`
  - `avg_char_f1`
  - 分任务统计
  - 最差样例列表
- 结论：
  - 现在项目已从“只有训练结果”推进到“具备可执行评测流程”
  - 下一步应在服务器运行 `bash scripts/run_eval_v1.sh`，拿到 in-domain 与 external 两组结果

## 2026-03-12 补充：First Evaluation Run Finished

- 已完成首轮正式评测，目录为：
  - `outputs/evals/qwen_lora_v1_full_2026-03-11_234402/`
- 首轮结果：
  - `test_v1`：
    - `exact_match_rate = 0.0000`
    - `avg_char_f1 = 0.3804`
  - `external_eval_v1`：
    - `exact_match_rate = 0.0000`
    - `avg_char_f1 = 0.4090`
- 当前判断：
  - 这轮结果可以用于发现失败模式
  - 但不应直接当作最终模型效果结论

原因：
- 报告显示预测中普遍出现 `<think> ... </think>` 推理内容泄露。
- 这会显著拉低 `exact_match_rate`，并污染 `char_f1`。
- 因此当前首轮评测更适合作为“输出控制问题定位”，而不是“最终任务能力打分”。

下一步：
- 使用已修正的 `scripts/eval_lora_model.py` 重新评测
- 在评测时剥离 `<think>` 残留，并保留 `raw_prediction` 供失败分析
- 再更新最终版 in-domain / external 结果

## 2026-03-12 补充：Third Evaluation Run Confirmed Clean Metrics

- 第三轮评测目录：
  - `outputs/evals/qwen_lora_v1_full_2026-03-12_180125/`
- 第三轮结果：
  - `test_v1`
    - `exact_match_rate = 0.0000`
    - `avg_char_f1 = 0.0050`
  - `external_eval_v1`
    - `exact_match_rate = 0.0000`
    - `avg_char_f1 = 0.0000`
- 这轮结果的正确解释：
  - 这是第一轮真正把 `<think>` 从评分通道剥离后的干净结果。
  - 前两轮 `0.38~0.41` 的 `char_f1` 主要被长段推理文本虚高了。
  - 当前真实问题不再是评测脚本，而是最终答案通道经常为空、残句或未落到目标模板。

结论：
- 第三轮之后，不再需要怀疑评测脚本是否生效。
- 后续优化重点应切换到输出控制与模板收束。

## 2026-03-12 补充：Fourth Iteration Entry Condition Confirmed

- 已完成训练目标审计：
  - `train_v1.jsonl` 共 `64` 条
  - `<think>` 出现次数 = `0`
  - 四类任务各 `16` 条
  - `output_len_avg ≈ 244.3`
- 审计结论：
  - 训练标签本身没有 `<think>` 污染。
  - 当前问题更像生成阶段的输出控制失败，而不是标签脏数据。
- 第四轮最小改动点：
  - 强化 `instruction` 中“只输出最终答案”的约束
  - 为四类任务写死更明确的输出模板
  - 在评测 summary 中补充 `empty_prediction_rate`、`raw_think_rate`、`cleaned_changed_rate`
- 第四轮的目标不是先追高分，而是先验证：
  - 空答案率是否下降
  - 残句率是否下降
  - 模板结构是否开始稳定

## 2026-03-12 补充：Fourth Iteration Hardening Applied

- 已落地的第四轮最小改动：
  - 重写 `scripts/build_dataset_v1.py`
  - 重写 `scripts/build_external_eval_v1.py`
  - 将四类任务统一改为固定字段输出，而不是宽松长段回答
  - 保留并前置“只输出最终答案，不要输出 `<think>`”规则
  - 在 `scripts/eval_lora_model.py` 中新增 `structure_ok_rate`
- 当前四类固定模板：
  - `contribution_extraction`
    - `核心问题`
    - `方法要点`
    - `相对基线增益`
    - `局限性`
  - `method_comparison`
    - `对比对象`
    - `新方法机制`
    - `主要优势`
    - `量化结果`
    - `代价与风险`
    - `结论`
  - `experiment_interpretation`
    - `结论`
    - `原因`
    - `边界`
    - `建议`
  - `defense_followup`
    - `Q1/A1/Q2/A2/Q3/A3`
- 已完成本地验证：
  - 数据重建通过
  - 主数据检查通过
  - external eval 检查通过
  - 三个脚本 `py_compile` 通过
- 下一步：
  - 用这版硬模板重新上服务器做第四轮 `smoke/full/eval`
  - 重点关注：
    - `empty_prediction_rate`
    - `structure_ok_rate`
    - `raw_think_rate`

## 2026-03-12 补充：Fourth Iteration Server Execution Blocker Captured

- 本地第四轮入口检查已完成：
  - `git status -sb` 为干净工作区
  - `check_dataset_v1.py` 通过
  - `check_external_eval_v1.py` 通过
  - 关键脚本 `py_compile` 通过
- 当前阻塞：
  - 连接训练服务器命令
    - `ssh -p 15912 root@connect.bjb1.seetacloud.com "echo connected && hostname && pwd"`
  - 返回 `Connection refused`
- 结论：
  - 问题在服务器可达性，不在本地代码与数据链路
  - 第四轮真实 `smoke/full/eval` 仍处于待执行状态
- 解锁后按固定顺序继续：
  1. `git pull --ff-only`
  2. `python scripts/check_dataset_v1.py`
  3. `python scripts/check_external_eval_v1.py`
  4. `bash scripts/run_train_smoke.sh`
  5. `bash scripts/run_train_full.sh`
  6. `bash scripts/run_eval_v1.sh`

## 2026-03-12 补充：Fourth Iteration Closed-Loop Result and Next Gate

- 最新完成目录：
  - `outputs/evals/qwen_lora_v1_full_2026-03-12_212350/`
- 本轮关键指标：
  - `test_v1`
    - `avg_char_f1 = 0.5105`
    - `empty_prediction_rate = 0.125`
    - `structure_ok_rate = 0.625`
    - `raw_think_rate = 1.0`
  - `external_eval_v1`
    - `avg_char_f1 = 0.4350`
    - `empty_prediction_rate = 0.25`
    - `structure_ok_rate = 0.34375`
    - `raw_think_rate = 1.0`
- 状态判断：
  - 相比第三轮“接近 0”的干净分数，本轮已恢复到可分析区间。
  - 但原始输出中的 `<think>` 泄漏仍是系统级主故障（`raw_think_rate = 1.0`）。
- 当前最高优先：
  - 不先加训练时长，先做推理口径 A/B（默认 vs no-think）。
  - 先验证输出通道是否真正收敛，再决定是否进入下一轮重训。
- 已加到脚本的能力：
  - `scripts/eval_lora_model.py` 支持 `--disable-thinking`
  - `scripts/run_eval_v1.sh` 支持：
    - `DISABLE_THINKING=0/1`
    - `RUN_TAG=<text>`

## 2026-03-13 补充：No-Think Gate Passed

- 完成目录：
  - `outputs/evals/qwen_lora_v1_full_2026-03-13_082359_nothink/`
- Gate 结果：
  - `test_v1`
    - `raw_think_rate = 0.0`
    - `empty_prediction_rate = 0.0`
    - `structure_ok_rate = 1.0`
    - `avg_char_f1 = 0.6698`
  - `external_eval_v1`
    - `raw_think_rate = 0.0`
    - `empty_prediction_rate = 0.0`
    - `structure_ok_rate = 1.0`
    - `avg_char_f1 = 0.6990`
- 结论：
  - 输出通道主故障（`<think>` 泄漏）已被推理口径控制显著修复。
  - 短期内不需要盲目追加训练时长，优先固化推理策略与流程防呆。
- 流程防呆（已落地）：
  - `run_eval_v1.sh` 新增 fail-fast：
    - 若 `RUN_TAG` 包含 `nothink` 但 `DISABLE_THINKING` 未开启，直接退出。
  - `run_eval_v1.sh` 对非法 `OMP_NUM_THREADS` 增加自动纠正。
