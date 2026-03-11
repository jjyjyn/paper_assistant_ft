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
- 已完成 smoke 训练脚本升级：优先 `Qwen3-4B-Instruct`，兼容回退 `Qwen2.5-3B-Instruct`
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
  - `export MODEL_PATH=~/models/Qwen/Qwen3-4B-Instruct`
  - `bash scripts/run_train_smoke.sh`
- 验收：
  - 训练完整启动并结束
  - `outputs/` 下出现日志和 checkpoint
  - 无 OOM/路径错误/字段错误

4. 正式训练（smoke 通过后）
- 执行：
  - `export MODEL_PATH=~/models/Qwen/Qwen3-4B-Instruct`
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
