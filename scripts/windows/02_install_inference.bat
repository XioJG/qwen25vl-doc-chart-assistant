@echo off
setlocal
call .venv\Scriptsctivate

echo [INFO] Please make sure you have installed the correct CUDA version of PyTorch first.
echo [INFO] Example:
echo pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

pip install -r requirements.demo.txt

echo [OK] inference/demo dependencies installed.
