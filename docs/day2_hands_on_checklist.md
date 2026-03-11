# Day 2 亲手执行清单（打卡版）

## 必做（今天）

- [ ] `python scripts/build_dataset_v1.py`
- [ ] `python scripts/check_dataset_v1.py`
- [ ] 查看 `data/processed/train_v1.jsonl` 前 5 条
- [ ] 查看 `data/processed/val_v1.jsonl` 前 5 条
- [ ] 手工修改至少 3 条样本（不同任务类型）
- [ ] 在 `docs/progress_log.md` 记录：
  - 执行命令
  - 发现的问题
  - 你做的修改
  - 当前结论

## 加分（今天）

- [ ] 给 `build_dataset_v1.py` 增加参数：`--max_cases`
- [ ] 把抽检结果汇总成 5 条“常见错误模式”
- [ ] 在 `docs/interview_notes_categorized.md` 增加 3 条“老师追问-回答”

## 明日训练前（租机后）

- [ ] 执行 `bash scripts/server_rental_init.sh`
- [ ] 验证 `torch.cuda.is_available() == True`
- [ ] 执行 `bash scripts/run_train_smoke.sh`
- [ ] 记录首轮训练的 loss/log 路径
