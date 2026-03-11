# 数据准备分支（Data Preparation）

这个目录专门记录“原始 case 如何变成训练样本”的过程说明。

## 文件导航

- `case_to_sample_mapping_case004.md`：
  - 用 `case_004` 做完整一对一映射讲解
  - 解释每个字段怎么进入 `instruction/input/output`
  - 说明哪些内容是直接拷贝，哪些是模板生成

## 你后续怎么用这个分支

1. 先看映射文档，理解数据生成逻辑。
2. 再改 `data/raw/paper_cases_v1.json` 的某条 case。
3. 运行 `python scripts/build_dataset_v1.py` 重建数据。
4. 在 `train_v1_readable.md` 中验证映射是否符合预期。

## Case测试日志（新增）
- case_test_log.md：记录每次 case 修改及其在 train/val 样本中的变化。
