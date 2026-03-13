#!/usr/bin/env bash
set -euo pipefail

# ===============================
# Day 1 server bootstrap script
# Ubuntu + TITAN RTX 24GB
# ===============================

PROJECT_NAME="paper_assistant_ft"
PROJECT_DIR="$HOME/${PROJECT_NAME}"
CONDA_ENV="paper_ft"
PYTHON_VER="3.10"

echo "[1/8] System info"
uname -a
nvidia-smi

echo "[2/8] Ensure project dir exists"
mkdir -p "${PROJECT_DIR}"
cd "${PROJECT_DIR}"

echo "[3/8] Init conda (if needed)"
if ! command -v conda >/dev/null 2>&1; then
  echo "conda not found. Please install Miniconda first."
  exit 1
fi

echo "[4/8] Create/activate conda env"
source "$(conda info --base)/etc/profile.d/conda.sh"
if conda env list | awk '{print $1}' | grep -qx "${CONDA_ENV}"; then
  echo "Conda env ${CONDA_ENV} already exists."
else
  conda create -y -n "${CONDA_ENV}" "python=${PYTHON_VER}"
fi
conda activate "${CONDA_ENV}"

echo "[5/8] Upgrade pip and basic tools"
python -m pip install --upgrade pip wheel setuptools

echo "[6/8] Install PyTorch (CUDA 12.1)"
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo "[7/8] Install training stack"
pip install "transformers>=4.46.0" "datasets>=2.20.0" "accelerate>=0.33.0" \
  "peft>=0.12.0" "trl>=0.9.6" "deepspeed>=0.15.0" "sentencepiece" "jieba" \
  "scikit-learn" "tensorboard" "evaluate"

echo "[8/8] Install LLaMA-Factory"
if [ ! -d "LLaMA-Factory" ]; then
  git clone https://github.com/hiyouga/LLaMA-Factory.git
fi
cd LLaMA-Factory
pip install -e ".[torch,metrics]"

echo "Bootstrap done."
python -V
python -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())"
llamafactory-cli version || true
