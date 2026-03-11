# external_eval_v1 readable view

- Total samples: 32

## 1. ext_v1_0001

- task_type: `contribution_extraction`
- source_case_id: `ext_case_001`
- split: `external_test`

### instruction

```text
请提炼该工作最关键的三点贡献，要求分别覆盖问题、方法创新和结果价值。
```

### input

```text
论文标题: Cross-Modal Citation Grounding for Figure-Centric Papers
研究问题: 图表密集型论文中，文字结论与图中证据常出现对应不清，导致引用解释不可靠。
核心方法: 构建图文双通道检索器，并在候选证据上执行区域级对齐打分，再生成带证据编号的解释。
对比基线: Text-only retrieval, Caption-only retrieval
实验结果: 在 FigureQA-Cite 基准上，证据命中率提升 9.8%，错误引用率下降 27%。
局限性: 当图像质量较差或坐标标注缺失时，对齐稳定性明显下降。
```

### output

```text
核心贡献可归纳为三点:
1) 问题导向: 聚焦“图表密集型论文中，文字结论与图中证据常出现对应不清，导致引用解释不可靠。”这一高频痛点，并给出可落地方案。
2) 方法创新: 采用“构建图文双通道检索器，并在候选证据上执行区域级对齐打分，再生成带证据编号的解释。”，在信息利用效率上优于常规路径。
3) 结果价值: 相比“Text-only retrieval, Caption-only retrieval”，实验显示“在 FigureQA-Cite 基准上，证据命中率提升 9.8%，错误引用率下降 27%。”。
同时需注意作者给出的边界条件“当图像质量较差或坐标标注缺失时，对齐稳定性明显下降。”。
```

## 2. ext_v1_0002

- task_type: `method_comparison`
- source_case_id: `ext_case_001`
- split: `external_test`

### instruction

```text
请做结构化方法对比，说明新方法为何更优，以及代价和风险。
```

### input

```text
论文标题: Cross-Modal Citation Grounding for Figure-Centric Papers
研究问题: 图表密集型论文中，文字结论与图中证据常出现对应不清，导致引用解释不可靠。
核心方法: 构建图文双通道检索器，并在候选证据上执行区域级对齐打分，再生成带证据编号的解释。
对比基线: Text-only retrieval, Caption-only retrieval
实验结果: 在 FigureQA-Cite 基准上，证据命中率提升 9.8%，错误引用率下降 27%。
局限性: 当图像质量较差或坐标标注缺失时，对齐稳定性明显下降。
```

### output

```text
方法对比如下:
- 对比对象: Text-only retrieval, Caption-only retrieval
- 新方法机制: 构建图文双通道检索器，并在候选证据上执行区域级对齐打分，再生成带证据编号的解释。
- 主要优势: 对目标瓶颈更有针对性，通常能提高有效证据利用率和推理稳定性。
- 量化结果: 在 FigureQA-Cite 基准上，证据命中率提升 9.8%，错误引用率下降 27%。
- 代价与风险: 当图像质量较差或坐标标注缺失时，对齐稳定性明显下降。
- 结论: 该方法体现的是“性能-成本-鲁棒性”之间的再平衡，而非无代价提升。
```

## 3. ext_v1_0003

- task_type: `experiment_interpretation`
- source_case_id: `ext_case_001`
- split: `external_test`

### instruction

```text
请用“结论-原因-边界”解释实验结果，并给出后续验证建议。
```

### input

```text
论文标题: Cross-Modal Citation Grounding for Figure-Centric Papers
研究问题: 图表密集型论文中，文字结论与图中证据常出现对应不清，导致引用解释不可靠。
核心方法: 构建图文双通道检索器，并在候选证据上执行区域级对齐打分，再生成带证据编号的解释。
对比基线: Text-only retrieval, Caption-only retrieval
实验结果: 在 FigureQA-Cite 基准上，证据命中率提升 9.8%，错误引用率下降 27%。
局限性: 当图像质量较差或坐标标注缺失时，对齐稳定性明显下降。
```

### output

```text
结论: “在 FigureQA-Cite 基准上，证据命中率提升 9.8%，错误引用率下降 27%。”说明该方法在目标任务上具有可观收益。
原因: 收益主要来自“构建图文双通道检索器，并在候选证据上执行区域级对齐打分，再生成带证据编号的解释。”，其机制上更直接缓解了“图表密集型论文中，文字结论与图中证据常出现对应不清，导致引用解释不可靠。”。
边界: “当图像质量较差或坐标标注缺失时，对齐稳定性明显下降。”提示该方法在特定场景下可能退化。
建议: 进一步补充跨域实验与资源受限条件下的稳定性验证。
```

## 4. ext_v1_0004

- task_type: `defense_followup`
- source_case_id: `ext_case_001`
- split: `external_test`

### instruction

```text
请模拟答辩追问，给出 3 组高质量问答，聚焦创新性、证据充分性和局限改进。
```

### input

```text
论文标题: Cross-Modal Citation Grounding for Figure-Centric Papers
研究问题: 图表密集型论文中，文字结论与图中证据常出现对应不清，导致引用解释不可靠。
核心方法: 构建图文双通道检索器，并在候选证据上执行区域级对齐打分，再生成带证据编号的解释。
对比基线: Text-only retrieval, Caption-only retrieval
实验结果: 在 FigureQA-Cite 基准上，证据命中率提升 9.8%，错误引用率下降 27%。
局限性: 当图像质量较差或坐标标注缺失时，对齐稳定性明显下降。
```

### output

