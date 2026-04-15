# data 目录说明

- `raw/`：原始标注文件、原始图片、截图、PDF 页面导出图等
- `images/`：统一供训练/推理使用的图片目录
- `processed/`：转换后的中间产物
- `examples/`：模板示例数据

## 推荐工作流
1. 把图片统一放到 `data/images/`
2. 用 `train.simple.jsonl / val.simple.jsonl` 维护任务样本
3. 用 `tools/convert_simple_jsonl_to_llava_json.py` 转成训练 JSON
