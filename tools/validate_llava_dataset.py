from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 LLaVA 格式数据")
    parser.add_argument("--data", type=str, required=True, help="LLaVA JSON 文件")
    parser.add_argument("--image-root", type=str, required=True, help="图片根目录")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    image_root = Path(args.image_root)

    errors = []
    for idx, row in enumerate(data):
        if "id" not in row:
            errors.append(f"[{idx}] missing id")
        if "image" not in row:
            errors.append(f"[{idx}] missing image")
        if "conversations" not in row or not isinstance(row["conversations"], list):
            errors.append(f"[{idx}] missing conversations")
            continue

        image_field = row["image"]
        if isinstance(image_field, str):
            image_path = image_root / image_field
            if not image_path.exists():
                errors.append(f"[{idx}] image not found: {image_path}")
        elif isinstance(image_field, list):
            for rel in image_field:
                image_path = image_root / rel
                if not image_path.exists():
                    errors.append(f"[{idx}] image not found: {image_path}")
        else:
            errors.append(f"[{idx}] image must be str or list")

        convs = row["conversations"]
        if len(convs) < 2:
            errors.append(f"[{idx}] conversations too short")
            continue

        for c_idx, conv in enumerate(convs):
            if "from" not in conv or "value" not in conv:
                errors.append(f"[{idx}] conversation[{c_idx}] missing from/value")

        if convs[0].get("from") != "human":
            errors.append(f"[{idx}] first conversation should be human")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(" -", err)
    else:
        print("Validation passed.")


if __name__ == "__main__":
    main()
