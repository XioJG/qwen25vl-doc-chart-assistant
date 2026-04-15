# Architecture Notes

本项目当前以本地推理、结构化输出和 Demo 工程化为主线，后续再扩展到 LoRA/QLoRA 微调和指标对比。

## 当前推理链路

```text
image screenshot
    -> prompt template
    -> Qwen2.5-VL-3B-Instruct local inference
    -> raw model answer
    -> optional JSON block parsing
    -> CLI / Gradio / batch output
```

核心文件：

- `src/common.py`：模型加载、量化配置、视觉输入处理、文本生成、JSON 解析。
- `src/prompt_templates.py`：结构化抽取、文档问答、图表问答、UI 理解等任务模板。
- `src/inference_cli.py`：单图命令行推理。
- `src/app_gradio.py`：本地 Gradio Demo。
- `src/batch_infer.py`：simple.jsonl 批量推理。

## 数据与评测链路

```text
simple.jsonl examples
    -> batch inference
    -> predictions jsonl
    -> QA / extraction evaluation
```

核心文件：

- `data/examples/`：可公开的小型示例数据。
- `tools/convert_simple_jsonl_to_llava_json.py`：将 simple.jsonl 转为 LLaVA 风格 JSON。
- `src/eval_qa.py`：文本问答基础评测。
- `src/eval_extraction.py`：结构化字段抽取基础评测。

## 后续微调路线

计划路线：

```text
private desensitized dataset
    -> simple.jsonl
    -> LLaVA-style JSON
    -> QLoRA / LoRA fine-tuning
    -> baseline vs fine-tuned evaluation
```

当前状态：

- 已准备训练数据格式转换工具和训练脚本说明。
- 尚未完成 LoRA/QLoRA 微调结果。
- 尚未报告微调前后指标对比。

## 项目说明重点

- 这不是远程 API 调用项目，而是围绕本地 Qwen2.5-VL-3B 的多模态推理工程。
- 项目已覆盖视觉输入、任务 prompt、结构化 JSON 输出、CLI、Demo、批量推理和基础评测。
- 微调路线已经规划，但结果不夸大，后续会以真实指标补充。
