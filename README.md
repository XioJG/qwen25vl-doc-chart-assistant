# Qwen2.5-VL-3B 多模态文档/图表理解与结构化抽取系统

基于 **Qwen2.5-VL-3B-Instruct** 的本地多模态项目，用于对文档截图、图表页面、网页/软件界面截图进行图像问答、字段抽取和结构化 JSON 输出，并提供命令行推理与本地 Gradio Demo。

## 项目目标

本项目目标是搭建一个可在本地运行的多模态文档/图表理解系统，而不是只调用远程 API。项目重点体现：

- 本地部署 Qwen2.5-VL-3B-Instruct。
- 处理文档、图表、网页界面截图等视觉输入。
- 通过任务 prompt 实现问答、字段抽取、UI 理解和 JSON 输出。
- 提供 CLI、批量推理、基础评测和 Gradio Demo。
- 为后续 LoRA/QLoRA 微调、基线对比保留清晰工程结构。

## 当前进度

已完成：

- 项目基础目录结构与发布用 `.gitignore`。
- Qwen2.5-VL-3B-Instruct 本地推理代码骨架。
- 单图命令行推理入口：`src/inference_cli.py`。
- Gradio Demo 入口：`src/app_gradio.py`。
- 文档问答、图表问答、UI 理解、结构化抽取等 prompt 模板。
- `simple.jsonl` 示例数据格式。
- simple JSONL 到 LLaVA 格式的转换工具。
- 批量推理脚本和基础 QA / 结构化抽取评测脚本。
- 面向 GitHub 发布的 README、AGENTS、LICENSE 和仓库忽略规则。

正在进行：

- 使用脱敏样例图片跑通真实单图测试。
- 接入和整理 Gradio Demo 运行截图。
- 打磨模型输出到结构化 JSON 的稳定性。
- 整理更适合公开发布的示例输入与示例输出。

后续计划：

- 构建更高质量的私有文档/图表/截图样本集。
- 接入 LoRA/QLoRA 微调流程。
- 完成微调前后评测对比，但目前尚未完成相关实验结果。
- 扩展更多文档类型、图表类型和 UI 截图理解任务。
- 补充脱敏 Demo 截图、流程图和项目说明文档。

## 项目亮点

- **Qwen2.5-VL-3B 本地部署**：围绕开源视觉语言模型搭建本地推理流程，支持 4-bit / 8-bit / 16-bit 推理配置。
- **多模态文档理解场景**：聚焦文档截图、图表页面、网页/软件界面截图，而不是普通图片分类或纯文本任务。
- **结构化 JSON 输出**：通过 prompt 模板约束模型输出，并提供 JSON 块解析逻辑，便于字段抽取和后处理。
- **工程化 Demo**：同时提供命令行推理、批量推理和 Gradio Web Demo，方便调试。
- **可扩展训练路线**：保留 LoRA/QLoRA 微调脚本说明，但明确标注为后续计划，不虚构指标或训练效果。

## 项目文档索引

建议按以下顺序了解项目结构和实现：

1. 先看本 README 的项目目标、当前进度和项目亮点，快速确认项目定位。
2. 再看 [docs/architecture.md](docs/architecture.md)，理解本地推理、数据转换、评测和后续微调链路。
3. 然后看 [src/common.py](src/common.py)、[src/inference_cli.py](src/inference_cli.py)、[src/app_gradio.py](src/app_gradio.py)，确认核心实现不是空壳。
4. 最后看 [docs/screenshots](docs/screenshots) 中后续补充的脱敏 Demo 截图，了解 CLI / Gradio / JSON 输出效果。

## 技术栈

- Python 3.10+
- PyTorch
- Hugging Face Transformers
- Qwen2.5-VL-3B-Instruct
- qwen-vl-utils
- bitsandbytes / accelerate
- Gradio
- WSL2 Ubuntu / Linux shell scripts

## 项目结构

