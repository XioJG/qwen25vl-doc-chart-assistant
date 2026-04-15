from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    text = str(text).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def token_f1(pred: str, gold: str) -> float:
    pred_tokens = normalize_text(pred).split()
    gold_tokens = normalize_text(gold).split()
    if not pred_tokens and not gold_tokens:
        return 1.0
    if not pred_tokens or not gold_tokens:
        return 0.0

    common = Counter(pred_tokens) & Counter(gold_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0.0

    precision = num_same / len(pred_tokens)
    recall = num_same / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)


def read_jsonl(path: str | Path) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="文本问答评测")
    parser.add_argument("--predictions", type=str, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_jsonl(args.predictions)

    exact = 0
    f1_sum = 0.0
    total = 0

    for row in rows:
        gold = row.get("ground_truth")
        pred = row.get("prediction_text")
        if isinstance(gold, dict):
            continue
        total += 1
        if normalize_text(pred) == normalize_text(gold):
            exact += 1
        f1_sum += token_f1(str(pred), str(gold))

    if total == 0:
        print("No text QA samples found.")
        return

    print(json.dumps({
        "total": total,
        "exact_match": round(exact / total, 4),
        "token_f1": round(f1_sum / total, 4),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
