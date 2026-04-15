# AGENTS.md

本文件定义 Codex 或其他自动化助手在本仓库中工作时必须遵守的项目约束。

## 项目说明

本项目是一个基于 **Qwen2.5-VL-3B-Instruct** 的本地多模态文档/图表理解与结构化抽取系统，面向文档截图、图表页面、网页/软件界面截图等视觉输入，提供：

- 单图命令行推理
- 文档问答、图表问答、UI 截图理解
- 字段抽取与结构化 JSON 输出
- 批量推理与基础评测
- 本地 Gradio Demo
- 后续 LoRA/QLoRA 微调路线

本仓库的优先目标是：**工程化整理、GitHub 开源发布、项目文档完善和后续持续迭代**。

## 当前进度

已完成：

- 项目基础结构
- 依赖文件
- 本地推理代码骨架
- CLI 推理入口
- Gradio Demo 入口
- prompt 模板
- 示例数据格式
- 数据转换工具
- 批量推理与基础评测脚本
- GitHub 发布所需基础文档

正在进行：

- 单图真实样例测试
- Demo 接入和脱敏截图整理
- 结构化 JSON 输出稳定性优化

后续计划：

- 自建数据集扩充
- LoRA/QLoRA 微调
- 微调前后指标对比
- 更多公开脱敏示例和项目说明文档

## Codex 工作规则

1. 不许虚构结果。
   - 不得声称已经完成 LoRA/QLoRA 微调。
   - 不得编造准确率、F1、字段抽取提升幅度、性能指标或线上部署结果。
   - README、文档和注释必须明确区分“已完成 / 正在进行 / 后续计划”。

2. 不许上传或引入敏感/大体积内容。
   - 不提交 `.venv/`。
   - 不提交 Hugging Face 缓存。
   - 不提交模型权重、checkpoint、LoRA adapter。
   - 不提交日志、运行输出、wandb/runs/tensorboard 等实验追踪目录。
   - 不提交私密截图、原始文档、PDF、个人数据或业务数据。

3. 优先保持仓库适合公开 GitHub 发布。
   - README 应让读者快速理解项目价值。
   - 文档应突出本地部署、多模态输入、结构化输出、Demo 工程化和后续训练路线。
   - 真实图片必须先脱敏，公开截图应放入 `docs/screenshots/`。

4. 不做无关的大规模重构。
   - 优先做仓库工程化、文档、启动说明、脚本修复和小范围可验证改动。
   - 未经用户确认，不重写核心推理流程。
   - 遇到删除 `.venv/`、`transformers/`、数据文件、输出结果等风险操作时，先暂停并提醒用户。

5. 使用 WSL2 / Ubuntu 作为主要开发语境。
   - README 和脚本说明优先使用 Linux/WSL 命令。
   - Windows 脚本可以保留为辅助入口，但不要作为主路径。

## 发布边界

可以进入 GitHub：

- `src/`
- `tools/`
- `scripts/`
- `configs/`
- `data/examples/`
- `docs/`
- `README.md`
- `.gitignore`
- `AGENTS.md`
- `LICENSE`
- requirements 文件

不应进入 GitHub：

- `.venv/`
- `transformers/`
- `outputs/` 中的具体结果文件
- `data/images/` 中的真实私有截图
- `data/raw/` 中的原始数据
- `data/processed/` 中的生成数据
- 模型权重、checkpoint、缓存、日志和临时文件
