@echo off
setlocal
call .venv\Scriptsctivate

python -m src.app_gradio ^
  --model-name Qwen/Qwen2.5-VL-3B-Instruct ^
  --bits 4 ^
  --max-new-tokens 512 ^
  --temperature 0.1
