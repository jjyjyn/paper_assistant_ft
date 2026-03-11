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

---

## 2026-03-11（文档增强）

### 触发原因

- 用户希望获得“可亲手操作、可面试复述”的完整闭环，而不是简略说明。

### 新增内容

- `docs/llm_finetune_end2end_playbook.md`
- `docs/day2_data_hands_on_lab.md`
- `docs/interview_notes_categorized.md`
- `docs/dataset_reading_guide.md`
- `docs/README_docs.md` 导航增强

### 目标

- 把“我会执行命令”升级为“我能讲清楚每一步为什么、怎么做、结果是什么”。

### 补充动作（数据准备分支）

- 新增 `docs/data_preparation/` 目录，作为数据准备专题分支。
- 新增 `case_004 -> v1_0015` 一一映射文档，解释 case 字段如何进入训练样本。

## 2026-03-11（case 测试记录补充）
- 新增 docs/data_preparation/case_test_log.md。
- 已记录 case_004 的修改内容、重建命令、以及对 v1_0013~v1_0016 的映射影响。
- 后续每次 case 修改都按模板追加，不覆盖历史记录。

## 2026-03-11（case_005 映射验证）
- 完成 case_005 的手工改写，并重建数据集（build/check/export）。
- 确认映射结果：source_case_id=case_005 共 4 条样本（train 3 条 + val 1 条）。
- 样本 ID：v1_0017, v1_0018, v1_0019, v1_0020。
- 结论：单个 raw case 改动可稳定传播到四类任务样本，数据闭环验证通过。

## 2026-03-11（阶段2-第3步：test集 + 防泄漏 + 数据定版）
- 已将数据切分策略从样本级改为 case 级（按 source_case_id 切分）。
- 新增 test 集产物：data/processed/test_v1.jsonl（及 readable 导出）。
- 切分结果：train/val/test = 64/8/8（对应 case 数 16/2/2）。
- 新增检查：三组间 id 不重叠、source_case_id 不重叠，防止数据泄漏。
- 运行结果：python scripts/check_dataset_v1.py -> Dataset check passed.

## 2026-03-11（外部评测集闭环补齐）
- 新增外部评测原始集：data/external_eval/raw/external_eval_cases_v1.json（8 cases）。
- 新增脚本：build_external_eval_v1.py / check_external_eval_v1.py。
- 产物：external_eval_v1.jsonl + readable.json + readable.md（共32样本）。
- 校验结果：External eval check passed（含与主训练case标题/ID防重合）。

## 2026-03-11（数据分集口径确认）
- 已确认当前口径：1 套 train + 1 套 val + 2 套 test（test_v1 + external_eval_v1）。
- 目的：同时覆盖同分布评测与外部泛化评测，减少单一测试结论偏差。

## 2026-03-11 Chat Migration Prep
- Added migration handoff document: `docs/chat_migration_handoff_2026-03-11.md`.
- Document includes: fixed constraints, current dataset/eval status, next-step execution order, and paste-ready prompt block for starting a new Codex chat.
- Goal: avoid token-limit context loss and continue directly from Phase 2 -> Phase 3 (training).

## 2026-03-11（新会话迁移后：Phase 3 训练前准备）

### 本轮目标

- 在新对话窗口无上下文丢失地接续阶段 3。
- 完成训练前可执行性复核，并把训练入口补齐到“一条 smoke + 一条 full”。

### 本轮执行命令（本地）

```bash
python scripts/build_dataset_v1.py
python scripts/check_dataset_v1.py
python scripts/build_external_eval_v1.py
python scripts/check_external_eval_v1.py
```

### 本轮结果

- 主数据构建与校验通过：`train/val/test = 64/8/8`。
- 外部评测构建与校验通过：`external_eval_v1 = 32`。
- 数据链路状态：可复现、可训练、可评测。

### 本轮代码/配置更新

