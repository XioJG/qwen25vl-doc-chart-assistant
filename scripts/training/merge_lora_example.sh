#!/usr/bin/env bash
set -e

export PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
export FT_REPO="${PROJECT_ROOT}/third_party/Qwen-VL-Series-Finetune"

cd "${FT_REPO}"

# 这里需要你根据实际训练输出目录修改
bash scripts/merge_lora.sh

echo "[INFO] Please edit scripts/merge_lora.sh inside the external repo to point to your model path."
