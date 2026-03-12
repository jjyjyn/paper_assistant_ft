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

## 2026-03-11（补充正式评测脚本与评测口径）

### 触发原因

- `full` 已完成，项目下一阶段不应继续停留在“训练成功”层面。
- 当前真正需要解决的是：
  - 如何稳定复现评测
  - 如何同时报告 in-domain 与 external 结果
  - 如何把生成式输出变成可读、可汇报、可抽检的评测材料

### 新增内容

- 新增脚本：
  - `scripts/eval_lora_model.py`
  - `scripts/run_eval_v1.sh`

### 设计思路

- 不依赖额外服务，直接加载：
  - base model：`Qwen3-4B`
  - adapter：`outputs/qwen_lora_v1_full`
- 逐条读取 JSONL 评测集样本，按训练时同类 `instruction + input` 形式构造用户提示。
- 使用 `tokenizer.apply_chat_template(...)` 构造 Qwen 对话输入，保证推理格式尽量贴近训练格式。
- 每条样本写出：
  - 原始 instruction
  - 原始 input
  - reference
  - prediction
  - `exact_match`
  - `char_f1`

### 为什么选这套指标

- 当前任务是生成式、结构化、多句输出，不适合只用单一分类准确率理解。
- 因此先采用两层口径：
  - `exact_match_rate`：判断模型是否能稳定复现标准答案
  - `avg_char_f1`：作为中文生成任务的粗粒度重合度参考
- 同时输出 `report.md`，方便做人工抽检。
- 这意味着评测不是“只看一个数”，而是：
  - 自动指标做快筛
  - 可读报告做质检

### 运行方式

- 服务器执行：
  - `bash scripts/run_eval_v1.sh`
- 输出目录形如：
  - `outputs/evals/qwen_lora_v1_full_<timestamp>/`
- 主要文件：
  - `test_v1_predictions.jsonl`
  - `test_v1_summary.json`
  - `test_v1_report.md`
  - `external_eval_v1_predictions.jsonl`
  - `external_eval_v1_summary.json`
  - `external_eval_v1_report.md`

### 阶段结论

- 截至 2026-03-11，项目已经具备从训练到评测的最小闭环执行能力。
- 当前下一步不是继续改训练脚本，而是：
  - 跑出 test/external 两组评测结果
  - 选取高分样例与低分样例
  - 做失败归因与汇报材料沉淀

## 2026-03-12（首轮评测完成，定位到 `<think>` 泄露）

### 实际结果

- 首轮评测目录：
  - `outputs/evals/qwen_lora_v1_full_2026-03-11_234402/`
- `test_v1_summary.json`：
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.380395883563783`
- `external_eval_v1_summary.json`：
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.4089932670018874`

### 第一层结论

- 不能把这轮结果简单解释成“模型完全没学会”。
- 更准确地说，这轮评测首先暴露的是“输出控制问题”，不是“训练链路失效”。

### 关键发现：`<think>` 内容几乎全量泄露

- 在 `test_v1_report.md` 与 `external_eval_v1_report.md` 中，几乎所有样例都包含 `<think>`。
- 这说明当前 Qwen3 推理时把中间推理过程一并输出到了最终答案区域。
- 对评测的直接影响：
  - `exact_match_rate` 被显著拉低
  - `char_f1` 被冗长推理文本污染
  - 人工阅读报告时，也会误把“会思考”当成“会按目标格式作答”

### 具体例子

1. `test_v1 / v1_0012 / defense_followup / char_f1 = 0.3401`
- 参考答案要求直接输出三组 `Q/A`
- 原始预测先输出了长段 `<think> ... </think>`
- 在思维链结束后，只留下了：
  - `以下是模拟答辩老师追问的三`
- 这说明该样例不仅有推理泄露，还出现了答案区被截断的问题

2. `test_v1 / v1_0062 / method_comparison / char_f1 = 0.3428`
- 目标是结构化方法对比
- 预测长时间停留在分析式自述中，例如反复解释“我现在需要帮用户分析……”
- 说明模型知道任务方向，但没有稳定落到目标模板

3. `external_eval_v1 / ext_v1_0007 / experiment_interpretation / char_f1 = 0.3589`
- 参考答案要求“结论-原因-边界-建议”四段式
- 预测同样先输出 `<think>` 推理文本，并在解释阶段停留在分析过程
- 这说明问题不是只在 in-domain 出现，外部集上同样存在