- 更新：`scripts/run_train_smoke.sh`
  - 模型自动探测顺序改为优先 Qwen3-4B，回退 Qwen2.5-3B。
  - 增加 `BASE_CONFIG` 可覆盖参数，便于复用 smoke 脚本。
- 新增：`configs/lora_sft_qwen_v1_full.yaml`
  - 正式训练配置入口（默认 3 epoch，保留输出目录）。
- 新增：`scripts/run_train_full.sh`
  - 正式训练启动脚本，与 smoke 保持同一模型探测逻辑。

### 本轮文档同步

- 更新：`docs/project_plan.md`（Phase 3 状态与执行清单对齐）。
- 更新：`docs/README_docs.md`（加入 Day3 手册导航）。
- 更新：`docs/llm_finetune_end2end_playbook.md`（补 full 训练入口）。
- 更新：`docs/interview_notes.md`（新增 Phase 3 高频追问）。
- 新增：`docs/day3_training_hands_on_lab.md`（按“原理+操作+验收+常见坑”沉淀）。

### 关键结论（阶段口径）

1. 当前已从“训练待启动”推进到“训练执行准备完成”。
2. 训练执行顺序固定为：`server init -> data check -> smoke -> full`。
3. 文档需要持续记录：每次训练的配置、日志路径、loss 变化、失败原因与修复。

## 2026-03-11（训练前文档完备性审计与修正）

### 审计目标

- 检查“训练前准备”是否已可对外稳定复述（保研/面试场景）。
- 检查 docs 是否存在旧口径（72/8、90/10）导致前后冲突。

### 发现与修正

1. `docs/dataset_schema.md`
- 旧口径：90/10 train/val 与 72/8。
- 修正：case-level `64/8/8` + external_eval `32`，并补充防泄漏说明。

2. `docs/day2_data_hands_on_lab.md`
- 旧口径：Step 1 仍写 train 72 / val 8。
- 修正：更新为 train 64 / val 8 / test 8；抽检改为 train/val/test = 6/2/2。

3. `docs/data_cleaning_labeling_guide.md`
- 补充：train/val/test 覆盖要求与 `source_case_id` 防泄漏规则。
- 新增：清洗常见问题与处理（幻觉、模板化、泄漏、外部泛化不足）。

### 结论

- 当前“训练前准备 + 数据准备 + 清洗问题 + 面试追问”四块内容已成体系。
- 剩余工作重心转到：服务器执行 smoke/full，并把真实训练日志继续回填到 docs。

## 2026-03-11（租用服务器环境配置与版本固定）

### 本轮目标

- 在 AutoDL 租用服务器上完成一套可复现的训练环境。
- 不是只“装上能跑”，而是把版本冲突和真实报错归因清楚。

### 环境选择

- 平台：AutoDL
- 配置：北京 B 区 `RTX 4090 24GB`
- 镜像：`Miniconda / conda3 / Python 3.10 / Ubuntu 22.04`
- 执行策略：
  - 无卡模式：装环境、拉代码、跑数据检查
  - GPU 模式：只负责训练

### 实际遇到的问题

1. `tmux` 缺失
- 归因：系统层工具缺失
- 处理：`apt-get install -y tmux`

2. `MODEL_PATH` 指向不存在目录
- 归因：路径层错误
- 处理：先查目录，再设置真实模型路径

3. `huggingface_hub` / `transformers` / `tokenizers` 版本冲突
- 归因：Python 依赖链被错误升级
- 处理：删除旧环境，重建 conda 环境并钉死兼容版本

4. `torchvision::nms does not exist`
- 归因：`torch` 与 `torchvision` 二进制版本不匹配
- 处理：使用同一套 CUDA wheel 重装

### 最终固定版本

- `torch==2.4.1+cu121`
- `torchvision==0.19.1+cu121`
- `transformers==4.52.4`
- `tokenizers==0.21.1`
- `huggingface_hub==0.36.2`
- `llamafactory==0.9.3`

### 验证结果

