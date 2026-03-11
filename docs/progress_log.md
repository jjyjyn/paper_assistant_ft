# 过程记录（Progress Log）

## 2026-03-10（Day 1）

### 完成事项

- 搭建项目文档体系和脚本骨架
- 打通本地与服务器同步链路
- 完成基础环境安装与依赖排查
- 识别学校服务器 GPU 节点稳定性风险

### 结论

- Day 1 目标达成
- 训练执行平台改为“优先租用 4090”

---

## 2026-03-11（Day 2）

### 今日目标

- 完成数据集第一版（schema + 样本 + 构建 + 校验）
- 为明天训练准备可直接执行的配置和脚本

### 今日新增文件

- `docs/dataset_schema.md`
- `data/raw/paper_cases_v1.json`
- `data/raw/seed_samples.md`
- `data/dataset_info.json`
- `data/processed/train_v1.jsonl`
- `data/processed/val_v1.jsonl`
- `scripts/build_dataset_v1.py`
- `scripts/check_dataset_v1.py`
- `configs/dataset_paper_assistant_v1.yaml`
- `configs/lora_sft_qwen25_3b_v1.yaml`
- `scripts/run_train_smoke.sh`

### 今日执行命令（本地）

```bash
python scripts/build_dataset_v1.py
python scripts/check_dataset_v1.py
```

### 结果

- 构建样本总数：80
- 训练集：72
- 验证集：8
- 四类任务分布：
  - train: 18/18/18/18
  - val: 2/2/2/2
- 数据校验：`Dataset check passed.`

### 关键说明

- v1 采用“结构化案例 + 模板扩展”方案，优先保证启动速度和任务覆盖。
- 后续会迭代加入人工高难样本，提高泛化质量。

### 下一步

1. 租用 4090 服务器并初始化环境
2. 执行 smoke 训练（50-100 step）
3. 根据显存/速度反馈调整训练超参
