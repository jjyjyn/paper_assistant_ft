# 项目计划（Project Plan）

## 当前阶段

- 阶段 1：环境与仓库跑通（已完成）
- 阶段 2：数据集第一版制作（进行中）

## 阶段目标与完成标准

1. 环境与仓库跑通（Done）
- 标准：
  - 本地与服务器代码同步可用
  - 训练环境可创建，核心依赖可安装
  - `llamafactory-cli` 可运行
- 状态：
  - 已完成
  - 备注：当前学校服务器节点 GPU 存在稳定性风险

2. 数据集第一版制作（In Progress）
- 标准：
  - 四类任务统一 schema 定稿
  - 产出可训练 `train_v1.jsonl` 与 `val_v1.jsonl`
  - 完成抽样质检与修正
- 目标规模：
  - v0：80-150 条高质量样本

3. LoRA 微调训练（Pending）
- 标准：
  - 首次训练跑通并产出 checkpoint
  - 超参与日志可追溯
  - 至少完成 1 轮调参与对比

4. 评测、案例整理、简历包装（Pending）
- 标准：
  - 形成定量对比与案例分析
  - 形成可讲述的项目闭环故事线

## Day 2 详细执行清单（明天）

1. 定义数据 schema
- 文件：
  - `docs/dataset_schema.md`
  - `configs/dataset_paper_assistant_v1.yaml`
- 完成标准：
  - 四类任务统一为 `instruction/input/output` 结构

2. 生成首版样本
- 文件：
  - `data/raw/seed_samples.md`
  - `data/processed/train_v1.jsonl`
  - `data/processed/val_v1.jsonl`
- 数量目标：
  - 每类任务 20-40 条，合计 80-150 条

3. 增加数据处理脚本
- 文件：
  - `scripts/build_dataset_v1.py`
  - `scripts/check_dataset_v1.py`
- 功能：
  - 自动转换、去重、字段校验、长度统计

4. 增加训练配置草案（先不启动长训）
- 文件：
  - `configs/lora_sft_qwen25_3b_v1.yaml`
  - `scripts/run_train_smoke.sh`
- 目标：
  - 先做 50-100 step 冒烟

## 风险与应对

- 风险 1：学校服务器 GPU 节点不稳定
  - 应对：先推进数据与配置，训练改为“健康检查通过后启动”

- 风险 2：外网访问波动（HF/GitHub）
  - 应对：优先本地模型路径 + ModelScope + 手动同步

- 风险 3：训练窗口受限
  - 应对：准备租用服务器的平迁方案，详见：
  - `docs/rental_server_guide.md`

## 时间安排（滚动）

- Day 1：环境、同步、记录体系（已完成）
- Day 2：数据 schema + 样本模板 + 数据构建脚本
- Day 3：首版数据集定稿 + 首次训练
- Day 4：调参与对比实验
- Day 5：first usable version
- Day 6-7：评测报告 + 简历/面试材料（resume-ready）
