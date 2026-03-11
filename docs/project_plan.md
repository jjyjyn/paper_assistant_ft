# 项目计划（Project Plan）

## 当前阶段

- 阶段 1：环境与仓库跑通（已完成）
- 阶段 2：数据集第一版制作（已完成）
- 阶段 3：LoRA 微调训练（进行中：已完成训练前准备）

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

3. LoRA 微调训练（In Progress）
- 已完成训练前检查（主数据 + external_eval 校验全部通过）
- 已完成租用服务器环境重建与版本固定（无卡模式验证通过）
- 已完成 smoke 训练脚本升级：优先 `Qwen3-4B`，兼容回退 `Qwen2.5-3B-Instruct`
- 已新增正式训练入口：
  - `configs/lora_sft_qwen_v1_full.yaml`
  - `scripts/run_train_full.sh`

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
