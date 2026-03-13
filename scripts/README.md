# scripts 目录说明

`scripts/` 只放“动作脚本”。你要构建数据、检查数据、训练、评测、同步服务器，入口基本都在这里。

## 1. 按功能分类

### 1.1 数据构建与导出

- `build_dataset_v1.py`
  - 从 `data/raw/paper_cases_v1.json` 构建 train/val/test
- `build_external_eval_v1.py`
  - 构建 external eval 数据集
- `export_dataset_readable.py`
  - 导出便于人工阅读的 JSON / Markdown

### 1.2 数据校验

- `check_dataset_v1.py`
  - 校验 train/val/test 行数、case 分布、任务分布
- `check_external_eval_v1.py`
  - 校验 external eval 行数、任务分布、overlap

### 1.3 训练

- `run_train_smoke.sh`
  - 冒烟训练，先确认配置和流程能跑通
- `run_train_full.sh`
  - 正式 full 训练

### 1.4 评测

- `eval_lora_model.py`
  - 单次评测主逻辑，负责生成、清洗、打分、产出 summary/report/predictions
- `run_eval_v1.sh`
  - 统一评测入口，串起检查脚本和评测脚本

当前评测脚本已支持：

- `--disable-thinking`
- `--run-tag`
- `no-think` 目录后缀
- fail-fast 防误跑

### 1.5 服务器与同步

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

### 2.2 训练阶段

1. `bash scripts/run_train_smoke.sh`
2. `bash scripts/run_train_full.sh`

### 2.3 评测阶段

1. `bash scripts/run_eval_v1.sh`
2. 看 `outputs/evals/<run_name>/`

## 3. 读脚本的建议顺序

1. `run_eval_v1.sh`
2. `eval_lora_model.py`
3. `run_train_smoke.sh`
4. `run_train_full.sh`
5. `build_dataset_v1.py`
6. `check_dataset_v1.py`

## 4. 维护原则

- 同类动作优先复用已有脚本，不临时造新入口
- 大改脚本时，同步更新 `docs/progress_log.md`
- 如果评测口径变了，要同时更新 `docs/project_plan.md` 和相关面试文档
