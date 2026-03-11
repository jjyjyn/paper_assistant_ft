# Case 到训练样本映射讲解（case_004）

## 1. 原始 case（输入原料）

来源：`data/raw/paper_cases_v1.json` 中 `case_004`

```json
{
  "case_id": "case_004",
  "title": "Token Pruning for Efficient Chinese LLM Inference",
  "problem": "长上下文推理显存占用高，推理速度慢。",
  "method": "在中间层动态剪枝低贡献 token，仅保留高注意力权重 token 继续传播。",
  "baseline": "Full Attention, Static Window Attention",
  "result": "在 8k 上下文下吞吐提升 1.42 倍，平均准确率下降小于 0.8%。",
  "limitations": "对需要全局细粒度信息的任务存在小幅性能损失。"
}
```

## 2. 对应训练样本（experiment_interpretation）

示例：`v1_0015`（`source_case_id = case_004`）

- `task_type`: `experiment_interpretation`
- `instruction`: 任务指令模板（固定）
- `input`: 由 case 字段拼接
- `output`: 基于 case 字段生成的“结论-原因-边界-建议”结构化答案

---

## 3. 一一对照（你要会讲）

## 3.1 直接映射到 input（逐字段）

| case 字段 | input 中位置 | 映射方式 |
|---|---|---|
| `title` | `论文标题:` | 直接拷贝 |
| `problem` | `研究问题:` | 直接拷贝 |
| `method` | `核心方法:` | 直接拷贝 |
| `baseline` | `对比基线:` | 直接拷贝 |
| `result` | `实验结果:` | 直接拷贝 |
| `limitations` | `局限性:` | 直接拷贝 |

说明：`input` 本质是把原始 case 做了格式化排版，信息不变。

## 3.2 output 如何从 case 生成（逐句）

`output` 模板结构是：

1. 结论：引用 `result`  
2. 原因：引用 `method` + `problem`  
3. 边界：引用 `limitations`  
4. 建议：模板补充句（非 case 原句）

具体到你这条样本：

- 结论句来自：`result`
- 原因句来自：`method` + `problem`
- 边界句来自：`limitations`
- 建议句是模板句：用于让回答更完整（不是新事实）

---

## 4. 哪些是“事实”，哪些是“模板”

### 4.1 事实内容（必须可回溯）

- 指标数值（例如 1.42 倍、<0.8%）
- 方法描述
- 局限性描述

这些必须能在 case 里找到来源，不能凭空新增。

### 4.2 模板内容（允许，但要克制）

- 回答结构词：`结论/原因/边界/建议`
- 通用建议句：如“补充跨域验证”

模板句的作用是提升表达完整性，但不能引入与 case 冲突的新结论。

---

## 5. 你后续改数据时怎么做

如果你觉得 `v1_0015` 不够好，不要直接改 `train_v1.jsonl`，而是按这个流程：

1. 改源头：`data/raw/paper_cases_v1.json` 的 `case_004`
2. 重建：`python scripts/build_dataset_v1.py`
3. 校验：`python scripts/check_dataset_v1.py`
4. 导出可读：`python scripts/export_dataset_readable.py`
5. 回看 `train_v1_readable.md` 对应条目

这样做的好处是：可复现、可追踪、可批量升级。

---

## 6. 面试可直接说的 3 句话

1. “我把原始论文案例抽象为结构化 case，再映射到 instruction/input/output 训练样本。”  
2. “样本中的事实信息全部可回溯到 source_case_id，模板只负责组织表达，不制造新事实。”  
3. “我通过源头 case 修改 + 脚本重建，保证了数据改动的可复现和可审计。”  
