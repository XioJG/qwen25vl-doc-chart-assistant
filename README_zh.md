# Qwen2.5-VL-3B 可运行代码模板包

这是一个面向 **“文档 / 图表 / 截图理解与结构化抽取助手”** 的可运行项目模板包，针对你的设备配置（i9-14900 笔记本 + RTX 4060 Laptop 8GB 左右显存）做了现实可行的取舍：

- **本地推理 / Gradio Demo：可直接跑**
- **小规模批量推理 / 评测：可直接跑**
- **LoRA / QLoRA 微调：建议在 WSL2 / Ubuntu 下运行**
- **全参数训练 / 大分辨率多图 / 视频微调：不建议在本机作为主路线**

## 1. 你拿到这个模板包后能做什么

1. 用 **Qwen2.5-VL-3B-Instruct** 在本地对单张图片执行：
   - 文档问答
   - 图表问答
   - 字段抽取
   - 截图理解
   - 结构化 JSON 输出

2. 用一个简单数据集做：
   - 批量推理
   - QA 评测
   - 结构化抽取评测

3. 把自己的数据集转成 **Qwen-VL-Series-Finetune** 所需的 **LLaVA 格式 JSON**

4. 在 WSL2 / Linux 下用官方开源训练链做：
   - **4-bit QLoRA 微调（建议 8GB 设备优先）**
   - LoRA 权重合并
   - 微调后重新推理和评测

5. 跑一个本地 **Gradio Web Demo**

---

## 2. 与官方资源的关系

本模板包的定位是：

- **推理 / Demo / 数据转换 / 评测**：直接由本模板包提供代码
- **正式 LoRA / QLoRA 微调**：通过你本地克隆的官方开源项目完成

原因是：
- Qwen2.5-VL 官方已经给出了 Transformers 推理方式
- 官方推荐使用最新 Transformers 与 `qwen-vl-utils`
- 社区维护的 **Qwen-VL-Series-Finetune** 已经支持 Qwen2.5-VL、LoRA/QLoRA、LLaVA 格式数据、LoRA 合并、WebUI 等完整训练链

所以这个模板包不是“另起炉灶再写一套训练框架”，而是把你真正需要自己掌控的部分——**项目结构、数据、评测、Demo、命令、脚本**——全部整理好。

---

## 3. 目录结构

```text
qwen25vl_code_template_pack/
├─ README_zh.md
├─ open_source_links.md
├─ requirements.inference.txt
├─ requirements.demo.txt
├─ .gitignore
├─ configs/
│  └─ app_config.example.yaml
├─ data/
│  ├─ README.md
│  ├─ raw/
│  ├─ images/
│  ├─ processed/
│  └─ examples/
│     ├─ train.simple.jsonl
│     ├─ val.simple.jsonl
│     ├─ train.llava.json
│     └─ val.llava.json
├─ outputs/
├─ scripts/
│  ├─ windows/
│  │  ├─ 01_create_venv.bat
│  │  ├─ 02_install_inference.bat
│  │  ├─ 03_run_demo.bat
│  │  └─ 04_run_infer_example.bat
│  ├─ linux/
│  │  ├─ 01_setup.sh
│  │  ├─ 02_run_demo.sh
│  │  └─ 03_run_infer_example.sh
│  └─ training/
│     ├─ README_zh.md
│     ├─ clone_finetune_repo.sh
│     ├─ finetune_8gb_qlora_example.sh
│     └─ merge_lora_example.sh
├─ src/
│  ├─ __init__.py
│  ├─ common.py
│  ├─ prompt_templates.py
│  ├─ inference_cli.py
│  ├─ batch_infer.py
│  ├─ eval_qa.py
│  ├─ eval_extraction.py
│  └─ app_gradio.py
└─ tools/
   ├─ convert_simple_jsonl_to_llava_json.py
   ├─ validate_llava_dataset.py
   ├─ make_train_val_split.py
   └─ preview_dataset.py
```

---

## 4. 建议你的实际使用顺序

### 第一步：跑通本地推理
先用 `src/inference_cli.py` 对一张图片跑通问答 / 抽取。

### 第二步：跑通 Gradio Demo
确认你能上传图片并看到结果。

### 第三步：建立你自己的 `simple.jsonl` 数据集
先做 100～300 条高质量样本，不要一开始追求上千条。

### 第四步：批量推理 + 评测
用 `src/batch_infer.py`、`src/eval_qa.py`、`src/eval_extraction.py` 跑基线分数。

### 第五步：转成 LLaVA 格式
用 `tools/convert_simple_jsonl_to_llava_json.py` 生成训练用 JSON。

### 第六步：在 WSL2 / Linux 下做 QLoRA 微调
优先跑 `scripts/training/finetune_8gb_qlora_example.sh`。

### 第七步：合并 LoRA 权重并重新评测
用合并后的模型替换推理底座，再比较前后结果。

---

## 5. 最快上手命令

### Windows
```bat
cd qwen25vl_code_template_pack
scripts\windows_create_venv.bat
scripts\windows_install_inference.bat
scripts\windows_run_infer_example.bat
```

### Linux / WSL2
```bash
cd qwen25vl_code_template_pack
bash scripts/linux/01_setup.sh
bash scripts/linux/03_run_infer_example.sh
bash scripts/linux/02_run_demo.sh
```

---

## 6. 你的数据推荐格式：simple.jsonl

模板包内部优先使用一种更适合自己维护的数据格式：

```json
{
  "id": "sample_001",
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

然后通过工具脚本转成训练仓库需要的 **LLaVA 格式 JSON**。

这样做的好处是：
- 你自己维护数据更轻松
- 同一份原始数据既可用于评测，也可用于训练转换
- 字段抽取和问答任务都能统一管理

---

## 7. 适合你本机的训练策略

你的设备是单卡 4060 Laptop，因此建议按下面优先级来：

### 最优方案
- **Qwen2.5-VL-3B-Instruct**
- **4-bit QLoRA**
- **冻结 vision tower**
- **冻结 merger / projector**
- 只对语言模型部分做 LoRA
- 图像分辨率控制在 448 左右
- batch size = 1
- gradient accumulation = 8～16

### 不建议的方案
- 全参数训练
- 多图 / 视频训练
- vision tower LoRA + 4bit 量化同时开启
- 超高分辨率图像微调

---

## 8. 你还需要自己准备什么

1. 你自己的图片数据集
2. Hugging Face 访问与模型下载能力
3. Windows 下建议安装：
   - Python 3.10+
   - Git
   - CUDA 对应的 PyTorch
4. 若做微调，建议安装：
   - WSL2 + Ubuntu
   - 或 Linux 环境

---

## 9. 重要提醒

- 这个模板包里的 **推理 / Demo / 数据转换 / 评测** 是可直接运行的代码模板。
- **正式训练** 依赖外部开源训练项目，模板包已给出配套脚本和说明。
- 由于不同机器的 CUDA、驱动、PyTorch 版本会影响安装，模板包默认优先保证：
  - 代码结构清晰
  - 命令可改
  - 逻辑完整
  - 本地单图推理和 Demo 最容易先跑通

建议你先跑通推理和 Demo，再进入微调。

建议持续补充脱敏样例、真实运行记录和评测结果，让项目从可运行模板逐步演进为完整的多模态应用工程。
