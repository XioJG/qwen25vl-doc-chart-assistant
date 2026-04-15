# Demo Checklist

运行项目前，建议按这个清单检查。

## 环境检查

```bash
source .venv/bin/activate
python smoke_test.py
```

确认项：

- Python 环境可以正常进入。
- Qwen2.5-VL-3B-Instruct 模型和 processor 可以加载。
- CUDA / PyTorch 版本与本机环境匹配。

## 单图推理检查

准备一张脱敏截图到 `data/images/`，然后运行：

```bash
python -m src.inference_cli \
  --model-name Qwen/Qwen2.5-VL-3B-Instruct \
  --bits 4 \
  --image data/images/your_public_demo_image.png \
  --task structured_extraction \
  --question "请提取图中的关键字段，并以 JSON 输出。" \
  --save outputs/demo_prediction.json
```

确认项：

- 命令可以运行完成。
- 输出中能看到 prompt 和模型回答。
- 如果模型返回 JSON，`answer_json` 能被解析。

## Gradio Demo 检查

```bash
bash scripts/linux/02_run_demo.sh
```

确认项：

- 浏览器能访问 `http://127.0.0.1:7860`。
- 可以上传脱敏图片。
- 可以切换任务模板。
- 能看到模型原始回答和解析出的 JSON。

## GitHub 发布检查

上传前确认：

- README 中没有虚构微调结果或指标。
- `docs/screenshots/` 中只放脱敏截图。
- `outputs/` 中的运行结果没有被提交。
- `.venv/`、`transformers/`、模型权重、缓存目录没有被提交。

## 项目检查顺序

1. 先看 README 顶部：项目是本地 Qwen2.5-VL 多模态文档/图表理解系统。
2. 再看项目亮点：本地部署、截图理解、结构化 JSON、CLI + Gradio + 评测。
3. 然后打开 `docs/architecture.md`：查看推理链路、数据链路和后续微调路线。
4. 最后查看 `docs/screenshots/` 中的脱敏 Demo 截图。
