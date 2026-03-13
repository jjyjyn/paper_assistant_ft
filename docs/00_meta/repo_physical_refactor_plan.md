# 仓库物理层重构方案

这份文档讨论的不是“怎么读仓库”，而是“哪些文件未来值得真的迁移、哪些路径该固定、哪些名字该统一”。

当前原则：

- 先出方案，再分批执行
- 先做不破坏脚本的重构，再做路径迁移
- 每一批迁移都必须保证训练与评测入口仍然可用

## 0. 当前执行状态

截至 `2026-03-13`：

- 第一批 `docs/` 物理重构已完成
  - `docs/README_docs.md` -> `docs/README.md`
  - 总控文档迁入 `docs/00_meta/`
  - handoff 文档迁入 `docs/00_meta/handoffs/`
  - `interview_notes.md` 迁入 `docs/03_interview/interview_notes_quick.md`
- 第二批 `scripts/` 物理重构已完成
  - 真实实现迁入 `scripts/data/ train/ eval/ server/`
  - 根目录旧脚本入口保留为兼容 wrapper
- 当前下一批应聚焦：
  - `configs/` 分层
  - `data/processed/` 是否值得物理拆分

## 1. 当前结构的主要问题

### 1.1 `docs/` 根目录问题已完成首轮修复

已完成修复：

- `docs/README.md` 成为统一入口
- 总控文档迁入 `docs/00_meta/`
- handoff 迁入 `docs/00_meta/handoffs/`
- 面试快读口径迁入 `docs/03_interview/`

剩余工作：

- 继续清理少量历史文档中的旧口径描述
- 保持所有新文档引用使用新路径

### 1.2 `scripts/` 平铺结构问题已完成首轮修复

已完成修复：

- 新建 `scripts/data/ train/ eval/ server/`
- 真实实现迁入对应子目录
- 根目录旧入口保留为 wrapper

剩余工作：

- 在 docs 中逐步把推荐命令切到新路径
- 等一段兼容期后，再决定是否移除旧 wrapper

### 1.3 `configs/` 语义还不够分层

当前 `configs/` 里数据配置和训练配置平铺在一起。

问题：

- 规模再增大后，不容易区分“dataset config”和“train config”
- 文件名里历史版本和当前版本混排

### 1.4 `data/processed/` 可读导出和训练 JSONL 混放

当前 `data/processed/` 同时放：

- 训练用 `.jsonl`
- 人读用 `_readable.json`
- 人读用 `_readable.md`

问题：

- 一个 split 会出现 3 份并列文件
- 机器输入和人工检查产物没有物理隔离

### 1.5 `outputs/` 当前是“逻辑清楚，物理上仍然粗放”

目前 `outputs/evals/` 可用，但没有进一步区分：

- 临时评测
- 需要长期保留的关键评测

这不是当前最高优先级，但后面仍有优化空间。

## 2. 重构目标

目标不是“为了好看而重构”，而是让仓库做到：

1. 新人第一次进来能快速定位入口
2. 每类文件放在最符合职责的目录
3. 脚本路径有清晰命名空间
4. 配置、数据、结果三类资产边界更明确
5. 重构过程不打断当前训练/评测闭环

## 3. 建议目标结构

```text
paper_assistant_ft/
├─ README.md
├─ .gitignore
├─ configs/
│  ├─ README.md
│  ├─ datasets/
│  └─ train/
├─ data/
│  ├─ README.md
│  ├─ raw/
│  ├─ processed/
│  │  ├─ jsonl/
│  │  └─ readable/
│  └─ external_eval/
│     ├─ raw/
│     └─ processed/
│        ├─ jsonl/
│        └─ readable/
├─ docs/
│  ├─ README.md
│  ├─ 00_meta/
│  ├─ 01_data/
│  ├─ 02_training/
│  └─ 03_interview/
├─ logs/
├─ outputs/
│  ├─ README.md
│  └─ evals/
└─ scripts/
   ├─ README.md
   ├─ data/
   ├─ train/
   ├─ eval/
   └─ server/
```

## 4. 逐目录迁移建议

### 4.1 `docs/` 重构建议

