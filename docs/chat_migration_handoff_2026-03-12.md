# Chat Migration Handoff (2026-03-12)

## 1. Purpose

Use this file when the current Codex chat is near limit.
Open a new Codex chat and use the copy-paste package below so the next window can continue immediately.

## 2. Copy-Paste Package for New Chat

Paste everything between the two lines into the first message of the new chat.

```text
继续维护项目：paper_assistant_ft
本地路径：D:\llm_train\paper_assistant_ft

固定目标（不要改）：
1) 项目目标：做一遍完整的大模型微调闭环，用于“网安转 AI”的简历/联系老师/面试项目。
2) 路线固定：LLaMA-Factory + Qwen3-4B + LoRA SFT。
3) 工作方式固定：本地开发 + 服务器执行 + 手动同步（git / scp）。
4) docs 必须持续维护，而且解释要站在“我能讲给老师听”的角度，不只是记流水账。
5) 每次有新增改动，都要给出可直接复制的 `git add / commit / push` 命令。

当前真实状态（截至 2026-03-12）：

A. 数据链路
1) 主数据：
- raw: data/raw/paper_cases_v1.json
- build: scripts/build_dataset_v1.py
- check: scripts/check_dataset_v1.py
- readable export: scripts/export_dataset_readable.py
- split: case-level train/val/test = 64/8/8

2) external_eval：
- raw: data/external_eval/raw/external_eval_cases_v1.json
- build: scripts/build_external_eval_v1.py
- check: scripts/check_external_eval_v1.py
- size: 32
- overlap check: 已做 case_id/title 去重校验

3) 第四轮本地数据模板已经加固：
- 四类任务全部改成固定字段模板，不再是宽松长段回答
- 四类任务都显式要求：
  - 只输出最终答案
  - 不输出 `<think>` / `</think>`
  - 标签和顺序不得改变
- 当前四类模板：
  - contribution_extraction:
    - 核心问题
    - 方法要点
    - 相对基线增益
    - 局限性
  - method_comparison:
    - 对比对象
    - 新方法机制
    - 主要优势
    - 量化结果
    - 代价与风险
    - 结论
  - experiment_interpretation:
    - 结论
    - 原因
    - 边界
    - 建议
  - defense_followup:
    - Q1/A1/Q2/A2/Q3/A3

B. 训练与环境
1) 服务器训练环境已经跑通：
- conda env: paper_ft
- 关键版本：
  - torch 2.6.0+cu124
  - torchvision 0.21.0+cu124
  - torchaudio 2.6.0+cu124
  - transformers 4.52.4
  - numpy 1.26.4
  - fsspec 2025.3.0
  - pillow 11.3.0
- `pip check` 已通过

2) 服务器模型路径：
- /root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B

3) 已完成真实训练：
- smoke：成功
- full：成功
- full 输出目录：
  - outputs/qwen_lora_v1_full

C. 评测链路与结论
1) 评测脚本：
- scripts/eval_lora_model.py
- scripts/run_eval_v1.sh

2) 评测目录与结论：
- 第一轮：
  - outputs/evals/qwen_lora_v1_full_2026-03-11_234402
  - test avg_char_f1 ≈ 0.3804
  - external avg_char_f1 ≈ 0.4090
  - 结论：被 `<think>` 长文本污染，是“脏分数”

- 第二轮：
  - outputs/evals/qwen_lora_v1_full_2026-03-12_120624
  - 与第一轮逐字一致
  - 根因：服务器当时还在跑旧版 eval 脚本，不是模型问题

- 第三轮：
  - outputs/evals/qwen_lora_v1_full_2026-03-12_180125
  - test avg_char_f1 ≈ 0.0050
  - external avg_char_f1 = 0.0000
  - 结论：清洗 `<think>` 后得到“干净分数”
  - 当前真实瓶颈：最终答案通道为空、残句、模板不收束

3) 当前评测脚本已具备：
- strip_think_content
- raw_prediction
- prediction（cleaned）
- empty_prediction_rate
- raw_think_rate
- cleaned_changed_rate
- structure_ok_rate（第四轮新增）

D. 关键解释（必须保持）
1) 第三轮分数掉到接近 0，不代表模型突然退化。
2) 它说明前两轮 `char_f1` 主要被 `<think>` 文本虚高了。
3) 当前真正问题不是评测脚本，而是最终答案通道不稳定。
4) 这个坏结果是有价值的，因为它让项目从“只会报分数”推进到“能定位 failure mode”。

E. docs 已经维护到的重点
请继续维护这些文件，不要删历史内容：
- docs/progress_log.md
- docs/project_plan.md
- docs/interview_notes.md
- docs/02_training/day3_training_hands_on_lab.md
- docs/03_interview/teacher_question_bank.md
- docs/03_interview/interview_notes_categorized.md

F. 当前下一步（最高优先）
目标：做第四轮真实服务器闭环

1) 先检查本地仓库状态，确认是否有未提交改动。
2) 如果有，先提交并 push。
3) 服务器拉最新代码。
4) 在服务器重跑第四轮：
- check
- smoke
- full
- eval
5) 第四轮结果先看：
- empty_prediction_rate 是否下降
- structure_ok_rate 是否上升
- raw_think_rate 是否下降
不要先执着于分数是否明显上涨。

G. 服务器命令块（如果本地已经 push）
```bash
cd ~/paper_assistant_ft
git pull --ff-only

