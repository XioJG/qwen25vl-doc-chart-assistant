#!/usr/bin/env bash
set -e

python3 -m venv .venv
source .venv/bin/activate

echo "[INFO] Please install the correct CUDA build of PyTorch first."
echo "[INFO] Example:"
echo "pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121"

pip install -r requirements.demo.txt

echo "[OK] setup finished."
