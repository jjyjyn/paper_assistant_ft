# 项目计划（Project Plan）

## 当前阶段

- 阶段 1：环境与仓库跑通（已完成）
- 阶段 2：数据集第一版制作（已完成 v1 初版）
- 阶段 3：LoRA 微调训练（待启动）

## 阶段状态

1. 环境与仓库跑通（Done）
- 本地/服务器同步链路已通
- LLaMA-Factory 可运行
- 已准备租用服务器执行方案

2. 数据集第一版（Done - v1）
- 已完成四类任务统一 schema
- 已完成结构化案例库 + 自动扩展脚本
- 已产出并校验：
  - `data/processed/train_v1.jsonl`（72）
  - `data/processed/val_v1.jsonl`（8）
- 校验结果：四类任务在 train/val 全覆盖

3. LoRA 微调训练（Next）
- 在新租 4090 节点执行 smoke run（50-100 step）
- 通过后执行正式训练

## 明日执行清单（训练日）

1. 服务器准备
- 租用 `RTX 4090 24GB`
- 拉取仓库并执行 `scripts/server_rental_init.sh`
- 验证：`torch.cuda.is_available()` 和 `llamafactory-cli version`

2. 数据准备
- 执行：
  - `python scripts/build_dataset_v1.py`
  - `python scripts/check_dataset_v1.py`

3. 冒烟训练
- 执行：`bash scripts/run_train_smoke.sh`
- 完成标准：
  - 成功启动并完成一个短训练
  - 生成日志和输出目录

4. 正式训练准备
- 根据 smoke 显存和速度调整：
  - `per_device_train_batch_size`
  - `gradient_accumulation_steps`
  - `cutoff_len`

## 风险与应对

- 风险：学校服务器节点 GPU 不稳定
  - 应对：默认在租用 4090 上训练，学校节点只保留为备份

- 风险：训练时间超预算
  - 应对：先小步数验证，再开长训练；中途基于 loss 曲线早停

## 阶段2里程碑更新（2026-03-11）
- 数据集已升级为 train/val/test 三分集。
- 已启用 case-level split，避免同一论文案例跨集合泄漏。
- 完成标准：
  1) build/check/export 全部可执行；
  2) check 脚本能自动拦截 id/source_case_id 泄漏；
  3) 训练前数据版本已固定可复现。