### 如何正确解读 test 与 external 的关系

- 当前首轮结果中：
  - `external_eval_v1` 的 `avg_char_f1 (0.4090)` 反而略高于 `test_v1 (0.3804)`
- 这不能直接解读为“外部泛化比项目内更强”
- 因为当前指标已经被 `<think>` 泄露污染，且两套数据规模都较小
- 所以目前只能说：
  - 两套数据都能触发有一定相关性的输出
  - 但结构控制失败，使当前自动指标不适合直接拿来做最终汇报

### 我做的修复

- 已修正 `scripts/eval_lora_model.py`：
  - 评测时剥离 `<think> ... </think>` 内容
  - 若输出被截断在 `<think>` 区间，清洗后视为无有效最终答案
  - 保留 `raw_prediction` 字段，方便后续做故障分析
  - 在 `generate()` 中显式关闭与采样有关但当前无效的参数，减少 warning 干扰

### 阶段结论

- 截至 2026-03-12，项目已经完成“首轮评测 + 失败模式定位”。
- 当前最重要的不是直接汇报这轮分数，而是：
  - 用修正后的评测脚本重跑
  - 观察去掉 `<think>` 污染后，真实 `exact_match_rate` 与 `char_f1` 能提升多少
  - 再基于清洗后的报告做成功/失败样例分析

### 补充：这轮首评我具体怎么看样例

- 我不是只停在 summary 的两个数字上，而是回到 `report.md` 逐条看低分样例。
- 这一步的目标不是证明模型“行”或“不行”，而是判定失败属于哪一类：
  - 事实错误
  - 结构错误
  - 推理泄露
  - 答案截断

具体看了几个代表样例：

1. `test_v1 / v1_0012 / defense_followup`
- 任务要求：至少输出 3 组 `Q/A`
- 实际现象：预测里先出现大段 `<think> ... </think>`，正式答案只剩一句残缺文本
- 结论：这是“推理泄露 + 截断”的组合故障

2. `test_v1 / v1_0062 / method_comparison`
- 任务要求：结构化比较方法与基线
- 实际现象：模型一直在解释“我现在需要帮助用户分析这个方法”
- 结论：模型知道任务方向，但输出没有稳定收束到模板

3. `external_eval_v1 / ext_v1_0007 / experiment_interpretation`
- 任务要求：按“结论-原因-边界-建议”作答
- 实际现象：同样先输出 `<think>`，再污染正式答案
- 结论：问题具有跨分布一致性，不只是 in-domain 偶发

### 补充：这轮指标应该怎么解释

- `exact_match_rate`
  - 含义：最终输出与参考答案是否严格一致
  - 特点：最严格，最容易被格式差异和 `<think>` 污染直接打成 0
- `avg_char_f1`
  - 含义：字符级重合程度
  - 特点：更宽松，能反映“内容是否部分答到”，但不能保证答案干净

所以这轮首评的正确解释是：

- `exact_match = 0` 不等于“完全不会”
- `char_f1` 仍在 `0.38~0.41` 说明输出与参考答案存在一定内容重合
- 真正首要问题是输出控制失败，导致自动评测口径被污染
## 2026-03-12（补充：首轮评测结果怎么解释，为什么坏结果也是有效经历）

### 这轮结果先说明什么

- 首轮评测目录：
  - `outputs/evals/qwen_lora_v1_full_2026-03-11_234402/`
- `test_v1`：
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.380395883563783`
- `external_eval_v1`：
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.4089932670018874`

### 这轮结果不应该被误读成什么

- 不能直接把 `exact_match_rate = 0` 解读成“模型完全没学会”。
- 不能直接把 `external_eval_v1 (0.4090)` 略高于 `test_v1 (0.3804)` 解读成“模型对外部分布泛化更强”。
- 这轮结果首先说明的是：当前输出控制与评测口径有系统性问题，尤其是 `<think>` 泄露。

### 我是怎么从报告里定位问题的

1. 先看 summary，只判断“值不值得回到样例”，不急着下最终结论。
2. 再看 `worst_examples`，优先挑最差样例和代表性任务。
3. 最后回到 `report.md` 里读原始预测，判断到底是：
   - 事实错
   - 结构错
   - `<think>` 泄露
   - 答案截断

