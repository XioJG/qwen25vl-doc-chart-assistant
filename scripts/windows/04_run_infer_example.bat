@echo off
setlocal
call .venv\Scriptsctivate

python -m src.inference_cli ^
  --model-name Qwen/Qwen2.5-VL-3B-Instruct ^
  --bits 4 ^
  --image data\images\your_image.png ^
  --task structured_extraction ^
  --question "请提取图中的关键字段，并以 JSON 输出。" ^
  --save outputs\example_prediction.json
