#!/usr/bin/env bash
set -e

mkdir -p third_party
cd third_party

if [ ! -d "Qwen-VL-Series-Finetune" ]; then
  git clone https://github.com/2U1/Qwen-VL-Series-Finetune.git
else
  echo "[INFO] Repo already exists, skipping clone."
fi
