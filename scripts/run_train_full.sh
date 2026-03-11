#!/usr/bin/env bash
set -euo pipefail

# Full training run for Day 3+
# Run from repo root:
#   bash scripts/run_train_full.sh

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate paper_ft

python scripts/check_dataset_v1.py

MODEL_PATH="${MODEL_PATH:-}"
if [[ -z "${MODEL_PATH}" ]]; then
  if [[ -d "${HOME}/autodl-tmp/models/Qwen/Qwen3-4B" ]]; then
    MODEL_PATH="${HOME}/autodl-tmp/models/Qwen/Qwen3-4B"
  elif [[ -d "${HOME}/models/Qwen/Qwen3-4B" ]]; then
    MODEL_PATH="${HOME}/models/Qwen/Qwen3-4B"
  elif [[ -d "${HOME}/autodl-tmp/models/Qwen/Qwen3___4B" ]]; then
    MODEL_PATH="${HOME}/autodl-tmp/models/Qwen/Qwen3___4B"
  elif [[ -d "${HOME}/models/Qwen/Qwen3___4B" ]]; then
    MODEL_PATH="${HOME}/models/Qwen/Qwen3___4B"
  elif [[ -d "${HOME}/autodl-tmp/models/Qwen/Qwen2___5-3B-Instruct" ]]; then
    MODEL_PATH="${HOME}/autodl-tmp/models/Qwen/Qwen2___5-3B-Instruct"
  elif [[ -d "${HOME}/autodl-tmp/models/Qwen/Qwen2.5-3B-Instruct" ]]; then
    MODEL_PATH="${HOME}/autodl-tmp/models/Qwen/Qwen2.5-3B-Instruct"
  elif [[ -d "${HOME}/models/Qwen/Qwen2___5-3B-Instruct" ]]; then
    MODEL_PATH="${HOME}/models/Qwen/Qwen2___5-3B-Instruct"
  elif [[ -d "${HOME}/models/Qwen/Qwen2.5-3B-Instruct" ]]; then
    MODEL_PATH="${HOME}/models/Qwen/Qwen2.5-3B-Instruct"
  else
    echo "Model path not found."
    echo "Set MODEL_PATH, e.g.:"
    echo "  export MODEL_PATH=${HOME}/autodl-tmp/models/Qwen/Qwen3-4B"
    echo "  # fallback: ${HOME}/models/Qwen/Qwen2___5-3B-Instruct"
    exit 1
  fi
fi

BASE_CONFIG="${BASE_CONFIG:-configs/lora_sft_qwen_v1_full.yaml}"
TMP_CONFIG="$(mktemp /tmp/lora_sft_full.XXXX.yaml)"
cp "${BASE_CONFIG}" "${TMP_CONFIG}"
sed -i "s|^model_name_or_path:.*|model_name_or_path: ${MODEL_PATH}|" "${TMP_CONFIG}"

echo "Using model: ${MODEL_PATH}"
echo "Using base config: ${BASE_CONFIG}"
echo "Start LLaMA-Factory full training..."
llamafactory-cli train "${TMP_CONFIG}"

echo "Full training finished."
