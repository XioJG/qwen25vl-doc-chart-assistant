from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tqdm import tqdm

from src.common import extract_first_json_block, generate_answer, load_model_and_processor
from src.prompt_templates import build_task_prompt


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: str | Path, rows: list[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Qwen2.5-VL 批量推理")
    parser.add_argument("--model-name", type=str, default="Qwen/Qwen2.5-VL-3B-Instruct")
    parser.add_argument("--bits", type=int, default=4, choices=[4, 8, 16])
    parser.add_argument("--device-map", type=str, default="auto")
    parser.add_argument("--input", type=str, required=True, help="simple.jsonl 路径")
    parser.add_argument("--image-root", type=str, required=True, help="图片根目录")
    parser.add_argument("--output", type=str, required=True, help="预测结果 jsonl 输出路径")
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--min-pixels", type=int, default=None)
    parser.add_argument("--max-pixels", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = read_jsonl(args.input)
    image_root = Path(args.image_root)

    model, processor = load_model_and_processor(
        model_name=args.model_name,
        bits=args.bits,
        device_map=args.device_map,
        min_pixels=args.min_pixels,
        max_pixels=args.max_pixels,
    )

    outputs = []
    for row in tqdm(records, desc="batch infer"):
        image_path = image_root / row["image"]
        prompt = build_task_prompt(row.get("task", ""), row.get("instruction", ""))
        answer_text = generate_answer(
            model=model,
            processor=processor,
            image_path=image_path,
            prompt=prompt,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            top_p=args.top_p,
        )
        outputs.append(
            {
                "id": row.get("id"),
                "image": row.get("image"),
                "task": row.get("task"),
                "instruction": row.get("instruction"),
                "ground_truth": row.get("answer"),
                "prediction_text": answer_text,
                "prediction_json": extract_first_json_block(answer_text),
            }
        )

    write_jsonl(args.output, outputs)
    print(f"[OK] predictions saved to {args.output}")


if __name__ == "__main__":
    main()
