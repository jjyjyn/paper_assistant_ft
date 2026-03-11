# 环境配置与踩坑记录（Phase 3）

> 这份文档不是“安装说明书”而已，而是这次真实环境搭建过程的复盘。你后面给老师讲项目时，环境这一段就靠它。

## 1. 这一步在项目里解决什么问题

- 把“本地能写代码”变成“服务器能稳定开训”
- 把“临时跑通一次”变成“下次还能复现”
- 把“遇到报错慌张排查”变成“知道每类错误属于哪一层问题”

## 2. 我们这次实际采用的环境方案

### 2.1 服务器选择

- 平台：AutoDL
- 地区：北京 B 区
- GPU：`RTX 4090 24GB`
- 计费方式：按量计费
- 存储：
  - 系统盘：30GB
  - 数据盘：70GB（含扩容）

### 2.2 为什么这么选

- `4090 24GB` 对 `Qwen3-4B-Instruct + LoRA SFT` 足够
- 单卡成本低，适合先 smoke 再 full 的实验节奏
- 北京区对本地登录、文件同步更方便

### 2.3 镜像选择

- 基础镜像：`Miniconda / conda3 / Python 3.10 / Ubuntu 22.04`

原因：
- 干净，冲突少
- 后续依赖自己装，可控性高
- Python 3.10 对当前工具链兼容性较稳

## 3. 无卡模式和有卡模式怎么分工

### 无卡模式适合做什么

- 拉代码
- 重建 conda 环境
- 安装 Python 依赖
- 运行数据检查脚本
- 下载模型文件

### 无卡模式不该做什么

- `run_train_smoke.sh`
- `run_train_full.sh`
- 任何依赖真实 GPU 的训练命令

### 为什么这样分工

- 无卡模式更便宜
- 环境安装主要消耗的是网络和磁盘，不一定需要 GPU
- 训练才是真正消耗实例费用的部分

## 4. 这次真实执行的环境命令

```bash
cd ~/paper_assistant_ft
source "$(conda info --base)/etc/profile.d/conda.sh"

conda deactivate || true
conda env remove -n paper_ft -y || true
conda create -y -n paper_ft python=3.10
conda activate paper_ft
python -m pip install -U pip wheel setuptools

python -m pip install --no-cache-dir \
  torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 \
  --index-url https://download.pytorch.org/whl/cu121

python -m pip install --no-cache-dir \
  "llamafactory==0.9.3" \
  "transformers==4.52.4" \
  "tokenizers==0.21.1" \
  "huggingface_hub==0.36.2" \
  "datasets>=2.20.0" "accelerate>=0.33.0" \
  "peft>=0.12.0" "trl>=0.9.6" \
  sentencepiece jieba scikit-learn tensorboard evaluate
```

## 5. 最终固定版本（这次已经验证过）

- `torch==2.4.1+cu121`
- `torchvision==0.19.1+cu121`
- `transformers==4.52.4`
- `tokenizers==0.21.1`
- `huggingface_hub==0.36.2`
- `llamafactory==0.9.3`

这组版本是当前项目的“已验证组合”。没有明确理由不要随便升版本。

## 6. 这次真实遇到的错误，以及怎么定位

### 6.1 `tmux: command not found`

现象：
- 想开后台会话跑训练，但系统没装 `tmux`

原因：
- Ubuntu 最小镜像默认不带这个工具

处理：
```bash
apt-get update
apt-get install -y tmux
```

结论：
- 这是系统层缺工具，不是训练框架问题

### 6.2 `Repo id must be in the form ... '/root/models/Qwen/Qwen3-4B-Instruct'`

现象：
- LLaMA-Factory 启动时把本地路径当成 HuggingFace repo id 解析

原因：
- `MODEL_PATH` 指向了一个不存在的目录
- 当本地目录不存在时，`transformers` 会尝试按远端 repo 处理

处理：
- 先用 `find` 或 `ls` 确认模型目录真实存在
- 再设置 `export MODEL_PATH=...`

结论：
- 这类问题属于“路径层”错误，先验证文件是否存在，再怀疑框架

### 6.3 `huggingface-hub>=0.30.0,<1.0 is required ... but found 1.6.0`

现象：
- `transformers` 与 `huggingface_hub` 版本不兼容

原因：
- 环境里某次升级把 `huggingface_hub` 提到了 1.x

处理：
- 重建环境
- 钉住兼容版本，而不是在坏环境上继续打补丁

结论：
- 当核心依赖链乱掉时，重建环境比逐个修补更稳

### 6.4 `tokenizers` / `transformers` 与 `llamafactory` 版本冲突

现象：
- `pip` 安装成功，但后续运行时仍报依赖不兼容

原因：
- `pip` 解析器不会总是帮你回退到最适合的组合
- 你手动升级过某些包后，依赖树已经偏离 LLaMA-Factory 官方兼容范围

处理：
- 明确写死版本，不使用“最新即可”的策略

结论：
- 训练环境更适合“版本钉死”，不适合“全家桶升级到最新”

### 6.5 `RuntimeError: operator torchvision::nms does not exist`

现象：
- 导入链在 `torchvision` 处崩溃

原因：
- `torch` 和 `torchvision` 不是同一套兼容版本
- 旧环境残留包也可能导致混装

处理：
- 删除旧 conda 环境
- 用同一套 CUDA wheel 重装 `torch/torchvision/torchaudio`

结论：
- 这类错误属于“底层二进制包不匹配”，继续在旧环境里修价值不高

## 7. 环境验证怎么做

### 7.1 无卡模式验证

```bash
python - <<'PY'
import torch, torchvision, transformers, tokenizers, huggingface_hub
print("torch:", torch.__version__)
print("torchvision:", torchvision.__version__)
print("transformers:", transformers.__version__)
print("tokenizers:", tokenizers.__version__)
print("huggingface_hub:", huggingface_hub.__version__)
print("cuda:", torch.cuda.is_available())
PY
```

预期：
- 版本和上面固定版本一致
- `cuda: False` 是正常的，因为当前是无卡模式

### 7.2 训练前验证

```bash
python scripts/check_dataset_v1.py
python scripts/check_external_eval_v1.py
```

预期：
- `Dataset check passed.`
- `External eval check passed.`

### 7.3 GPU 模式验证

```bash
python - <<'PY'
import torch
print("cuda:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("gpu:", torch.cuda.get_device_name(0))
PY
```

预期：
- `cuda: True`
- 能打印出 `RTX 4090`

## 8. 明天开机后的最短流程

```bash
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate paper_ft

python - <<'PY'
import torch
print("cuda:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("gpu:", torch.cuda.get_device_name(0))
PY

cd ~/paper_assistant_ft
export MODEL_PATH=/root/autodl-tmp/models/Qwen/Qwen3-4B-Instruct
bash scripts/run_train_smoke.sh
```

## 9. 你给老师讲这一段时可以怎么说

- “我没有把环境安装当成机械步骤，而是把它当成工程链路验证的一部分。”
- “这次我实际遇到了模型路径错误、依赖版本冲突、`torchvision` 二进制不匹配等问题，最后通过重建 conda 环境并钉住兼容版本解决。”
- “我把无卡模式和有卡模式分开使用，先低成本完成依赖安装和数据检查，再切回 GPU 跑训练，这样成本更可控。”