- 无卡模式版本验证通过
- `check_dataset_v1.py` -> `Dataset check passed.`
- `check_external_eval_v1.py` -> `External eval check passed.`
- 说明：无卡模式下 `cuda: False` 为预期现象，不代表环境失败

### 结论

- 环境配置阶段已从“经验性安装”升级为“有版本基线、有故障归因、有验证输出”的可复现流程。

## 2026-03-11（docs 结构重组与阶段归档）

### 触发原因

- 根目录文档过多，按阶段复盘和按老师追问准备都不方便。
- 仅靠零散文档难以支撑“从数据到训练到面试”的完整叙事。

### 本次重组结果

- 根目录只保留总控文档：
  - `README_docs.md`
  - `project_plan.md`
  - `progress_log.md`
  - `interview_notes.md`
  - `chat_migration_handoff_2026-03-11.md`
- 数据阶段文档归入：`docs/01_data/`
- 训练阶段文档归入：`docs/02_training/`
- 面试阶段文档归入：`docs/03_interview/`

### 本次新增文档

- `docs/02_training/environment_setup_guide.md`
- `docs/03_interview/teacher_question_bank.md`

### 目标

- 让你后面按阶段读，就能把项目完整讲下来。
- 让“老师可能怎么问”与“你该去哪份文档看”形成一一对应关系。

## 2026-03-11（Qwen3 模型命名纠偏与 HF 超时处理）

### 触发原因

- GPU 模式准备开始 `smoke` 时，发现 `Qwen3-4B-Instruct` 本地目录不存在。
- 继续尝试从 Hugging Face 下载时，服务器到 `huggingface.co` 连接超时。

### 关键判断

- 训练环境本身是健康的：`numpy/fsspec/transformers/tokenizers/huggingface_hub` 版本校验通过，`pip check` 无破损依赖。
- 问题分成两层：
  - 模型命名层：Qwen3 官方 4B 路线应对齐为 `Qwen3-4B`
  - 网络层：国内租用服务器访问 Hugging Face 不稳定，下载源需要切换

### 代码与流程修正

- 训练脚本自动探测路径改为优先寻找：
  - `/root/autodl-tmp/models/Qwen/Qwen3-4B`
  - `~/models/Qwen/Qwen3-4B`
- 保留 `Qwen2.5-3B-Instruct` 作为 fallback
- 新增 `scripts/download_qwen3_modelscope.sh`
  - 作用：通过 ModelScope 官方源下载 `Qwen/Qwen3-4B`
  - 目的：绕开 `huggingface.co` 超时
- 修正下载脚本实现：
  - 原写法使用 `conda run -n base python - <<PY`，在实际服务器上未把 heredoc 正常传入 Python
  - 现改为 `conda run -n base python -c ...`，确保脚本会真实执行 `snapshot_download`

### 文档同步

- 将默认模型名从 `Qwen3-4B-Instruct` 更正为 `Qwen3-4B`
- 在训练文档中增加：
  - Hugging Face 超时归因
  - ModelScope 下载方案
  - AutoDL 数据盘优先路径
- 将训练命令中的默认 `MODEL_PATH` 进一步对齐到本次实测下载目录：
  - `/root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B`

## 2026-03-11（ModelScope 模型下载完成与文件级验收）

### 本轮目标

- 在无卡模式下完成 `Qwen3-4B` 预下载，避免占用 GPU 时长做大文件传输。
- 把“模型在不在”从口头判断升级为文件级验收。

### 实际执行

1. 服务器进入无卡模式
- 原因：模型下载主要消耗网络和磁盘，不消耗 GPU 计算。

2. 拉取修正后的仓库代码
- `git pull --ff-only`

3. 通过 ModelScope 下载模型
- 成功信息：
  - `MODEL_PATH=/root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B`
  - `Download model 'Qwen/Qwen3-4B' successfully.`