### 这轮最有代表性的失败样例

1. `test_v1 / v1_0012 / defense_followup / char_f1 = 0.3401`
- 任务要求：至少输出 3 组 `Q/A`。
- 实际现象：预测先输出整段 `<think> ... </think>`，最后正式答案只剩一句残缺文本：
  - `以下是模拟答辩老师追问的三`
- 解释：这是“推理泄露 + 答案截断”的组合问题，不是简单的知识全错。

2. `test_v1 / v1_0062 / method_comparison / char_f1 = 0.3428`
- 任务要求：结构化方法对比。
- 实际现象：模型长时间停留在“我现在需要帮助用户分析……”这类自我分析句式，没有稳定落到目标模板。
- 解释：模型抓住了任务方向，但没有稳定收束到最终输出格式。

3. `external_eval_v1 / ext_v1_0007 / experiment_interpretation / char_f1 = 0.3589`
- 任务要求：按“结论-原因-边界-建议”输出。
- 实际现象：同样先进入 `<think>` 推理，再污染正式答案。
- 解释：这说明问题不是只发生在 in-domain，external 上也存在。

### 各任务类型的第一轮读法

- `test_v1`
  - `contribution_extraction = 0.4157`，相对最好，说明抽取类任务更容易学到部分内容。
  - `defense_followup = 0.3644`，最低，说明多问多答格式更容易被 `<think>` 和截断破坏。
  - `experiment_interpretation = 0.3733`
  - `method_comparison = 0.3681`
- `external_eval_v1`
  - `contribution_extraction = 0.4302`，相对最好。
  - `experiment_interpretation = 0.3808`，最低，说明解释类任务在外部分布上更脆弱。
  - `defense_followup = 0.4062`
  - `method_comparison = 0.4187`

### 这轮坏结果为什么仍然是有效项目经历

- 因为我没有停在“分数不好”。
- 我回到逐样本报告，定位了可复现的 failure mode：
  - `<think>` 泄露
  - 答案截断
  - 模板不稳定
- 这意味着我已经走到了“训练后错误分析”这一步，而不是只会运行命令。
- 对老师来说，这比单独报一个分数更能说明我在做的是一个完整工程闭环。

### 可直接复述的话

- “首轮评测分数不好，但我没有把问题简单归因于模型没学会，而是回到逐样本报告做故障定位。”
- “我发现很多低分样例的主问题不是知识完全错误，而是 `<think>` 泄露、答案截断和模板不稳定，所以首轮评测更像是一轮输出控制问题定位。”
- “这类坏结果不是无效经历，反而是后续迭代最有价值的依据，因为它告诉我下一步该修评测口径、还是该继续改训练数据和输出格式。”

## 2026-03-12（第二轮评测产物核对：重跑成功，但结果未发生任何变化）

### 核对范围

- 首轮目录：
  - `outputs/evals/qwen_lora_v1_full_2026-03-11_234402/`
- 第二轮目录：
  - `outputs/evals/qwen_lora_v1_full_2026-03-12_120624/`

### 文件级结论

- `test_v1_summary.json` 的 SHA256 完全一致。
- `external_eval_v1_summary.json` 的 SHA256 完全一致。
- `test_v1_report.md` 的 SHA256 也完全一致。

这说明第二轮不是“分数接近”，而是评测产物逐字相同。

### 我据此得出的判断

- 第二轮确实重新生成了一个新时间戳目录。
- 但新的评测逻辑并没有真正作用到最终输出产物。
- 从新目录里的 `report.md` 继续能看到大量 `<think>` 出现在 `Prediction` 区域。
- 因此当前更合理的结论不是“修复无效”，而是：
  - 这次重跑并没有实际使用到应当生效的清洗逻辑
  - 或者服务器运行的仍是旧版评测脚本

### 这一步的项目价值

- 这次核对说明我没有停在“又跑了一次命令”。
- 我进一步做了产物级比对，而不是只看控制台输出。
- 这类检查对工程项目很重要，因为它能区分：
  - 是模型没有改善
  - 还是评测流程根本没有真正切换到新逻辑

### 下一步应做什么