```text
Q1: 你相对基线的真正创新是什么？
A1: 创新点在于“构建图文双通道检索器，并在候选证据上执行区域级对齐打分，再生成带证据编号的解释。”，它不是简单叠加模块，而是直接针对“图表密集型论文中，文字结论与图中证据常出现对应不清，导致引用解释不可靠。”的机制级改造。

Q2: 你的实验是否足以支撑结论？
A2: 从结果“在 FigureQA-Cite 基准上，证据命中率提升 9.8%，错误引用率下降 27%。”看，收益方向明确；但仍需更多跨场景验证以增强结论外推性。

Q3: 已知局限是什么，下一步怎么改？
A3: 当前主要局限是“当图像质量较差或坐标标注缺失时，对齐稳定性明显下降。”。下一步应优先做失效场景分析与针对性鲁棒性增强。
```

## 5. ext_v1_0005

- task_type: `contribution_extraction`
- source_case_id: `ext_case_002`
- split: `external_test`

### instruction

```text
请提炼该工作最关键的三点贡献，要求分别覆盖问题、方法创新和结果价值。
```

### input

```text
论文标题: Adaptive Unit Normalization for Scientific Table Extraction
研究问题: 跨论文比较实验指标时，单位不统一导致结论偏差。
核心方法: 先识别单位与量纲，再执行规则+模型混合归一化，将表格值映射到统一标准单位。
对比基线: Regex-only normalization, Manual post-processing
实验结果: 在单位归一化测试集上，标准化准确率从 81.4% 提升到 92.7%。
局限性: 对新出现的非标准单位缩写仍需人工词典补充。
```

### output

```text
核心贡献可归纳为三点:
1) 问题导向: 聚焦“跨论文比较实验指标时，单位不统一导致结论偏差。”这一高频痛点，并给出可落地方案。
2) 方法创新: 采用“先识别单位与量纲，再执行规则+模型混合归一化，将表格值映射到统一标准单位。”，在信息利用效率上优于常规路径。
3) 结果价值: 相比“Regex-only normalization, Manual post-processing”，实验显示“在单位归一化测试集上，标准化准确率从 81.4% 提升到 92.7%。”。
同时需注意作者给出的边界条件“对新出现的非标准单位缩写仍需人工词典补充。”。
```

## 6. ext_v1_0006

- task_type: `method_comparison`
- source_case_id: `ext_case_002`
- split: `external_test`

### instruction

```text
请做结构化方法对比，说明新方法为何更优，以及代价和风险。
```

### input

```text
论文标题: Adaptive Unit Normalization for Scientific Table Extraction
研究问题: 跨论文比较实验指标时，单位不统一导致结论偏差。
核心方法: 先识别单位与量纲，再执行规则+模型混合归一化，将表格值映射到统一标准单位。
对比基线: Regex-only normalization, Manual post-processing
实验结果: 在单位归一化测试集上，标准化准确率从 81.4% 提升到 92.7%。
局限性: 对新出现的非标准单位缩写仍需人工词典补充。
```

### output

```text
方法对比如下:
- 对比对象: Regex-only normalization, Manual post-processing
- 新方法机制: 先识别单位与量纲，再执行规则+模型混合归一化，将表格值映射到统一标准单位。
- 主要优势: 对目标瓶颈更有针对性，通常能提高有效证据利用率和推理稳定性。
- 量化结果: 在单位归一化测试集上，标准化准确率从 81.4% 提升到 92.7%。
- 代价与风险: 对新出现的非标准单位缩写仍需人工词典补充。
- 结论: 该方法体现的是“性能-成本-鲁棒性”之间的再平衡，而非无代价提升。
```

## 7. ext_v1_0007

- task_type: `experiment_interpretation`
- source_case_id: `ext_case_002`
- split: `external_test`

### instruction

```text
请用“结论-原因-边界”解释实验结果，并给出后续验证建议。
```

### input

```text
论文标题: Adaptive Unit Normalization for Scientific Table Extraction
研究问题: 跨论文比较实验指标时，单位不统一导致结论偏差。
核心方法: 先识别单位与量纲，再执行规则+模型混合归一化，将表格值映射到统一标准单位。
对比基线: Regex-only normalization, Manual post-processing
实验结果: 在单位归一化测试集上，标准化准确率从 81.4% 提升到 92.7%。
局限性: 对新出现的非标准单位缩写仍需人工词典补充。
```

### output

```text
结论: “在单位归一化测试集上，标准化准确率从 81.4% 提升到 92.7%。”说明该方法在目标任务上具有可观收益。
原因: 收益主要来自“先识别单位与量纲，再执行规则+模型混合归一化，将表格值映射到统一标准单位。”，其机制上更直接缓解了“跨论文比较实验指标时，单位不统一导致结论偏差。”。
边界: “对新出现的非标准单位缩写仍需人工词典补充。”提示该方法在特定场景下可能退化。
建议: 进一步补充跨域实验与资源受限条件下的稳定性验证。
```

## 8. ext_v1_0008

- task_type: `defense_followup`
- source_case_id: `ext_case_002`
- split: `external_test`

### instruction

```text
请模拟答辩追问，给出 3 组高质量问答，聚焦创新性、证据充分性和局限改进。
```

### input

```text
论文标题: Adaptive Unit Normalization for Scientific Table Extraction
研究问题: 跨论文比较实验指标时，单位不统一导致结论偏差。
核心方法: 先识别单位与量纲，再执行规则+模型混合归一化，将表格值映射到统一标准单位。
对比基线: Regex-only normalization, Manual post-processing
实验结果: 在单位归一化测试集上，标准化准确率从 81.4% 提升到 92.7%。
局限性: 对新出现的非标准单位缩写仍需人工词典补充。
```

### output

```text
Q1: 你相对基线的真正创新是什么？
A1: 创新点在于“先识别单位与量纲，再执行规则+模型混合归一化，将表格值映射到统一标准单位。”，它不是简单叠加模块，而是直接针对“跨论文比较实验指标时，单位不统一导致结论偏差。”的机制级改造。

Q2: 你的实验是否足以支撑结论？
A2: 从结果“在单位归一化测试集上，标准化准确率从 81.4% 提升到 92.7%。”看，收益方向明确；但仍需更多跨场景验证以增强结论外推性。

Q3: 已知局限是什么，下一步怎么改？
A3: 当前主要局限是“对新出现的非标准单位缩写仍需人工词典补充。”。下一步应优先做失效场景分析与针对性鲁棒性增强。
```

