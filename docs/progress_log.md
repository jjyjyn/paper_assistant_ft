# 过程记录（Progress Log）

## 2026-03-10（Day 1）

### 今日目标

- 按既定路线启动项目并完成 Day 1
- 建立过程记录体系，保证后续可复盘、可面试讲述
- 跑通服务器链路并验证训练前置条件

### 今日已完成

1. 本地仓库与文档
- 完成 `docs/` 三文档初始化与持续更新
- 完成 `README.md` 工作流与目录说明更新
- 新增脚本：
  - `scripts/server_day1_init.sh`
  - `scripts/sync_to_server.ps1`

2. 本地-服务器同步
- 由于服务器访问 GitHub 受限，采用本地到服务器 bare repo 的 Git 同步方案
- 已可在服务器 `git pull` 到最新代码

3. 服务器环境
- 已创建并使用 `paper_ft` 环境
- `llamafactory-cli` 可运行
- 依赖冲突已处理，`python -m pip check` 通过
- CUDA 验证曾出现 `True`，可识别 `NVIDIA TITAN RTX`

4. 网络与模型下载
- HF 不可直连时改用 ModelScope 下载模型
- 已完成 `Qwen2.5-3B-Instruct` 本地路径下载

### 关键问题与结论

- 问题 1：学校服务器外网/证书策略复杂，安装阶段反复失败
  - 处理：校园网认证 + 镜像/路径调整

- 问题 2：GPU 节点出现不稳定（CUDA 调用在最后步骤卡死）
  - 现象：最小张量命令偶发卡死、会话僵住、`nvidia-smi` 出现 `ERR!`
  - 结论：当前节点不适合直接开长训练

### 明确决策

- Day 1 收尾完成
- Day 2 优先推进“数据与配置”，不等待 GPU 完全恢复
- 若明日节点仍不稳，直接租用 `4090 24GB` 节点继续执行（见 `docs/rental_server_guide.md`）

### 明日待办（Day 2）

1. 完成四类任务统一 schema（instruction/input/output）
2. 产出 v0 数据集（80-150 条）
3. 新增数据构建和校验脚本
4. 完成训练配置草案与 smoke run 命令（短步数）