python scripts/check_dataset_v1.py
python scripts/check_external_eval_v1.py

unset OMP_NUM_THREADS
export OMP_NUM_THREADS=8
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate paper_ft

export MODEL_PATH=/root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B

bash scripts/run_train_smoke.sh
bash scripts/run_train_full.sh
bash scripts/run_eval_v1.sh
```

H. 如果服务器 `git pull` 再次 TLS 失败
用本地 `scp` 直接覆盖服务器脚本：
```cmd
cd /d D:\llm_train\paper_assistant_ft
scp -P 15912 scripts\build_dataset_v1.py root@connect.bjb1.seetacloud.com:~/paper_assistant_ft/scripts/
scp -P 15912 scripts\build_external_eval_v1.py root@connect.bjb1.seetacloud.com:~/paper_assistant_ft/scripts/
scp -P 15912 scripts\eval_lora_model.py root@connect.bjb1.seetacloud.com:~/paper_assistant_ft/scripts/
scp -P 15912 scripts\run_eval_v1.sh root@connect.bjb1.seetacloud.com:~/paper_assistant_ft/scripts/
```

I. 新窗口里的工作要求（不要丢）
1) 每一步都要解释：
- 我在做什么
- 为什么这样做
- 怎么验收
- 常见坑是什么

2) 任何重要状态变更都要同步到 docs。

3) 每次涉及更新，都要给出对应的 `git add / commit / push` 命令。

4) 解释要站在“我后面要讲给老师/面试官听”的角度，不是只给结论。
```

## 3. Quick Resume Checklist

Before opening a new chat, optionally run:

```powershell
cd D:\llm_train\paper_assistant_ft
git status -sb
git log --oneline -n 8
```

## 4. Notes

- Do not paste passwords or tokens into chat.
- Server path of interest:
  - `~/paper_assistant_ft`
- Model path of interest:
  - `/root/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B`
- Third-pass clean-eval directory:
  - `outputs/evals/qwen_lora_v1_full_2026-03-12_180125`
- This handoff supersedes the older `docs/chat_migration_handoff_2026-03-11.md`.

## 5. Latest Delta (2026-03-12, after this handoff file was created)

- Local entry checks for fourth round have been re-verified:
  - `git status -sb` clean (`## main...origin/main`)
  - `python scripts/check_dataset_v1.py` passed
  - `python scripts/check_external_eval_v1.py` passed
  - `python -m py_compile scripts/build_dataset_v1.py scripts/build_external_eval_v1.py scripts/eval_lora_model.py` passed
- Server reachability probe attempted:
  - `ssh -p 15912 root@connect.bjb1.seetacloud.com "echo connected && hostname && pwd"`
  - result: `Connection refused`
- Current blocker:
  - Infrastructure reachability only (not local code/data)
- Resume point when server is back:
  - continue exactly from step `F` and command block `G` in this file (`check -> smoke -> full -> eval`)

## 6. Latest Delta (2026-03-12, server loop completed later)

- Fourth-round server loop has been completed with outputs:
  - `outputs/evals/qwen_lora_v1_full_2026-03-12_212350/`
- Key metrics:
  - `test_v1`
    - `avg_char_f1 = 0.5105`
    - `empty_prediction_rate = 0.125`
    - `structure_ok_rate = 0.625`
    - `raw_think_rate = 1.0`
  - `external_eval_v1`
    - `avg_char_f1 = 0.4350`
    - `empty_prediction_rate = 0.25`
    - `structure_ok_rate = 0.34375`
    - `raw_think_rate = 1.0`
- New script capabilities for next pass:
  - `scripts/eval_lora_model.py` now supports:
    - `--disable-thinking`
    - `--run-tag`
    - summary/report fields:
      - `disable_thinking`
      - `thinking_control_modes`
  - `scripts/run_eval_v1.sh` now supports:
    - `DISABLE_THINKING=0/1`
    - `RUN_TAG=<text>`
    - `_nothink` suffix for output directory when `DISABLE_THINKING=1`
- Next gate:
  - run eval A/B first (default vs no-think), do not rush into longer training yet.

## 7. Latest Delta (2026-03-13, no-think gate passed)

- Successful no-think run:
  - `outputs/evals/qwen_lora_v1_full_2026-03-13_082359_nothink/`
- Proof of effective no-think control:
  - `disable_thinking = true`
  - `run_tag = nothink_after_sync`
  - `thinking_control_modes = chat_template_enable_thinking_false`
- Key metrics:
  - `test_v1`
    - `avg_char_f1 = 0.6698`
    - `empty_prediction_rate = 0.0`
    - `raw_think_rate = 0.0`
    - `structure_ok_rate = 1.0`
  - `external_eval_v1`
    - `avg_char_f1 = 0.6990`
    - `empty_prediction_rate = 0.0`
    - `raw_think_rate = 0.0`
    - `structure_ok_rate = 1.0`
- Process hardening added:
  - `scripts/run_eval_v1.sh` fail-fast when tag/flag mismatch (`nothink` tag but `DISABLE_THINKING!=1`)
  - invalid `OMP_NUM_THREADS` auto-correction to `8`