1. 在服务器上确认 `scripts/eval_lora_model.py` 的实际内容是否包含：
   - `strip_think_content`
   - `raw_prediction`
   - `cleaned_prediction`
2. 确认服务器在重跑前是否真的 `git pull --ff-only`
3. 确认新目录里的 `report.md` 展示的是清洗后预测还是原始预测
4. 在上述检查通过后，再做第三轮评测

### 可直接复述的话

- “我没有把第二轮重跑简单当作一次成功迭代，而是继续做了文件级核对，发现新旧评测产物哈希完全一致。这说明问题不在于模型突然没变化，而在于评测修复逻辑并没有真正作用到结果产物。” 

### 根因补充（已查清）

- 本地 `git log` 显示：
  - `origin/main` 停在 `cf77f84`
  - 清洗 `<think>` 的修复提交是 `536e214`
- 也就是说：
  - 评测修复只在本地 `main` 上
  - 还没有真正进入服务器通过 `git pull` 能拿到的 `origin/main`
- 第二轮服务器评测之所以和第一轮完全一样，根因不是模型没变化，而是：
  - 服务器仍在运行旧版 `scripts/eval_lora_model.py`

### 证据链

1. 两轮 `summary.json` 和 `report.md` 的哈希完全一致。
2. 新目录里的 `report.md` 仍然直接把 `<think>` 放在 `Prediction` 下。
3. 新目录里的 `test_v1_predictions.jsonl` 只有：
   - `prediction`
   - `exact_match`
   - `char_f1`
   没有 `raw_prediction` 字段。
4. 而本地修复后的 `scripts/eval_lora_model.py` 已经会写：
   - `raw_prediction`
   - `prediction`（清洗后）

### 正确结论

- 第二轮结果一模一样，不是“模型能力没有任何变化”的证据。
- 这是“服务器没有跑到修复后评测脚本”的证据。

## 2026-03-12 补充：Third Evaluation Run Produced Clean Scores

### 本轮动作

- 先在服务器确认 `scripts/eval_lora_model.py` 已经包含：
  - `strip_think_content`
  - `raw_prediction`
  - `cleaned_prediction`
- 然后重新执行：
  - `bash scripts/run_eval_v1.sh`
- 本轮评测目录：
  - `outputs/evals/qwen_lora_v1_full_2026-03-12_180125/`

### 结果

