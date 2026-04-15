#!/usr/bin/env bash
set -e

# 说明：
# 1. 这是给 8GB 左右单卡设备准备的保守示例脚本
# 2. 需要你先克隆 Qwen-VL-Series-Finetune 仓库
# 3. 需要你先准备好 LLaVA 格式数据
# 4. 本脚本优先考虑“能跑通”，不是追求极限效果

export PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
export FT_REPO="${PROJECT_ROOT}/third_party/Qwen-VL-Series-Finetune"

export MODEL_ID="Qwen/Qwen2.5-VL-3B-Instruct"
export DATA_PATH="${PROJECT_ROOT}/data/processed/train.llava.json"
export IMAGE_FOLDER="${PROJECT_ROOT}/data/images"
export EVAL_PATH="${PROJECT_ROOT}/data/processed/val.llava.json"
export OUTPUT_DIR="${PROJECT_ROOT}/outputs/qwen25vl_lora_8gb"

cd "${FT_REPO}"

# 注意：
# - QLoRA + vision 不建议一起开
# - 这里冻结 vision tower 和 merger
# - LoRA 只作用于语言模型，最适合你的笔记本先跑通
bash scripts/finetune_lora.sh   --model_id "${MODEL_ID}"   --data_path "${DATA_PATH}"   --eval_path "${EVAL_PATH}"   --image_folder "${IMAGE_FOLDER}"   --output_dir "${OUTPUT_DIR}"   --num_train_epochs 1   --per_device_train_batch_size 1   --gradient_accumulation_steps 16   --learning_rate 2e-4   --freeze_vision_tower True   --freeze_merger True   --lora_enable True   --vision_lora False   --bits 4   --disable_flash_attn2 True   --use_liger False   --report_to none   --logging_steps 5   --image_resized_width 448   --image_resized_height 448

echo "[OK] training finished or started successfully."
echo "Output dir: ${OUTPUT_DIR}"
