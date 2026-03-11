#!/usr/bin/env bash
set -euo pipefail

# Bootstrap for rental GPU server (e.g., AutoDL RTX 4090 24GB)
# Usage:
#   bash scripts/server_rental_init.sh

PROJECT_NAME="paper_assistant_ft"
PROJECT_DIR="${HOME}/${PROJECT_NAME}"
CONDA_ENV="paper_ft"
PYTHON_VER="3.10"

echo "[1/8] System check"
uname -a
nvidia-smi

echo "[2/8] Ensure project dir"
mkdir -p "${PROJECT_DIR}" "${PROJECT_DIR}/logs" "${PROJECT_DIR}/outputs"
cd "${PROJECT_DIR}"

echo "[3/8] Check conda"
if ! command -v conda >/dev/null 2>&1; then
  echo "conda not found. Install Miniconda first."
  exit 1
fi

echo "[4/8] Create/activate env"
source "$(conda info --base)/etc/profile.d/conda.sh"
if conda env list | awk '{print $1}' | grep -qx "${CONDA_ENV}"; then
  echo "Conda env ${CONDA_ENV} already exists."
else
  conda create -y -n "${CONDA_ENV}" "python=${PYTHON_VER}"
fi
conda activate "${CONDA_ENV}"

echo "[5/8] Upgrade pip tools"
python -m pip install --upgrade pip wheel setuptools

echo "[6/8] Install PyTorch (CUDA 12.1)"
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo "[7/8] Install LLaMA-Factory stack"
python -m pip install "transformers>=4.46.0" "datasets>=2.20.0" "accelerate>=0.33.0" \
  "peft>=0.12.0" "trl>=0.9.6" "sentencepiece" "jieba" "scikit-learn" "tensorboard" "evaluate"
python -m pip install llamafactory

echo "[8/8] Verification"
python - << 'PY'
import torch
print("torch:", torch.__version__)
print("cuda available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("gpu:", torch.cuda.get_device_name(0))
PY
llamafactory-cli version || true

echo "Done. Rental server environment is ready."
