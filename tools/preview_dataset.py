from __future__ import annotations

import argparse
import json
from collections import Counter
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="预览 simple.jsonl 数据集")
    parser.add_argument("--input", type=str, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_jsonl(args.input)
    tasks = Counter(row.get("task", "unknown") for row in rows)

    print("=" * 80)
    print(f"样本数: {len(rows)}")
    print("任务分布:")
    for task, count in tasks.items():
        print(f" - {task}: {count}")

    if rows:
        print("=" * 80)
        print("第一条样本:")
        print(json.dumps(rows[0], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
