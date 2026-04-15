# Docs

本目录用于放置公开展示材料，目标是让面试官能快速理解项目的技术路线、Demo 形态和后续迭代计划。

## 目录结构

```text
docs/
├── README.md
├── architecture.md           # 推理、数据、评测、后续微调的整体流程说明
├── demo_checklist.md         # 面试演示前检查清单
├── screenshots/
│   ├── README.md             # 截图类型与命名规范
│   └── .gitkeep
├── diagrams/
│   ├── README.md             # 流程图/架构图放置说明
│   └── .gitkeep
└── notes/
    └── README.md             # 后续实验、问题记录、面试讲解草稿
```

## 推荐放置内容

- `screenshots/`：脱敏后的 Gradio 页面、CLI 推理输出、结构化 JSON 输出截图。
- `diagrams/`：项目流程图、推理链路图、数据转换与评测流程图。
- `notes/`：面试讲解提纲、实验记录、后续 LoRA/QLoRA 计划。

## 发布边界

不要在 `docs/` 中放入：

- 私密文档截图或业务截图。
- 原始 PDF、Excel、数据集压缩包。
- 模型权重、checkpoint、adapter。
- Hugging Face 缓存或运行日志。

所有公开图片应先脱敏，截图中不要出现真实姓名、账号、地址、token、本地绝对路径或敏感业务数据。