## 9. ext_v1_0009

- task_type: `contribution_extraction`
- source_case_id: `ext_case_003`
- split: `external_test`

### instruction

```text
请提炼该工作最关键的三点贡献，要求分别覆盖问题、方法创新和结果价值。
```

### input

```text
论文标题: Debate-Style Verifier for Mathematical Proof Assistants
研究问题: 模型在数学证明问答中容易给出看似合理但逻辑断裂的解释。
核心方法: 引入主张-反驳双代理辩论，并由裁决器基于步骤一致性与反例覆盖度打分。
对比基线: Single-pass chain-of-thought verifier
实验结果: 在 ProofBench-ZH 上，步骤一致性评分提升 11.6%，致命逻辑错误率下降 18%。
局限性: 多代理流程推理成本较高，延迟显著增加。
```

### output

```text
核心贡献可归纳为三点:
1) 问题导向: 聚焦“模型在数学证明问答中容易给出看似合理但逻辑断裂的解释。”这一高频痛点，并给出可落地方案。
2) 方法创新: 采用“引入主张-反驳双代理辩论，并由裁决器基于步骤一致性与反例覆盖度打分。”，在信息利用效率上优于常规路径。
3) 结果价值: 相比“Single-pass chain-of-thought verifier”，实验显示“在 ProofBench-ZH 上，步骤一致性评分提升 11.6%，致命逻辑错误率下降 18%。”。
同时需注意作者给出的边界条件“多代理流程推理成本较高，延迟显著增加。”。
```

## 10. ext_v1_0010

- task_type: `method_comparison`
- source_case_id: `ext_case_003`
- split: `external_test`

### instruction

```text
请做结构化方法对比，说明新方法为何更优，以及代价和风险。
```

### input

```text
论文标题: Debate-Style Verifier for Mathematical Proof Assistants
研究问题: 模型在数学证明问答中容易给出看似合理但逻辑断裂的解释。
核心方法: 引入主张-反驳双代理辩论，并由裁决器基于步骤一致性与反例覆盖度打分。
对比基线: Single-pass chain-of-thought verifier
实验结果: 在 ProofBench-ZH 上，步骤一致性评分提升 11.6%，致命逻辑错误率下降 18%。
局限性: 多代理流程推理成本较高，延迟显著增加。
```

### output

```text
方法对比如下:
- 对比对象: Single-pass chain-of-thought verifier
- 新方法机制: 引入主张-反驳双代理辩论，并由裁决器基于步骤一致性与反例覆盖度打分。
- 主要优势: 对目标瓶颈更有针对性，通常能提高有效证据利用率和推理稳定性。
- 量化结果: 在 ProofBench-ZH 上，步骤一致性评分提升 11.6%，致命逻辑错误率下降 18%。
- 代价与风险: 多代理流程推理成本较高，延迟显著增加。
- 结论: 该方法体现的是“性能-成本-鲁棒性”之间的再平衡，而非无代价提升。
```

## 11. ext_v1_0011

- task_type: `experiment_interpretation`
- source_case_id: `ext_case_003`
- split: `external_test`

### instruction

```text
请用“结论-原因-边界”解释实验结果，并给出后续验证建议。
```

### input

```text
论文标题: Debate-Style Verifier for Mathematical Proof Assistants
研究问题: 模型在数学证明问答中容易给出看似合理但逻辑断裂的解释。
核心方法: 引入主张-反驳双代理辩论，并由裁决器基于步骤一致性与反例覆盖度打分。
对比基线: Single-pass chain-of-thought verifier
实验结果: 在 ProofBench-ZH 上，步骤一致性评分提升 11.6%，致命逻辑错误率下降 18%。
局限性: 多代理流程推理成本较高，延迟显著增加。
```

### output

```text
结论: “在 ProofBench-ZH 上，步骤一致性评分提升 11.6%，致命逻辑错误率下降 18%。”说明该方法在目标任务上具有可观收益。
原因: 收益主要来自“引入主张-反驳双代理辩论，并由裁决器基于步骤一致性与反例覆盖度打分。”，其机制上更直接缓解了“模型在数学证明问答中容易给出看似合理但逻辑断裂的解释。”。
边界: “多代理流程推理成本较高，延迟显著增加。”提示该方法在特定场景下可能退化。
建议: 进一步补充跨域实验与资源受限条件下的稳定性验证。
```

## 12. ext_v1_0012

- task_type: `defense_followup`
- source_case_id: `ext_case_003`
- split: `external_test`

### instruction

```text
请模拟答辩追问，给出 3 组高质量问答，聚焦创新性、证据充分性和局限改进。
```

### input

```text
论文标题: Debate-Style Verifier for Mathematical Proof Assistants
研究问题: 模型在数学证明问答中容易给出看似合理但逻辑断裂的解释。
核心方法: 引入主张-反驳双代理辩论，并由裁决器基于步骤一致性与反例覆盖度打分。
对比基线: Single-pass chain-of-thought verifier
实验结果: 在 ProofBench-ZH 上，步骤一致性评分提升 11.6%，致命逻辑错误率下降 18%。
局限性: 多代理流程推理成本较高，延迟显著增加。
```

### output

```text
Q1: 你相对基线的真正创新是什么？
A1: 创新点在于“引入主张-反驳双代理辩论，并由裁决器基于步骤一致性与反例覆盖度打分。”，它不是简单叠加模块，而是直接针对“模型在数学证明问答中容易给出看似合理但逻辑断裂的解释。”的机制级改造。

Q2: 你的实验是否足以支撑结论？
A2: 从结果“在 ProofBench-ZH 上，步骤一致性评分提升 11.6%，致命逻辑错误率下降 18%。”看，收益方向明确；但仍需更多跨场景验证以增强结论外推性。

Q3: 已知局限是什么，下一步怎么改？
A3: 当前主要局限是“多代理流程推理成本较高，延迟显著增加。”。下一步应优先做失效场景分析与针对性鲁棒性增强。
```