这是最值得优先做、同时风险最低的一层。

#### 建议迁移

- `docs/README_docs.md` -> `docs/README.md`
- `docs/project_plan.md` -> `docs/00_meta/project_plan.md`
- `docs/progress_log.md` -> `docs/00_meta/progress_log.md`
- `docs/repo_structure_guide.md` -> `docs/00_meta/repo_structure_guide.md`
- `docs/chat_migration_handoff_2026-03-11.md` -> `docs/00_meta/handoffs/chat_migration_handoff_2026-03-11.md`
- `docs/chat_migration_handoff_2026-03-12.md` -> `docs/00_meta/handoffs/chat_migration_handoff_2026-03-12.md`
- `docs/interview_notes.md` -> `docs/03_interview/interview_notes_quick.md`

#### 原因

- 总控层集中到 `00_meta/`
- 面试口径统一收口到 `03_interview/`
- `docs/README.md` 更符合通用习惯

#### 风险

- Markdown 链接需要批量更新
- 现有 handoff 路径在旧对话里被引用过，迁移时要保留说明

### 4.2 `scripts/` 重构建议

这是第二优先级，但必须分批做，因为它会影响执行路径。

#### 建议迁移

- `scripts/build_dataset_v1.py` -> `scripts/data/build_dataset_v1.py`
- `scripts/build_external_eval_v1.py` -> `scripts/data/build_external_eval_v1.py`
- `scripts/check_dataset_v1.py` -> `scripts/data/check_dataset_v1.py`
- `scripts/check_external_eval_v1.py` -> `scripts/data/check_external_eval_v1.py`
- `scripts/export_dataset_readable.py` -> `scripts/data/export_dataset_readable.py`
- `scripts/run_train_smoke.sh` -> `scripts/train/run_train_smoke.sh`
- `scripts/run_train_full.sh` -> `scripts/train/run_train_full.sh`
- `scripts/eval_lora_model.py` -> `scripts/eval/eval_lora_model.py`
- `scripts/run_eval_v1.sh` -> `scripts/eval/run_eval_v1.sh`
- `scripts/server_day1_init.sh` -> `scripts/server/server_day1_init.sh`
- `scripts/server_rental_init.sh` -> `scripts/server/server_rental_init.sh`
- `scripts/download_qwen3_modelscope.sh` -> `scripts/server/download_qwen3_modelscope.sh`
- `scripts/sync_to_server.ps1` -> `scripts/server/sync_to_server.ps1`

#### 原因

- 路径语义清晰
- 训练、评测、数据、服务器脚本不再混放
- 后续脚本数量增加时仍可维护

#### 风险

- shell 脚本内部引用路径要改
- README、docs、服务器执行命令都要同步
- 必须先保留旧路径兼容壳一段时间

#### 迁移策略

先移动，再在旧位置留一个轻量 wrapper，过渡 1 个阶段后再删。

### 4.3 `configs/` 重构建议

#### 建议迁移

- `configs/dataset_paper_assistant_v1.yaml` -> `configs/datasets/paper_assistant_v1.yaml`
- `configs/lora_sft_qwen25_3b_v1.yaml` -> `configs/train/lora_sft_qwen25_3b_v1.yaml`
- `configs/lora_sft_qwen_v1_full.yaml` -> `configs/train/lora_sft_qwen_v1_full.yaml`

#### 原因

- 数据配置和训练配置分层
- 文件名可以更短、更稳定

#### 风险

- 训练脚本和文档中的配置路径都要改

### 4.4 `data/` 重构建议

#### 建议迁移

- `data/processed/train_v1.jsonl` -> `data/processed/jsonl/train_v1.jsonl`
- `data/processed/val_v1.jsonl` -> `data/processed/jsonl/val_v1.jsonl`
- `data/processed/test_v1.jsonl` -> `data/processed/jsonl/test_v1.jsonl`
- `data/processed/train_v1_readable.json` -> `data/processed/readable/train_v1_readable.json`
- `data/processed/train_v1_readable.md` -> `data/processed/readable/train_v1_readable.md`
- `data/processed/val_v1_readable.json` -> `data/processed/readable/val_v1_readable.json`
- `data/processed/val_v1_readable.md` -> `data/processed/readable/val_v1_readable.md`
- `data/processed/test_v1_readable.json` -> `data/processed/readable/test_v1_readable.json`
- `data/processed/test_v1_readable.md` -> `data/processed/readable/test_v1_readable.md`