- `test_v1`
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.0050335570469798654`
- `external_eval_v1`
  - `exact_match_rate = 0.0000`
  - `avg_char_f1 = 0.0000`

### 为什么分数反而更低

- 这不是模型突然变差，而是评测终于开始对“最终答案”而不是“推理残留文本”打分。
- 前两轮 `char_f1` 之所以还有 `0.38~0.41`，主要是长段 `<think>` 与参考答案共享了不少字符，导致分数被虚高。
- 第三轮把 `<think>` 从 `Prediction` 中剥离后，暴露出的真实问题是：
  - 最终答案经常为空
  - 或者只剩残句
  - 或者没有稳定落到目标模板

### 样例证据

1. `v1_0012`
- `Raw Prediction` 保留了整段 `<think> ... </think>`
- `Prediction` 只剩“以下是模拟答辩老师追问的三”
- 说明模型并非完全没方向，而是答案通道被截断

2. `v1_0062`
- `Raw Prediction` 里有较长分析
- `Prediction` 清洗后为空
- 说明此前的字符重合并不代表有效最终答案

3. `external_eval_v1`
- 全部任务类型 `avg_char_f1 = 0.0`
- 说明 external 上清洗后几乎没有可评分的有效最终答案

### 当前结论

- 评测脚本层面的问题已经基本排除。
- 第三轮之后，优化重点应转向：
  - 训练目标模板是否足够硬
  - 生成阶段是否能稳定只输出最终答案
  - 是否需要额外补充空答案率、结构正确率、残句率等诊断指标

## 2026-03-12 补充：Fourth Iteration Target Hardening Started

### 训练目标审计

- 重新检查 `train_v1.jsonl`：
  - 总样本数 `64`
  - `<think>` 出现次数 `0`
  - 四类任务各 `16`
- 审计结论：
  - 训练标签本身没有被 `<think>` 污染
  - 当前故障更像“生成时未稳定收敛到答案模板”

### 已做修改

- 重写 `scripts/build_dataset_v1.py`
- 重写 `scripts/build_external_eval_v1.py`
- 为四类任务统一加入：
  - “只输出最终答案，不要输出任何思考过程、分析过程、自我提示或 `<think>` / `</think>` 标记”
- 将各任务答案模板写死到更明确的结构：
  - `contribution_extraction`
  - `method_comparison`
  - `experiment_interpretation`
  - `defense_followup`

### 下一步

1. 重新构建 train/val/test 和 external_eval 数据
2. 重新导出 readable 版本并做数据校验
3. 再进入第四轮 `smoke/full/eval`
4. 核心目标先看：
   - 空答案率是否下降
   - 残句率是否下降
   - 模板结构是否开始稳定

## 2026-03-12 补充：Fourth Iteration Hardening Applied Locally

### 这一步我实际改了什么

1. 重写 `scripts/build_dataset_v1.py`
- 四类任务统一改为固定字段模板，而不是宽松长段回答。
- 每类任务都显式要求：
  - 只输出最终答案
  - 不输出 `<think>` / `</think>`
  - 标签与顺序不得改变

2. 重写 `scripts/build_external_eval_v1.py`
- external_eval 与训练集保持同一套输出模板约束。
- 这样可以避免“训练时一种模板、外部评测时另一种模板”的变量混入。

3. 扩展 `scripts/eval_lora_model.py`
- 保留：
  - `empty_prediction_rate`
  - `raw_think_rate`
  - `cleaned_changed_rate`
- 新增：
  - `structure_ok_rate`
- 目的：
  - 不再只看字符重合
  - 直接判断模型最终输出是否真的落到目标结构

### 为什么这一步必要

- 第三轮干净评测已经说明，问题不再是“评分脚本失效”。
- 真实暴露出的故障是：
  - 空答案
  - 残句
  - 模板不收束
- 所以第四轮的正确动作不是再盲目重跑，而是先把训练目标和诊断口径一起收紧。

### 本地验证结果

- `python scripts/build_dataset_v1.py`：通过
- `python scripts/build_external_eval_v1.py`：通过
- `python scripts/export_dataset_readable.py`：通过
- `python scripts/check_dataset_v1.py`：通过
- `python scripts/check_external_eval_v1.py`：通过
- `python -m py_compile scripts/build_dataset_v1.py scripts/build_external_eval_v1.py scripts/eval_lora_model.py`：通过

### 这一步怎么讲

- “第三轮之后，我没有立即继续拉长训练，而是先把输出模板写死，并增加结构正确率指标。”
- “因为前面已经证明问题集中在最终答案通道，所以第四轮先修模板收束，再看分数变化。”

## 2026-03-12 补充：Fourth Iteration Server Loop Attempt Blocked (Connection Refused)

### 这一步我做了什么

- 按第四轮起点先执行本地仓库核对：
  - `git status -sb` 显示工作区干净（`## main...origin/main`）
  - 最新提交仍为 `8197a7d`
- 重新跑第四轮前置校验：
  - `python scripts/check_dataset_v1.py`：通过
  - `python scripts/check_external_eval_v1.py`：通过
  - `python -m py_compile scripts/build_dataset_v1.py scripts/build_external_eval_v1.py scripts/eval_lora_model.py`：通过
- 尝试连接服务器并准备进入真实闭环：
  - `ssh -p 15912 root@connect.bjb1.seetacloud.com "echo connected && hostname && pwd"`
  - 返回 `Connection refused`

### 当前判断

- 当前阻塞点是服务器入口不可达，不是本地脚本或数据问题。
- 第四轮真实 `smoke/full/eval` 还没有开始执行。

### 服务器恢复后的执行顺序（保持不变）

1. `git pull --ff-only`
2. `python scripts/check_dataset_v1.py`
3. `python scripts/check_external_eval_v1.py`
4. `bash scripts/run_train_smoke.sh`
5. `bash scripts/run_train_full.sh`
6. `bash scripts/run_eval_v1.sh`

### 第四轮验收优先级（保持不变）

- `empty_prediction_rate` 是否下降
- `structure_ok_rate` 是否上升
- `raw_think_rate` 是否下降
- 不先执着 `avg_char_f1` 是否立刻明显上涨