## 13. ext_v1_0013

- task_type: `contribution_extraction`
- source_case_id: `ext_case_004`
- split: `external_test`

### instruction

```text
请提炼该工作最关键的三点贡献，要求分别覆盖问题、方法创新和结果价值。
```

### input

```text
论文标题: Sparse Activation Routing for Biomedical Chinese LLMs
研究问题: 生物医学长文本问答中，模型推理成本高且关键实体易被噪声干扰。
核心方法: 在中间层加入稀疏激活路由，仅激活与医学实体子图相关的专家通道。
对比基线: Dense MoE routing, Vanilla dense transformer
实验结果: 在 MedLongQA-ZH 上，推理吞吐提升 1.31 倍，F1 提升 3.9 个百分点。
局限性: 当实体链接错误时，路由会放大误检影响。
```

### output

```text
核心贡献可归纳为三点:
1) 问题导向: 聚焦“生物医学长文本问答中，模型推理成本高且关键实体易被噪声干扰。”这一高频痛点，并给出可落地方案。
2) 方法创新: 采用“在中间层加入稀疏激活路由，仅激活与医学实体子图相关的专家通道。”，在信息利用效率上优于常规路径。
3) 结果价值: 相比“Dense MoE routing, Vanilla dense transformer”，实验显示“在 MedLongQA-ZH 上，推理吞吐提升 1.31 倍，F1 提升 3.9 个百分点。”。
同时需注意作者给出的边界条件“当实体链接错误时，路由会放大误检影响。”。
```

## 14. ext_v1_0014

- task_type: `method_comparison`
- source_case_id: `ext_case_004`
- split: `external_test`

### instruction

```text
请做结构化方法对比，说明新方法为何更优，以及代价和风险。
```

### input

```text
论文标题: Sparse Activation Routing for Biomedical Chinese LLMs
研究问题: 生物医学长文本问答中，模型推理成本高且关键实体易被噪声干扰。
核心方法: 在中间层加入稀疏激活路由，仅激活与医学实体子图相关的专家通道。
对比基线: Dense MoE routing, Vanilla dense transformer
实验结果: 在 MedLongQA-ZH 上，推理吞吐提升 1.31 倍，F1 提升 3.9 个百分点。
局限性: 当实体链接错误时，路由会放大误检影响。
```

### output

```text
方法对比如下:
- 对比对象: Dense MoE routing, Vanilla dense transformer
- 新方法机制: 在中间层加入稀疏激活路由，仅激活与医学实体子图相关的专家通道。
- 主要优势: 对目标瓶颈更有针对性，通常能提高有效证据利用率和推理稳定性。
- 量化结果: 在 MedLongQA-ZH 上，推理吞吐提升 1.31 倍，F1 提升 3.9 个百分点。
- 代价与风险: 当实体链接错误时，路由会放大误检影响。
- 结论: 该方法体现的是“性能-成本-鲁棒性”之间的再平衡，而非无代价提升。
```

## 15. ext_v1_0015

- task_type: `experiment_interpretation`
- source_case_id: `ext_case_004`
- split: `external_test`

### instruction

```text
请用“结论-原因-边界”解释实验结果，并给出后续验证建议。
```

### input

```text
论文标题: Sparse Activation Routing for Biomedical Chinese LLMs
研究问题: 生物医学长文本问答中，模型推理成本高且关键实体易被噪声干扰。
核心方法: 在中间层加入稀疏激活路由，仅激活与医学实体子图相关的专家通道。
对比基线: Dense MoE routing, Vanilla dense transformer
实验结果: 在 MedLongQA-ZH 上，推理吞吐提升 1.31 倍，F1 提升 3.9 个百分点。
局限性: 当实体链接错误时，路由会放大误检影响。
```

### output

```text
结论: “在 MedLongQA-ZH 上，推理吞吐提升 1.31 倍，F1 提升 3.9 个百分点。”说明该方法在目标任务上具有可观收益。
原因: 收益主要来自“在中间层加入稀疏激活路由，仅激活与医学实体子图相关的专家通道。”，其机制上更直接缓解了“生物医学长文本问答中，模型推理成本高且关键实体易被噪声干扰。”。
边界: “当实体链接错误时，路由会放大误检影响。”提示该方法在特定场景下可能退化。
建议: 进一步补充跨域实验与资源受限条件下的稳定性验证。
```

## 16. ext_v1_0016

- task_type: `defense_followup`
- source_case_id: `ext_case_004`
- split: `external_test`

### instruction

```text
请模拟答辩追问，给出 3 组高质量问答，聚焦创新性、证据充分性和局限改进。
```

### input

```text
论文标题: Sparse Activation Routing for Biomedical Chinese LLMs
研究问题: 生物医学长文本问答中，模型推理成本高且关键实体易被噪声干扰。
核心方法: 在中间层加入稀疏激活路由，仅激活与医学实体子图相关的专家通道。
对比基线: Dense MoE routing, Vanilla dense transformer
实验结果: 在 MedLongQA-ZH 上，推理吞吐提升 1.31 倍，F1 提升 3.9 个百分点。
局限性: 当实体链接错误时，路由会放大误检影响。
```

### output

