# scripts 目录说明

`scripts/` 只放“动作脚本”。你要构建数据、检查数据、训练、评测、直接问模型、同步服务器，入口基本都在这里。

## 0. 当前目录结构

```text
scripts/
├─ README.md
├─ data/
├─ train/
├─ eval/
├─ chat/
├─ server/
└─ 兼容 wrapper（保留旧路径）
```

说明：

- `scripts/data/ train/ eval/ chat/ server/` 是当前真实实现所在目录
- `scripts/*.py`、`scripts/*.sh`、`scripts/sync_to_server.ps1` 旧入口仍保留为兼容 wrapper
- 所以旧命令暂时还能继续用，但新文档和后续开发应优先使用子目录路径

## 1. 按功能分类

### 1.1 数据构建与导出：`scripts/data/`

- `build_dataset_v1.py`
  - 从 `data/raw/paper_cases_v1.json` 构建 train/val/test
- `build_external_eval_v1.py`
  - 构建 external eval 数据集
- `export_dataset_readable.py`
  - 导出便于人工阅读的 JSON / Markdown

### 1.2 数据校验：`scripts/data/`

- `check_dataset_v1.py`
  - 校验 train/val/test 行数、case 分布、任务分布
- `check_external_eval_v1.py`
  - 校验 external eval 行数、任务分布、overlap

### 1.3 训练：`scripts/train/`

- `run_train_smoke.sh`
  - 冒烟训练，先确认配置和流程能跑通
- `run_train_full.sh`
  - 正式 full 训练

### 1.4 评测：`scripts/eval/`

- `eval_lora_model.py`
  - 单次评测主逻辑，负责生成、清洗、打分、产出 summary/report/predictions
- `run_eval_v1.sh`
  - 统一评测入口，串起检查脚本和评测脚本

当前评测脚本已支持：

- `--disable-thinking`
- `--run-tag`
- `no-think` 目录后缀
- fail-fast 防误跑

### 1.5 直接问模型：`scripts/chat/`

- `chat_lora_model.py`
  - 交互式加载 `Qwen base model + LoRA adapter`
  - 支持单轮 `--prompt`
  - 支持多轮会话
  - 支持 `--disable-thinking`
  - 支持 `--show-raw` / `--show-meta`

推荐用法：

```bash
python scripts/chat/chat_lora_model.py \
  --base-model "$MODEL_PATH" \
  --adapter-path outputs/qwen_lora_v1_full \
  --disable-thinking
```

单轮问答：

```bash
python scripts/chat/chat_lora_model.py \
  --base-model "$MODEL_PATH" \
  --adapter-path outputs/qwen_lora_v1_full \
  --disable-thinking \
  --prompt "请比较这篇论文与 baseline 的核心差异。"
```

### 1.6 服务端与同步：`scripts/server/`

- `server_day1_init.sh`
  - 服务器首次初始化
- `server_rental_init.sh`
  - 租服后环境初始化
- `download_qwen3_modelscope.sh`
  - 下载模型
- `sync_to_server.ps1`
  - 本地到服务器的同步辅助脚本

## 2. 最常用执行顺序

### 2.1 数据阶段

1. `python scripts/build_dataset_v1.py`
2. `python scripts/check_dataset_v1.py`
3. `python scripts/build_external_eval_v1.py`
4. `python scripts/check_external_eval_v1.py`

推荐新路径：

1. `python scripts/data/build_dataset_v1.py`
2. `python scripts/data/check_dataset_v1.py`
3. `python scripts/data/build_external_eval_v1.py`
4. `python scripts/data/check_external_eval_v1.py`

### 2.2 训练阶段

1. `bash scripts/run_train_smoke.sh`
2. `bash scripts/run_train_full.sh`

推荐新路径：

1. `bash scripts/train/run_train_smoke.sh`
2. `bash scripts/train/run_train_full.sh`

### 2.3 评测阶段

1. `bash scripts/run_eval_v1.sh`
2. 看 `outputs/evals/<run_name>/`

推荐新路径：

1. `bash scripts/eval/run_eval_v1.sh`
2. 看 `outputs/evals/<run_name>/`

### 2.4 直接问模型

1. `python scripts/chat_lora_model.py --help`
2. 交互式：`python scripts/chat/chat_lora_model.py --base-model ... --adapter-path ... --disable-thinking`
3. 单轮：`python scripts/chat/chat_lora_model.py --base-model ... --adapter-path ... --disable-thinking --prompt "..."`

## 3. 读脚本的建议顺序

1. `eval/run_eval_v1.sh`
2. `eval/eval_lora_model.py`
3. `chat/chat_lora_model.py`
4. `train/run_train_smoke.sh`
5. `train/run_train_full.sh`
6. `data/build_dataset_v1.py`
7. `data/check_dataset_v1.py`

## 4. 维护原则

- 同类动作优先复用已有脚本，不临时造新入口
- 新增脚本优先放入对应子目录，不再继续平铺到 `scripts/` 根目录
- 大改脚本时，同步更新 `docs/00_meta/progress_log.md`
- 如果评测口径变了，要同时更新 `docs/00_meta/project_plan.md` 和相关面试文档
