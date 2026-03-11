#!/usr/bin/env bash
set -euo pipefail

# Download the official Qwen3-4B model from ModelScope.
# This is the preferred route on China-network servers where huggingface.co may time out.
# ModelScope controls the final snapshot path, so the script prints the resolved MODEL_PATH.

CACHE_DIR="${CACHE_DIR:-/root/autodl-tmp/modelscope-cache}"
MODEL_ID="${MODEL_ID:-Qwen/Qwen3-4B}"

mkdir -p "${CACHE_DIR}"

conda run -n base python -m pip install -U modelscope
conda run -n base python - <<PY
from modelscope.hub.snapshot_download import snapshot_download

path = snapshot_download("${MODEL_ID}", cache_dir="${CACHE_DIR}")
print(f"MODEL_PATH={path}")
PY