```text
.
├── README.md
├── README_zh.md
├── AGENTS.md
├── LICENSE
├── .gitignore
├── configs/
│   └── app_config.example.yaml
├── data/
│   ├── README.md
│   ├── examples/              # 可公开的小型示例数据
│   ├── images/                # 本地图片，默认忽略，仅保留 .gitkeep
│   ├── raw/                   # 原始私有数据，默认忽略
│   └── processed/             # 中间产物，默认忽略
├── docs/
│   ├── README.md
│   ├── architecture.md        # 推理、数据、评测、微调路线说明
│   ├── demo_checklist.md      # 项目运行前检查清单
│   ├── screenshots/           # 后续放脱敏 Demo 截图
│   ├── diagrams/              # 后续放流程图/架构图
│   └── notes/                 # 后续放实验记录和问题排查笔记
├── outputs/                   # 本地推理输出，默认忽略
├── requirements.inference.txt
├── requirements.demo.txt
├── scripts/
│   ├── linux/                 # WSL2 / Ubuntu 启动脚本
│   ├── windows/               # Windows 辅助脚本
│   └── training/              # 后续 LoRA/QLoRA 路线说明
├── src/
│   ├── common.py              # 模型加载、生成、JSON 解析
│   ├── prompt_templates.py
│   ├── inference_cli.py
│   ├── batch_infer.py
│   ├── eval_qa.py
│   ├── eval_extraction.py
│   └── app_gradio.py
└── tools/
    ├── convert_simple_jsonl_to_llava_json.py
    ├── validate_llava_dataset.py
    ├── make_train_val_split.py
    └── preview_dataset.py
```

## 环境准备

推荐环境：

- Windows 11 + WSL2 Ubuntu
- NVIDIA GPU + CUDA 对应版本 PyTorch
- Python 3.10+

创建虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

先按本机 CUDA 版本安装 PyTorch。以下仅为 CUDA 12.1 示例：

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

安装项目依赖：

```bash
pip install -r requirements.demo.txt
```

首次运行会从 Hugging Face 下载模型。模型权重和 Hugging Face 缓存不应提交到 GitHub。

## 最小运行命令

模型加载 smoke test：

```bash
python smoke_test.py
```

单图命令行推理：

```bash
python -m src.inference_cli \
  --model-name Qwen/Qwen2.5-VL-3B-Instruct \
  --bits 4 \
  --image data/images/your_image.png \
  --task structured_extraction \
  --question "请提取图中的关键字段，并以 JSON 输出。" \
  --save outputs/example_prediction.json
```

启动 Gradio Demo：

```bash
bash scripts/linux/02_run_demo.sh
```

或直接运行：

```bash
python -m src.app_gradio \
  --model-name Qwen/Qwen2.5-VL-3B-Instruct \
  --bits 4 \
  --server-name 127.0.0.1 \
  --server-port 7860
```

访问：

```text
http://127.0.0.1:7860
```

## 示例数据格式

项目内部使用轻量 `simple.jsonl` 格式维护样本：

```json
{
  "id": "demo_001",
  "image": "invoice_001.png",
  "task": "structured_extraction",
  "instruction": "请提取图中发票号码、日期和总金额，并以 JSON 输出。",
  "answer": {
    "invoice_number": "INV-2025-001",
    "date": "2025-03-01",
    "total_amount": "1280.00"
  }
}
```

转换为 LLaVA 格式：

```bash
python tools/convert_simple_jsonl_to_llava_json.py \
  --input data/examples/train.simple.jsonl \
  --output data/processed/train.llava.json
```

## 批量推理与评测

批量推理：

```bash
python -m src.batch_infer \
  --input data/examples/val.simple.jsonl \
  --image-root data/images \
  --output outputs/val_predictions.jsonl \
  --bits 4
```

QA 评测：

```bash
python -m src.eval_qa --predictions outputs/val_predictions.jsonl
```

结构化抽取评测：

```bash
python -m src.eval_extraction --predictions outputs/val_predictions.jsonl
```

## GitHub 发布注意事项

不要提交：

- `.venv/`
- `transformers/` 等本地第三方仓库副本
- Hugging Face 缓存
- 模型权重、checkpoint、LoRA adapter
- 私密截图、PDF、原始数据
- `outputs/` 下的推理结果
- 日志、实验追踪目录、临时文件

## 致谢

- [Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)
- [Qwen2.5-VL Blog](https://qwenlm.github.io/blog/qwen2.5-vl/)
- [Hugging Face Transformers](https://github.com/huggingface/transformers)
- [bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes)
- [Gradio](https://github.com/gradio-app/gradio)
- [Qwen-VL-Series-Finetune](https://github.com/2U1/Qwen-VL-Series-Finetune)