```text
Q1: 你相对基线的真正创新是什么？
A1: 创新点在于“在中间层加入稀疏激活路由，仅激活与医学实体子图相关的专家通道。”，它不是简单叠加模块，而是直接针对“生物医学长文本问答中，模型推理成本高且关键实体易被噪声干扰。”的机制级改造。

Q2: 你的实验是否足以支撑结论？
A2: 从结果“在 MedLongQA-ZH 上，推理吞吐提升 1.31 倍，F1 提升 3.9 个百分点。”看，收益方向明确；但仍需更多跨场景验证以增强结论外推性。

Q3: 已知局限是什么，下一步怎么改？
A3: 当前主要局限是“当实体链接错误时，路由会放大误检影响。”。下一步应优先做失效场景分析与针对性鲁棒性增强。
```

## 17. ext_v1_0017

- task_type: `contribution_extraction`
- source_case_id: `ext_case_005`
- split: `external_test`

### instruction

```text
请提炼该工作最关键的三点贡献，要求分别覆盖问题、方法创新和结果价值。
```

### input

```text
论文标题: Temporal Drift Benchmark for Continual Paper QA
研究问题: 模型对旧论文结论记忆稳定，但对新版本结论更新不及时。
核心方法: 构建按时间切片的问答评测集，分别衡量历史记忆保持率与新事实吸收率。
对比基线: Static random split benchmark
实验结果: 发现主流模型在新事实吸收率上平均仅 46%，明显低于历史记忆保持率。
局限性: 时间戳依赖元数据质量，跨来源数据存在对齐噪声。
```

### output

```text
核心贡献可归纳为三点:
1) 问题导向: 聚焦“模型对旧论文结论记忆稳定，但对新版本结论更新不及时。”这一高频痛点，并给出可落地方案。
2) 方法创新: 采用“构建按时间切片的问答评测集，分别衡量历史记忆保持率与新事实吸收率。”，在信息利用效率上优于常规路径。
3) 结果价值: 相比“Static random split benchmark”，实验显示“发现主流模型在新事实吸收率上平均仅 46%，明显低于历史记忆保持率。”。
同时需注意作者给出的边界条件“时间戳依赖元数据质量，跨来源数据存在对齐噪声。”。
```

## 18. ext_v1_0018

- task_type: `method_comparison`
- source_case_id: `ext_case_005`
- split: `external_test`

### instruction

```text
请做结构化方法对比，说明新方法为何更优，以及代价和风险。
```

### input

```text
论文标题: Temporal Drift Benchmark for Continual Paper QA
研究问题: 模型对旧论文结论记忆稳定，但对新版本结论更新不及时。
核心方法: 构建按时间切片的问答评测集，分别衡量历史记忆保持率与新事实吸收率。
对比基线: Static random split benchmark
实验结果: 发现主流模型在新事实吸收率上平均仅 46%，明显低于历史记忆保持率。
局限性: 时间戳依赖元数据质量，跨来源数据存在对齐噪声。
```

### output

```text
方法对比如下:
- 对比对象: Static random split benchmark
- 新方法机制: 构建按时间切片的问答评测集，分别衡量历史记忆保持率与新事实吸收率。
- 主要优势: 对目标瓶颈更有针对性，通常能提高有效证据利用率和推理稳定性。
- 量化结果: 发现主流模型在新事实吸收率上平均仅 46%，明显低于历史记忆保持率。
- 代价与风险: 时间戳依赖元数据质量，跨来源数据存在对齐噪声。
- 结论: 该方法体现的是“性能-成本-鲁棒性”之间的再平衡，而非无代价提升。
```

## 19. ext_v1_0019

- task_type: `experiment_interpretation`
- source_case_id: `ext_case_005`
- split: `external_test`

### instruction

```text
请用“结论-原因-边界”解释实验结果，并给出后续验证建议。
```

### input

```text
论文标题: Temporal Drift Benchmark for Continual Paper QA
研究问题: 模型对旧论文结论记忆稳定，但对新版本结论更新不及时。
核心方法: 构建按时间切片的问答评测集，分别衡量历史记忆保持率与新事实吸收率。
对比基线: Static random split benchmark
实验结果: 发现主流模型在新事实吸收率上平均仅 46%，明显低于历史记忆保持率。
局限性: 时间戳依赖元数据质量，跨来源数据存在对齐噪声。
```

### output

```text
结论: “发现主流模型在新事实吸收率上平均仅 46%，明显低于历史记忆保持率。”说明该方法在目标任务上具有可观收益。
原因: 收益主要来自“构建按时间切片的问答评测集，分别衡量历史记忆保持率与新事实吸收率。”，其机制上更直接缓解了“模型对旧论文结论记忆稳定，但对新版本结论更新不及时。”。
边界: “时间戳依赖元数据质量，跨来源数据存在对齐噪声。”提示该方法在特定场景下可能退化。
建议: 进一步补充跨域实验与资源受限条件下的稳定性验证。
```

## 20. ext_v1_0020

- task_type: `defense_followup`
- source_case_id: `ext_case_005`
- split: `external_test`

### instruction

```text
请模拟答辩追问，给出 3 组高质量问答，聚焦创新性、证据充分性和局限改进。
```

### input

```text
论文标题: Temporal Drift Benchmark for Continual Paper QA
研究问题: 模型对旧论文结论记忆稳定，但对新版本结论更新不及时。
核心方法: 构建按时间切片的问答评测集，分别衡量历史记忆保持率与新事实吸收率。
对比基线: Static random split benchmark
实验结果: 发现主流模型在新事实吸收率上平均仅 46%，明显低于历史记忆保持率。
局限性: 时间戳依赖元数据质量，跨来源数据存在对齐噪声。
```

### output

```text
Q1: 你相对基线的真正创新是什么？
A1: 创新点在于“构建按时间切片的问答评测集，分别衡量历史记忆保持率与新事实吸收率。”，它不是简单叠加模块，而是直接针对“模型对旧论文结论记忆稳定，但对新版本结论更新不及时。”的机制级改造。

Q2: 你的实验是否足以支撑结论？
A2: 从结果“发现主流模型在新事实吸收率上平均仅 46%，明显低于历史记忆保持率。”看，收益方向明确；但仍需更多跨场景验证以增强结论外推性。

Q3: 已知局限是什么，下一步怎么改？
A3: 当前主要局限是“时间戳依赖元数据质量，跨来源数据存在对齐噪声。”。下一步应优先做失效场景分析与针对性鲁棒性增强。
```

