# 训练脚本说明

本目录的脚本默认基于以下开源仓库：

- https://github.com/2U1/Qwen-VL-Series-Finetune

## 推荐理由
这个仓库已经支持：
- Qwen2.5-VL
- LoRA / QLoRA
- LLaVA 格式数据
- LoRA 权重合并
- Gradio WebUI
- 多图 / 视频 / DPO / GRPO（本项目先不建议你在本机做这些）

## 为什么本模板包不自己重写训练器
因为你当前设备更适合：
- 自己掌控项目结构、数据、评测、Demo
- 训练部分复用成熟开源链
- 避免把时间浪费在重新写 VLM Trainer 上

## 8GB 单卡建议
根据该训练仓库 README 的训练说明：
- `QLoRA + vision` 不建议与 vision tower 解冻同时使用
- 4bit 量化更适合单卡低显存
- 你的设备优先走：
  - Qwen2.5-VL-3B
  - 4bit QLoRA
  - 冻结 vision tower
  - 冻结 merger
  - 只对语言模型做 LoRA

## 建议运行环境
- WSL2 Ubuntu 22.04
- 或原生 Linux

Windows 原生命令行也可以做一部分工作，但训练环节更建议用 WSL2 / Linux。