4. 做文件级验收，而不是只看进度条
- `config.json`：存在
- `tokenizer_config.json`：存在
- `model-00001-of-00003.safetensors`：约 `3.7G`
- `model-00002-of-00003.safetensors`：约 `3.8G`
- `model-00003-of-00003.safetensors`：约 `96M`
- 总目录体积：`7.6G`

### 经验总结

- SSH/VSCode 终端里的下载进度条会出现残影，不能把日志中的 `0%` 刷屏误判为下载失败。
- 对大模型下载，最终判断标准应当是：
  - 有成功日志
  - 返回 shell 提示符
  - 关键文件存在
  - 文件体积合理

### 阶段结论

- 截至 2026-03-11，Phase 3 的训练前准备已经闭环。
- 当前服务器已经达到：
  - environment ready
  - data ready
  - model ready
  - GPU smoke ready

## 2026-03-11（Qwen3 训练初始化失败，升级到 PyTorch 2.6 修复）

### 触发原因

- 切回 GPU 模式后首次执行 `smoke`，数据读取和模型权重加载都正常。
- 在 `Qwen3ForCausalLM` 初始化阶段崩溃，关键报错为：
  - `TypeError: argument of type 'NoneType' is not iterable`

### 关键判断

- 这不是数据问题，也不是模型文件损坏。
- 报错发生在 `transformers` 初始化 `Qwen3` 模型时，属于版本矩阵不兼容。
- 结合官方资料与 LLaMA-Factory issue，定位到：
  - `transformers==4.52.4` 已满足 Qwen3 要求
  - 但 `torch==2.4.1+cu121` 偏低
  - Qwen3 路线应升级到 `torch>=2.5`，更稳妥的是 `torch 2.6`

### 处理过程

1. 决定不在 GPU 模式下装大 wheel
- 原因：升级 `torch/torchvision/torchaudio` 主要消耗网络和磁盘
- 策略：切回无卡模式完成依赖升级，再切回 GPU 跑训练

2. 通过阿里云 PyTorch wheels 镜像安装
- 目标版本：
  - `torch==2.6.0+cu124`
  - `torchvision==0.21.0+cu124`
  - `torchaudio==2.6.0+cu124`

3. 安装后出现新的依赖漂移
- `numpy` 被带到 `2.2.6`
- `fsspec` 被带到 `2026.2.0`
- `pillow` 被带到 `12.1.1`
- 这些版本分别与：
  - `llamafactory`
  - `trl`
  - `datasets`
  - `gradio`
  不兼容

4. 回钉兼容版本
- `numpy==1.26.4`
- `fsspec==2025.3.0`
- `pillow==11.3.0`

### 最终验证

- `torch: 2.6.0+cu124`
- `torchvision: 0.21.0+cu124`
- `torchaudio: 2.6.0+cu124`
- `transformers: 4.52.4`
- `numpy: 1.26.4`
- `fsspec: 2025.3.0`
- `pillow: 11.3.0`
- 无卡模式下 `cuda: False` 为预期现象
- `python -m pip check` -> `No broken requirements found.`

### 结论

- 当前 `paper_ft` 环境已经升级到适配 Qwen3 的 PyTorch 版本线。
- 训练前准备再次通过验证，下一步应切回 GPU 模式重跑 `smoke`。

## 2026-03-11（Qwen3 Smoke 训练真实跑通）

### 触发原因

- 在完成：
  - ModelScope 模型下载
  - PyTorch 2.6 升级
  - `numpy/fsspec/pillow` 回钉
  之后，重新进入 GPU 模式执行 `smoke`

### 实际结果

- `Qwen3-4B` 成功完成一次真实 `smoke` 训练
- 训练末尾输出：
  - `Training completed.`
  - `Smoke training finished.`

### 关键指标

- `train_runtime: 24.392`
- `train_loss: 2.178870439529419`
- `train_samples_per_second: 2.624`
- `train_steps_per_second: 0.328`
- `epoch: 1.0`

### 产物

- 输出目录：
  - `outputs/qwen25_3b_lora_v1_smoke/`
