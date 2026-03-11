#!/usr/bin/env bash
set -euo pipefail

# Smoke run for Day 2/3
# Run from repo root:
#   bash scripts/run_train_smoke.sh

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate paper_ft

python scripts/check_dataset_v1.py

MODEL_PATH="${MODEL_PATH:-}"
if [[ -z "${MODEL_PATH}" ]]; then
  if [[ -d "${HOME}/models/Qwen/Qwen2___5-3B-Instruct" ]]; then
    MODEL_PATH="${HOME}/models/Qwen/Qwen2___5-3B-Instruct"
  elif [[ -d "${HOME}/models/Qwen/Qwen2.5-3B-Instruct" ]]; then
    MODEL_PATH="${HOME}/models/Qwen/Qwen2.5-3B-Instruct"
  else
    echo "Model path not found."
    echo "Set MODEL_PATH, e.g.:"
    echo "  export MODEL_PATH=${HOME}/models/Qwen/Qwen2___5-3B-Instruct"
    exit 1
  fi
fi

TMP_CONFIG="$(mktemp /tmp/lora_sft_qwen25_3b_v1.XXXX.yaml)"
cp configs/lora_sft_qwen25_3b_v1.yaml "${TMP_CONFIG}"
sed -i "s|^model_name_or_path:.*|model_name_or_path: ${MODEL_PATH}|" "${TMP_CONFIG}"

echo "Start LLaMA-Factory smoke training..."
llamafactory-cli train "${TMP_CONFIG}"

echo "Smoke training finished."