external eval 同理：

- `data/external_eval/processed/external_eval_v1.jsonl` -> `data/external_eval/processed/jsonl/external_eval_v1.jsonl`
- `data/external_eval/processed/external_eval_v1_readable.json` -> `data/external_eval/processed/readable/external_eval_v1_readable.json`
- `data/external_eval/processed/external_eval_v1_readable.md` -> `data/external_eval/processed/readable/external_eval_v1_readable.md`

#### 原因

- 机器输入和人工检查文件彻底分开
- 同目录可读性更高

#### 风险

- 构建脚本、检查脚本、文档路径都要同步

### 4.5 `outputs/` 重构建议

当前不建议立刻做物理迁移，只建议先约定命名。

#### 建议命名约定

- 正常评测：`qwen_lora_v1_full_<timestamp>`
- no-think 评测：`qwen_lora_v1_full_<timestamp>_nothink`
- 若未来有 v2：`qwen_lora_v2_full_<timestamp>`

#### 可选后续方案

如果以后评测非常多，再考虑：

- `outputs/evals/tracked/`
- `outputs/evals/tmp/`

但这不是当前最高优先级。

## 5. 执行优先级

### 第一批：低风险，已完成

1. `docs/README_docs.md` 改为 `docs/README.md`
2. 新建 `docs/00_meta/`
3. 把总控文档迁进去
4. 把 `interview_notes.md` 收口到 `docs/03_interview/`
5. 全量更新 Markdown 链接

这一批已经完成，并且没有破坏训练与评测入口。

### 第二批：中风险，已完成

1. 新建 `scripts/data/ train/ eval/ server/`
2. 用 `git mv` 迁移脚本
3. 在旧路径保留 wrapper
4. 用新旧两套入口验证 `check_dataset_v1.py`
5. 更新 `scripts/README.md`

### 第三批：中风险，整理配置

1. 新建 `configs/datasets/` 和 `configs/train/`
2. 迁移配置
3. 更新训练脚本和文档路径

### 第四批：中风险，整理数据目录

1. 新建 `jsonl/` 和 `readable/`
2. 更新构建脚本输出路径
3. 更新检查脚本读取路径
4. 更新 docs 引用

## 6. 当前不建议立即动的部分

### 6.1 `outputs/evals/` 历史结果目录

理由：

- 已经被多份 docs 和复盘记录引用
- 改路径收益不大，改坏引用的代价较高

### 6.2 `data/raw/paper_cases_v1.json`

理由：

- 它已经是当前主原始资产入口
- 不值得为了“更规范的命名”去破坏现有稳定路径

### 6.3 训练与评测 run 名称

理由：

- 当前命名已经足够表达模型、版本、时间戳、模式
- 不应在这个阶段引入额外命名变体

## 7. 推荐的下一步真实执行方案

从当前状态继续做“物理重构”，建议严格按这个顺序：

1. 先做 `configs/` 重构
2. 再评估 `data/processed/` 是否值得物理迁移

## 8. 验收标准

完成任意一批迁移后，都必须满足：

1. `README.md` 和 `docs/README.md` 无断链
2. `python scripts/check_dataset_v1.py` 或其兼容入口仍能运行
3. `bash scripts/run_eval_v1.sh` 或其兼容入口仍能运行
4. 历史文档里的关键入口有迁移说明
5. 新人仍能在 5 分钟内找到数据、脚本、结果、复盘文档

## 9. 一句话结论

当前最值得真的动手的不是 `outputs/`，也不是 `data/`，而是：

1. `docs/` 根目录分层
2. `scripts/` 命名空间拆分
3. `configs/` 语义分层

这三件事做完，仓库会从“能用但越来越满”变成“结构稳定、后续能继续长”的状态。
