# 过程记录（Progress Log）

## 2026-03-10（Day 1）

### 今日目标

- 按既定路线启动项目：LLaMA-Factory + Qwen + LoRA SFT
- 完成本地仓库文档体系与脚本初始化
- 打通服务器执行链路，验证是否可进入训练阶段

### 本地侧完成事项

- 补齐并更新目录与说明文档
- 新建并初始化：
  - `docs/project_plan.md`
  - `docs/progress_log.md`
  - `docs/interview_notes.md`
- 新建脚本：
  - `scripts/server_day1_init.sh`
  - `scripts/sync_to_server.ps1`
- 更新 `README.md`，明确固定工作流：本地开发 + 服务器执行 + 手动同步

### 服务器侧执行过程（关键节点）

1. 代码同步
- 由于服务器无法正常访问 GitHub HTTPS/SSH，改为本地到服务器 bare repo 的 Git 同步方式
- 成功完成：服务器 `~/paper_assistant_ft` 可 `git pull` 到最新代码

2. 网络连通排查
- 初期失败现象：
  - `github.com` SSL 证书不匹配
  - `conda/pip` 拉包失败
  - `huggingface.co` 不可达
- 发现并执行校园网认证后，外网连通性显著改善（至少对 pypi 可访问）

3. 环境与依赖安装
- 创建并激活 `paper_ft` 环境
- 安装并验证 `llamafactory-cli` 可用
- 由于驱动较旧（510.39.01 / CUDA 11.6），将 PyTorch 栈调整为：
  - `torch==1.13.1+cu116`
  - `torchvision==0.14.1+cu116`
  - `torchaudio==0.13.1+cu116`
- `pip check` 通过：`No broken requirements found`

4. GPU状态验证
- 一度验证成功：`torch.cuda.is_available() == True` 且识别 `NVIDIA TITAN RTX`
- 但后续最小 CUDA 张量命令出现“最后一步卡死”现象，`Ctrl+C` 与 `kill` 不稳定
- 同时观察到 `nvidia-smi` 长期出现 `ERR!` 字段，推断当前节点 GPU 运行状态不稳定

### 今日关键命令（节选）

```bash
# 服务器环境验证
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
llamafactory-cli version
python -m pip check

# 网络排查
curl -I -m 10 https://pypi.org/simple/transformers/
curl -I -m 10 http://mirrors.ustc.edu.cn/anaconda/pkgs/main/linux-64/repodata.json

# 模型下载（ModelScope）
python -c "from modelscope.hub.snapshot_download import snapshot_download; print(snapshot_download('Qwen/Qwen2.5-3B-Instruct', cache_dir='/home/jingyuning/models'))"
```

### 今日结论

- Day 1 的“仓库与环境搭建”目标基本完成
- 当前唯一阻塞：该节点 GPU 稳定性问题（非项目方案问题）
- 在不更换节点的前提下，建议先推进 Day 2 数据与配置工作，避免等待成本

### 明日计划（Day 2 启动）

- 先完成四类任务的数据 schema 与样本模板
- 产出首版 `train/val` 数据文件与生成脚本
- 训练启动条件：GPU 节点稳定后再执行 LoRA SFT
