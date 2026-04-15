from __future__ import annotations

import argparse
from pathlib import Path

from src.common import generate_answer, load_model_and_processor, save_prediction
from src.prompt_templates import build_task_prompt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Qwen2.5-VL 单图推理 CLI")
    parser.add_argument("--model-name", type=str, default="Qwen/Qwen2.5-VL-3B-Instruct")
    parser.add_argument("--bits", type=int, default=4, choices=[4, 8, 16])
    parser.add_argument("--device-map", type=str, default="auto")
    parser.add_argument("--image", type=str, required=True, help="输入图片路径")
    parser.add_argument("--task", type=str, default="structured_extraction")
    parser.add_argument("--question", type=str, default="")
    parser.add_argument("--system-prompt", type=str, default="")
    parser.add_argument("--min-pixels", type=int, default=None)
    parser.add_argument("--max-pixels", type=int, default=None)
    parser.add_argument("--attn-implementation", type=str, default=None)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--save", type=str, default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prompt = build_task_prompt(args.task, args.question)

    model, processor = load_model_and_processor(
        model_name=args.model_name,
        bits=args.bits,
        device_map=args.device_map,
        min_pixels=args.min_pixels,
        max_pixels=args.max_pixels,
        attn_implementation=args.attn_implementation,
    )

    answer = generate_answer(
        model=model,
        processor=processor,
        image_path=args.image,
        prompt=prompt,
        system_prompt=args.system_prompt or None,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
    )

    print("=" * 80)
    print("PROMPT:")
    print(prompt)
    print("=" * 80)
    print("ANSWER:")
    print(answer)
    print("=" * 80)

    if args.save:
        save_prediction(
            save_path=Path(args.save),
            image_path=args.image,
            prompt=prompt,
            answer_text=answer,
            task=args.task,
        )
        print(f"[OK] saved prediction to: {args.save}")


if __name__ == "__main__":
    main()
