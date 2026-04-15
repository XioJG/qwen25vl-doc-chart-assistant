from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def normalize_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip().lower()


def read_jsonl(path: str | Path) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="结构化抽取评测")
    parser.add_argument("--predictions", type=str, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_jsonl(args.predictions)

    total_samples = 0
    exact_samples = 0
    total_fields = 0
    correct_fields = 0

    for row in rows:
        gold = row.get("ground_truth")
        pred = row.get("prediction_json")

        if not isinstance(gold, dict):
            continue
        total_samples += 1

        if not isinstance(pred, dict):
            pred = {}

        field_ok = True
        for key, gold_value in gold.items():
            total_fields += 1
            if normalize_value(pred.get(key)) == normalize_value(gold_value):
                correct_fields += 1
            else:
                field_ok = False

        if field_ok and set(pred.keys()) >= set(gold.keys()):
            exact_samples += 1

    if total_samples == 0:
        print("No structured extraction samples found.")
        return

    metrics = {
        "total_samples": total_samples,
        "sample_exact_match": round(exact_samples / total_samples, 4),
        "field_accuracy": round(correct_fields / max(total_fields, 1), 4),
        "total_fields": total_fields,
    }
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
