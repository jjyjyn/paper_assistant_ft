# 过程记录（Progress Log）

## 2026-03-10（Day 1）

### 今日目标

- 按固定路线启动项目，不改题目不改框架
- 补齐文档记录体系
- 准备服务器环境初始化命令

### 本地已完成

- 确认仓库骨架：`configs/`、`scripts/`、`data/`、`logs/`、`outputs/`
- 新增 `docs/` 并创建三份核心文档
- 更新 `README.md`，明确固定技术路线与固定工作流
- 新增 `scripts/server_day1_init.sh`（服务器初始化脚本）
- 新增 `scripts/sync_to_server.ps1`（本地到服务器同步示例）

### 今日使用命令（本地）

```powershell
Get-ChildItem -Force
Get-ChildItem -Recurse -Depth 2 | Select-Object FullName
Get-Content README.md
Get-Content .gitignore
```

### 服务器命令（待执行）

见：`scripts/server_day1_init.sh`

### 报错与处理

- 现象：PowerShell profile 加载受执行策略限制（`profile.ps1` 无法加载）
- 影响：不影响项目文件读写与 git 操作
- 处理：后续命令使用 `-NoProfile` 或在工具调用中关闭 login profile

### 当前结论

- Day 1 的本地侧准备已就绪
- 下一步是在服务器执行初始化脚本并回传日志，进入 Day 2 数据集制作