## 21. ext_v1_0021

- task_type: `contribution_extraction`
- source_case_id: `ext_case_006`
- split: `external_test`

### instruction

```text
请提炼该工作最关键的三点贡献，要求分别覆盖问题、方法创新和结果价值。
```

### input

```text
论文标题: Noise-Robust OCR-to-Reasoning Pipeline for Scanned Papers
研究问题: 扫描版论文 OCR 噪声高，导致后续问答链路错误累积。
核心方法: 先进行版面纠错与术语恢复，再做结构化检索与答案生成的两阶段推理。
对比基线: Direct OCR text QA
实验结果: 在 ScanPaperQA 数据上，端到端准确率提升 8.4%，幻觉率下降 22%。
局限性: 对复杂公式区域仍存在识别缺失，影响深度推理。
```

### output

```text
核心贡献可归纳为三点:
1) 问题导向: 聚焦“扫描版论文 OCR 噪声高，导致后续问答链路错误累积。”这一高频痛点，并给出可落地方案。
2) 方法创新: 采用“先进行版面纠错与术语恢复，再做结构化检索与答案生成的两阶段推理。”，在信息利用效率上优于常规路径。
3) 结果价值: 相比“Direct OCR text QA”，实验显示“在 ScanPaperQA 数据上，端到端准确率提升 8.4%，幻觉率下降 22%。”。
同时需注意作者给出的边界条件“对复杂公式区域仍存在识别缺失，影响深度推理。”。
```

## 22. ext_v1_0022

- task_type: `method_comparison`
- source_case_id: `ext_case_006`
- split: `external_test`

### instruction

```text
请做结构化方法对比，说明新方法为何更优，以及代价和风险。
```

### input

```text
论文标题: Noise-Robust OCR-to-Reasoning Pipeline for Scanned Papers
研究问题: 扫描版论文 OCR 噪声高，导致后续问答链路错误累积。
核心方法: 先进行版面纠错与术语恢复，再做结构化检索与答案生成的两阶段推理。
对比基线: Direct OCR text QA
实验结果: 在 ScanPaperQA 数据上，端到端准确率提升 8.4%，幻觉率下降 22%。
局限性: 对复杂公式区域仍存在识别缺失，影响深度推理。
```

### output

```text
方法对比如下:
- 对比对象: Direct OCR text QA
- 新方法机制: 先进行版面纠错与术语恢复，再做结构化检索与答案生成的两阶段推理。
- 主要优势: 对目标瓶颈更有针对性，通常能提高有效证据利用率和推理稳定性。
- 量化结果: 在 ScanPaperQA 数据上，端到端准确率提升 8.4%，幻觉率下降 22%。
- 代价与风险: 对复杂公式区域仍存在识别缺失，影响深度推理。
- 结论: 该方法体现的是“性能-成本-鲁棒性”之间的再平衡，而非无代价提升。
```

## 23. ext_v1_0023

- task_type: `experiment_interpretation`
- source_case_id: `ext_case_006`
- split: `external_test`

### instruction

```text
请用“结论-原因-边界”解释实验结果，并给出后续验证建议。
```

### input

```text
论文标题: Noise-Robust OCR-to-Reasoning Pipeline for Scanned Papers
研究问题: 扫描版论文 OCR 噪声高，导致后续问答链路错误累积。
核心方法: 先进行版面纠错与术语恢复，再做结构化检索与答案生成的两阶段推理。
对比基线: Direct OCR text QA
实验结果: 在 ScanPaperQA 数据上，端到端准确率提升 8.4%，幻觉率下降 22%。
局限性: 对复杂公式区域仍存在识别缺失，影响深度推理。
```

### output

```text
结论: “在 ScanPaperQA 数据上，端到端准确率提升 8.4%，幻觉率下降 22%。”说明该方法在目标任务上具有可观收益。
原因: 收益主要来自“先进行版面纠错与术语恢复，再做结构化检索与答案生成的两阶段推理。”，其机制上更直接缓解了“扫描版论文 OCR 噪声高，导致后续问答链路错误累积。”。
边界: “对复杂公式区域仍存在识别缺失，影响深度推理。”提示该方法在特定场景下可能退化。
建议: 进一步补充跨域实验与资源受限条件下的稳定性验证。
```

## 24. ext_v1_0024

- task_type: `defense_followup`
- source_case_id: `ext_case_006`
- split: `external_test`

### instruction

```text
请模拟答辩追问，给出 3 组高质量问答，聚焦创新性、证据充分性和局限改进。
```

### input

```text
论文标题: Noise-Robust OCR-to-Reasoning Pipeline for Scanned Papers
研究问题: 扫描版论文 OCR 噪声高，导致后续问答链路错误累积。
核心方法: 先进行版面纠错与术语恢复，再做结构化检索与答案生成的两阶段推理。
对比基线: Direct OCR text QA
实验结果: 在 ScanPaperQA 数据上，端到端准确率提升 8.4%，幻觉率下降 22%。
局限性: 对复杂公式区域仍存在识别缺失，影响深度推理。
```

### output

```text
Q1: 你相对基线的真正创新是什么？
A1: 创新点在于“先进行版面纠错与术语恢复，再做结构化检索与答案生成的两阶段推理。”，它不是简单叠加模块，而是直接针对“扫描版论文 OCR 噪声高，导致后续问答链路错误累积。”的机制级改造。

Q2: 你的实验是否足以支撑结论？
A2: 从结果“在 ScanPaperQA 数据上，端到端准确率提升 8.4%，幻觉率下降 22%。”看，收益方向明确；但仍需更多跨场景验证以增强结论外推性。

Q3: 已知局限是什么，下一步怎么改？
A3: 当前主要局限是“对复杂公式区域仍存在识别缺失，影响深度推理。”。下一步应优先做失效场景分析与针对性鲁棒性增强。
```

