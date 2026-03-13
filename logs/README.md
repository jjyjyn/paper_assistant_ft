# logs 目录说明

`logs/` 用来放运行过程中的原始日志。

## 1. 适合放什么

- 训练日志
- 评测执行日志
- 报错日志
- 临时排查日志

## 2. 不适合放什么

- 最终结论
- 面试复盘
- 项目计划

这些内容应该回写到：

- `docs/00_meta/progress_log.md`
- `docs/00_meta/project_plan.md`
- `docs/03_interview/interview_notes_quick.md`

## 3. 版本控制策略

- `logs/` 默认忽略，不自动进 Git
- 只有这份 `logs/README.md` 会被保留，用来说明目录用途

## 4. 使用建议

- 运行时可以按日期或任务名建子目录
- 真正重要的结论不要只留在日志里，必须回写到 `docs/`

