# Diagrams

本目录用于放置流程图和架构图，帮助面试官快速理解项目不是零散脚本，而是围绕本地多模态模型推理、结构化输出和后续训练扩展组织起来的工程。

## 推荐图表

1. `inference_pipeline.png`
   - 图片输入
   - prompt template
   - Qwen2.5-VL-3B 本地推理
   - JSON 解析
   - CLI / Gradio / batch output

2. `data_eval_pipeline.png`
   - simple.jsonl
   - LLaVA 格式转换
   - batch inference
   - QA / extraction evaluation

3. `future_lora_plan.png`
   - 私有脱敏数据
   - QLoRA / LoRA 微调
   - baseline vs fine-tuned 评测
   - Demo 更新

## 注意事项

- 图中不要写虚构指标。
- 微调相关内容必须标注为 planned 或 future work。
- 推荐使用简洁流程图，不需要复杂系统架构包装。