## 25. ext_v1_0025

- task_type: `contribution_extraction`
- source_case_id: `ext_case_007`
- split: `external_test`

### instruction

```text
请提炼该工作最关键的三点贡献，要求分别覆盖问题、方法创新和结果价值。
```

### input

```text
论文标题: Evidence Graph Clustering for Retrieval Compression
研究问题: 多文档检索返回证据冗余严重，占用上下文窗口并干扰推理。
核心方法: 将候选证据构建为相似度图，聚类后仅保留中心证据与关键差异证据。
对比基线: Top-k truncation, MMR reranking
实验结果: 在 MultiDoc-Reason 基准上，证据冗余降低 35%，答案一致性提升 6.1%。
局限性: 聚类阈值敏感，阈值设置不当会丢失少量关键边角证据。
```

### output

```text
核心贡献可归纳为三点:
1) 问题导向: 聚焦“多文档检索返回证据冗余严重，占用上下文窗口并干扰推理。”这一高频痛点，并给出可落地方案。
2) 方法创新: 采用“将候选证据构建为相似度图，聚类后仅保留中心证据与关键差异证据。”，在信息利用效率上优于常规路径。
3) 结果价值: 相比“Top-k truncation, MMR reranking”，实验显示“在 MultiDoc-Reason 基准上，证据冗余降低 35%，答案一致性提升 6.1%。”。
同时需注意作者给出的边界条件“聚类阈值敏感，阈值设置不当会丢失少量关键边角证据。”。
```

## 26. ext_v1_0026

- task_type: `method_comparison`
- source_case_id: `ext_case_007`
- split: `external_test`

### instruction

```text
请做结构化方法对比，说明新方法为何更优，以及代价和风险。
```

### input

```text
论文标题: Evidence Graph Clustering for Retrieval Compression
研究问题: 多文档检索返回证据冗余严重，占用上下文窗口并干扰推理。
核心方法: 将候选证据构建为相似度图，聚类后仅保留中心证据与关键差异证据。
对比基线: Top-k truncation, MMR reranking
实验结果: 在 MultiDoc-Reason 基准上，证据冗余降低 35%，答案一致性提升 6.1%。
局限性: 聚类阈值敏感，阈值设置不当会丢失少量关键边角证据。
```

### output

```text
方法对比如下:
- 对比对象: Top-k truncation, MMR reranking
- 新方法机制: 将候选证据构建为相似度图，聚类后仅保留中心证据与关键差异证据。
- 主要优势: 对目标瓶颈更有针对性，通常能提高有效证据利用率和推理稳定性。
- 量化结果: 在 MultiDoc-Reason 基准上，证据冗余降低 35%，答案一致性提升 6.1%。
- 代价与风险: 聚类阈值敏感，阈值设置不当会丢失少量关键边角证据。
- 结论: 该方法体现的是“性能-成本-鲁棒性”之间的再平衡，而非无代价提升。
```

## 27. ext_v1_0027

- task_type: `experiment_interpretation`
- source_case_id: `ext_case_007`
- split: `external_test`

### instruction

```text
请用“结论-原因-边界”解释实验结果，并给出后续验证建议。
```

### input

```text
论文标题: Evidence Graph Clustering for Retrieval Compression
研究问题: 多文档检索返回证据冗余严重，占用上下文窗口并干扰推理。
核心方法: 将候选证据构建为相似度图，聚类后仅保留中心证据与关键差异证据。
对比基线: Top-k truncation, MMR reranking
实验结果: 在 MultiDoc-Reason 基准上，证据冗余降低 35%，答案一致性提升 6.1%。
局限性: 聚类阈值敏感，阈值设置不当会丢失少量关键边角证据。
```

### output

```text
结论: “在 MultiDoc-Reason 基准上，证据冗余降低 35%，答案一致性提升 6.1%。”说明该方法在目标任务上具有可观收益。
原因: 收益主要来自“将候选证据构建为相似度图，聚类后仅保留中心证据与关键差异证据。”，其机制上更直接缓解了“多文档检索返回证据冗余严重，占用上下文窗口并干扰推理。”。
边界: “聚类阈值敏感，阈值设置不当会丢失少量关键边角证据。”提示该方法在特定场景下可能退化。
建议: 进一步补充跨域实验与资源受限条件下的稳定性验证。
```

## 28. ext_v1_0028

- task_type: `defense_followup`
- source_case_id: `ext_case_007`
- split: `external_test`

### instruction

```text
请模拟答辩追问，给出 3 组高质量问答，聚焦创新性、证据充分性和局限改进。
```

### input

```text
论文标题: Evidence Graph Clustering for Retrieval Compression
研究问题: 多文档检索返回证据冗余严重，占用上下文窗口并干扰推理。
核心方法: 将候选证据构建为相似度图，聚类后仅保留中心证据与关键差异证据。
对比基线: Top-k truncation, MMR reranking
实验结果: 在 MultiDoc-Reason 基准上，证据冗余降低 35%，答案一致性提升 6.1%。
局限性: 聚类阈值敏感，阈值设置不当会丢失少量关键边角证据。
```

### output

```text
Q1: 你相对基线的真正创新是什么？
A1: 创新点在于“将候选证据构建为相似度图，聚类后仅保留中心证据与关键差异证据。”，它不是简单叠加模块，而是直接针对“多文档检索返回证据冗余严重，占用上下文窗口并干扰推理。”的机制级改造。

Q2: 你的实验是否足以支撑结论？
A2: 从结果“在 MultiDoc-Reason 基准上，证据冗余降低 35%，答案一致性提升 6.1%。”看，收益方向明确；但仍需更多跨场景验证以增强结论外推性。

Q3: 已知局限是什么，下一步怎么改？
A3: 当前主要局限是“聚类阈值敏感，阈值设置不当会丢失少量关键边角证据。”。下一步应优先做失效场景分析与针对性鲁棒性增强。
```

