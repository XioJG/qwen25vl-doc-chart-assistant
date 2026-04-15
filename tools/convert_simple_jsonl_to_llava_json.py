from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def answer_to_text(answer: Any) -> str:
    if isinstance(answer, (dict, list)):
        return json.dumps(answer, ensure_ascii=False)
    return str(answer)


def convert(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    converted = []
    for row in records:
        converted.append(
            {
                "id": row["id"],
                "image": row["image"],
                "conversations": [
                    {
                        "from": "human",
                        "value": f"<image>\n{row['instruction']}",
                    },
                    {
                        "from": "gpt",
                        "value": answer_to_text(row["answer"]),
                    },
                ],
            }
        )
    return converted


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="simple.jsonl 转 LLaVA 格式 JSON")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = read_jsonl(args.input)
    converted = convert(records)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(converted, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] saved llava json to {args.output}")


if __name__ == "__main__":
    main()