- 检查点：
  - `outputs/qwen25_3b_lora_v1_smoke/checkpoint-8/`
- 同时保存了：
  - `chat_template.jinja`
  - `tokenizer_config.json`
  - `special_tokens_map.json`

### 如何解释这次 smoke 成功

- 这次成功证明的不只是“脚本能运行”
- 更准确地说，它证明了：
  - Qwen3 模型路径正确
  - tokenizer/template 正常
  - 数据集 schema 正常
  - LoRA 训练链路正常
  - 当前 GPU / torch / transformers / LLaMA-Factory 版本矩阵可用

### 仍需注意的点

- `output_dir` 名称还是 `qwen25_3b_lora_v1_smoke`
- 这是 smoke 配置文件沿用旧命名造成的历史遗留
- 本次训练实际模型仍然是 `Qwen3-4B`，因为脚本在运行前已动态覆写 `model_name_or_path`

### 阶段结论

- 截至 2026-03-11，Phase 3 已从“训练前准备完成”推进到“smoke 已通过”。
- 下一步应执行：
  - `bash scripts/run_train_full.sh`
  - 并同步记录 full 训练日志、loss、checkpoint 和评测计划

## 2026-03-11（Qwen3 Full 训练真实跑通）

### 触发原因

- 在 `smoke` 已通过的前提下，进入正式训练阶段。
- 当前目标不再是验证链路能否启动，而是拿到：
  - 正式输出目录
  - 正式 loss 曲线
  - 正式训练日志
  - 可用于后续评测和案例分析的主实验产物

### 实际结果

- `Qwen3-4B` 成功完成一次真实 `full` 训练。
- 训练末尾输出：
  - `Full training finished.`
- 同时写出：
  - `outputs/qwen_lora_v1_full/`
  - `outputs/qwen_lora_v1_full/training_loss.png`

### 关键指标

- `train_runtime: 65.0085`
- `train_loss: 1.6736689408620198`
- `train_samples_per_second: 2.953`
- `train_steps_per_second: 0.369`
- `epoch: 3.0`

### 训练过程中的代表性 loss

- `epoch: 1.25` 时：
  - `loss: 2.1071`
  - `grad_norm: 0.9666892290115356`
  - `learning_rate: 8.117449009293668e-05`
- `epoch: 2.5` 时：
  - `loss: 1.4035`
  - `grad_norm: 0.8593475222587585`
  - `learning_rate: 1.3347406408508695e-05`

### 如何解释这些数字

- 这次 `full` 的时间很短，不是因为训练没有真正发生，而是因为当前 v1 数据规模较小。
- `train_loss = 1.6737` 是整轮训练的聚合结果，不等于最后一次打印的单步 loss。
- 从 `2.1071 -> 1.4035` 的中间过程可以看到，训练过程中 loss 总体在下降。
- 因此当前阶段最重要的结论不是“模型已经最优”，而是：
  - 正式训练配置已经真实跑通
  - 正式训练产物已经成功落盘
  - 后续可以进入评测与失败案例复盘阶段

### 非阻塞 warning

- 日志中出现：
  - `No metric eval_loss to plot.`
  - `No metric eval_accuracy to plot.`
- 这不代表训练失败。
- 更准确地说，它说明当前这轮 `full` 主要完成了训练与训练曲线落盘，还没有在同一轮流程中产出对应的 eval 曲线。
- 因此下一步应补：
  - in-domain test 评测
  - external_eval 评测
  - 成功样例/失败样例分析

### 阶段结论

- 截至 2026-03-11，Phase 3 已从“smoke 已通过”推进到“full 已完成”。
- 当前项目已经具备：
  - 数据准备闭环
  - 环境搭建闭环
  - 模型获取闭环
  - smoke 训练闭环
  - full 训练闭环
- 下一步优先级应转为：
  - 评测脚本与结果汇总
  - external_eval 表现分析
  - 失败样例归因
  - 面向老师汇报的话术收敛