## 29. ext_v1_0029

- task_type: `contribution_extraction`
- source_case_id: `ext_case_008`
- split: `external_test`

### instruction

```text
请提炼该工作最关键的三点贡献，要求分别覆盖问题、方法创新和结果价值。
```

### input

```text
论文标题: Counterexample Mining for Safety Claim Verification
研究问题: 安全性相关论文常给出强结论，但反例覆盖不足导致结论泛化风险高。
核心方法: 自动挖掘条件反例并执行对抗验证，报告结论成立边界与失效场景。
对比基线: Claim-only verification
实验结果: 在 SafetyClaim-ZH 集合上，虚高结论检出率提升 14.7%。
局限性: 反例生成质量依赖检索语料，低资源领域覆盖仍不足。
```

### output

```text
核心贡献可归纳为三点:
1) 问题导向: 聚焦“安全性相关论文常给出强结论，但反例覆盖不足导致结论泛化风险高。”这一高频痛点，并给出可落地方案。
2) 方法创新: 采用“自动挖掘条件反例并执行对抗验证，报告结论成立边界与失效场景。”，在信息利用效率上优于常规路径。
3) 结果价值: 相比“Claim-only verification”，实验显示“在 SafetyClaim-ZH 集合上，虚高结论检出率提升 14.7%。”。
同时需注意作者给出的边界条件“反例生成质量依赖检索语料，低资源领域覆盖仍不足。”。
```

## 30. ext_v1_0030

- task_type: `method_comparison`
- source_case_id: `ext_case_008`
- split: `external_test`

### instruction

```text
请做结构化方法对比，说明新方法为何更优，以及代价和风险。
```

### input

```text
论文标题: Counterexample Mining for Safety Claim Verification
研究问题: 安全性相关论文常给出强结论，但反例覆盖不足导致结论泛化风险高。
核心方法: 自动挖掘条件反例并执行对抗验证，报告结论成立边界与失效场景。
对比基线: Claim-only verification
实验结果: 在 SafetyClaim-ZH 集合上，虚高结论检出率提升 14.7%。
局限性: 反例生成质量依赖检索语料，低资源领域覆盖仍不足。
```

### output

```text
方法对比如下:
- 对比对象: Claim-only verification
- 新方法机制: 自动挖掘条件反例并执行对抗验证，报告结论成立边界与失效场景。
- 主要优势: 对目标瓶颈更有针对性，通常能提高有效证据利用率和推理稳定性。
- 量化结果: 在 SafetyClaim-ZH 集合上，虚高结论检出率提升 14.7%。
- 代价与风险: 反例生成质量依赖检索语料，低资源领域覆盖仍不足。
- 结论: 该方法体现的是“性能-成本-鲁棒性”之间的再平衡，而非无代价提升。
```

## 31. ext_v1_0031

- task_type: `experiment_interpretation`
- source_case_id: `ext_case_008`
- split: `external_test`

### instruction

```text
请用“结论-原因-边界”解释实验结果，并给出后续验证建议。
```

### input

```text
论文标题: Counterexample Mining for Safety Claim Verification
研究问题: 安全性相关论文常给出强结论，但反例覆盖不足导致结论泛化风险高。
核心方法: 自动挖掘条件反例并执行对抗验证，报告结论成立边界与失效场景。
对比基线: Claim-only verification
实验结果: 在 SafetyClaim-ZH 集合上，虚高结论检出率提升 14.7%。
局限性: 反例生成质量依赖检索语料，低资源领域覆盖仍不足。
```

### output

```text
结论: “在 SafetyClaim-ZH 集合上，虚高结论检出率提升 14.7%。”说明该方法在目标任务上具有可观收益。
原因: 收益主要来自“自动挖掘条件反例并执行对抗验证，报告结论成立边界与失效场景。”，其机制上更直接缓解了“安全性相关论文常给出强结论，但反例覆盖不足导致结论泛化风险高。”。
边界: “反例生成质量依赖检索语料，低资源领域覆盖仍不足。”提示该方法在特定场景下可能退化。
建议: 进一步补充跨域实验与资源受限条件下的稳定性验证。
```

## 32. ext_v1_0032

- task_type: `defense_followup`
- source_case_id: `ext_case_008`
- split: `external_test`

### instruction

```text
请模拟答辩追问，给出 3 组高质量问答，聚焦创新性、证据充分性和局限改进。
```

### input

```text
论文标题: Counterexample Mining for Safety Claim Verification
研究问题: 安全性相关论文常给出强结论，但反例覆盖不足导致结论泛化风险高。
核心方法: 自动挖掘条件反例并执行对抗验证，报告结论成立边界与失效场景。
对比基线: Claim-only verification
实验结果: 在 SafetyClaim-ZH 集合上，虚高结论检出率提升 14.7%。
局限性: 反例生成质量依赖检索语料，低资源领域覆盖仍不足。
```

### output

```text
Q1: 你相对基线的真正创新是什么？
A1: 创新点在于“自动挖掘条件反例并执行对抗验证，报告结论成立边界与失效场景。”，它不是简单叠加模块，而是直接针对“安全性相关论文常给出强结论，但反例覆盖不足导致结论泛化风险高。”的机制级改造。

Q2: 你的实验是否足以支撑结论？
A2: 从结果“在 SafetyClaim-ZH 集合上，虚高结论检出率提升 14.7%。”看，收益方向明确；但仍需更多跨场景验证以增强结论外推性。

Q3: 已知局限是什么，下一步怎么改？
A3: 当前主要局限是“反例生成质量依赖检索语料，低资源领域覆盖仍不足。”。下一步应优先做失效场景分析与针对性鲁棒性增强。
```
