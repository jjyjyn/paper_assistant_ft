#!/usr/bin/env bash
set -euo pipefail

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate paper_ft

python scripts/check_dataset_v1.py
python scripts/check_external_eval_v1.py

MODEL_PATH="${MODEL_PATH:-}"
if [[ -z "${MODEL_PATH}" ]]; then
  if [[ -d "${HOME}/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B" ]]; then
    MODEL_PATH="${HOME}/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B"
  elif [[ -d "${HOME}/autodl-tmp/models/Qwen/Qwen3-4B" ]]; then
    MODEL_PATH="${HOME}/autodl-tmp/models/Qwen/Qwen3-4B"
  elif [[ -d "${HOME}/models/Qwen/Qwen3-4B" ]]; then
    MODEL_PATH="${HOME}/models/Qwen/Qwen3-4B"
  else
    echo "Model path not found."
    echo "Set MODEL_PATH, e.g.:"
    echo "  export MODEL_PATH=${HOME}/autodl-tmp/modelscope-cache/Qwen/Qwen3-4B"
    exit 1
  fi
fi

ADAPTER_PATH="${ADAPTER_PATH:-outputs/qwen_lora_v1_full}"
DISABLE_THINKING="${DISABLE_THINKING:-0}"
RUN_TAG="${RUN_TAG:-}"
STAMP="$(date +%F_%H%M%S)"
MODE_SUFFIX=""
if [[ "${DISABLE_THINKING}" == "1" ]]; then
  MODE_SUFFIX="_nothink"
fi
OUT_DIR="outputs/evals/qwen_lora_v1_full_${STAMP}${MODE_SUFFIX}"
mkdir -p "${OUT_DIR}"

EXTRA_ARGS=()
if [[ "${DISABLE_THINKING}" == "1" ]]; then
  EXTRA_ARGS+=("--disable-thinking")
fi
if [[ -n "${RUN_TAG}" ]]; then
  EXTRA_ARGS+=("--run-tag" "${RUN_TAG}")
fi

echo "Using model: ${MODEL_PATH}"
echo "Using adapter: ${ADAPTER_PATH}"
echo "Disable thinking: ${DISABLE_THINKING}"
echo "Run tag: ${RUN_TAG:-<none>}"
echo "Saving reports to: ${OUT_DIR}"

python scripts/eval_lora_model.py \
  --base-model "${MODEL_PATH}" \
  --adapter-path "${ADAPTER_PATH}" \
  --dataset data/processed/test_v1.jsonl \
  --output-jsonl "${OUT_DIR}/test_v1_predictions.jsonl" \
  --output-summary "${OUT_DIR}/test_v1_summary.json" \
  --output-md "${OUT_DIR}/test_v1_report.md" \
  "${EXTRA_ARGS[@]}"

python scripts/eval_lora_model.py \
  --base-model "${MODEL_PATH}" \
  --adapter-path "${ADAPTER_PATH}" \
  --dataset data/external_eval/processed/external_eval_v1.jsonl \
  --output-jsonl "${OUT_DIR}/external_eval_v1_predictions.jsonl" \
  --output-summary "${OUT_DIR}/external_eval_v1_summary.json" \
  --output-md "${OUT_DIR}/external_eval_v1_report.md" \
  "${EXTRA_ARGS[@]}"

echo "Evaluation finished."
echo "Reports:"
echo "  ${OUT_DIR}/test_v1_summary.json"
echo "  ${OUT_DIR}/external_eval_v1_summary.json"
