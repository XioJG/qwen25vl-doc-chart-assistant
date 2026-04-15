from __future__ import annotations

import argparse
import json
from functools import lru_cache
from typing import Optional

import gradio as gr

from src.common import extract_first_json_block, generate_answer, load_model_and_processor
from src.prompt_templates import PROMPT_LIBRARY, build_task_prompt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Qwen2.5-VL Gradio Demo")
    parser.add_argument("--model-name", type=str, default="Qwen/Qwen2.5-VL-3B-Instruct")
    parser.add_argument("--bits", type=int, default=4, choices=[4, 8, 16])
    parser.add_argument("--device-map", type=str, default="auto")
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--min-pixels", type=int, default=None)
    parser.add_argument("--max-pixels", type=int, default=None)
    parser.add_argument("--share", action="store_true")
    parser.add_argument("--server-name", type=str, default="127.0.0.1")
    parser.add_argument("--server-port", type=int, default=7860)
    return parser.parse_args()


def build_demo(args: argparse.Namespace) -> gr.Blocks:
    @lru_cache(maxsize=1)
    def get_runtime():
        return load_model_and_processor(
            model_name=args.model_name,
            bits=args.bits,
            device_map=args.device_map,
            min_pixels=args.min_pixels,
            max_pixels=args.max_pixels,
        )

    def run_infer(
        image_path: Optional[str],
        task: str,
        user_question: str,
        system_prompt: str,
    ):
        if not image_path:
            return "请先上传一张图片。", None

        model, processor = get_runtime()
        prompt = build_task_prompt(task, user_question)
        answer = generate_answer(
            model=model,
            processor=processor,
            image_path=image_path,
            prompt=prompt,
            system_prompt=system_prompt or None,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            top_p=args.top_p,
        )
        parsed = extract_first_json_block(answer)
        parsed_pretty = json.dumps(parsed, ensure_ascii=False, indent=2) if parsed else None
        return answer, parsed_pretty

    with gr.Blocks(title="Qwen2.5-VL 文档/图表/截图理解助手") as demo:
        gr.Markdown("# Qwen2.5-VL 文档/图表/截图理解助手\n上传图片后，选择任务模板并输入问题。")
        with gr.Row():
            with gr.Column(scale=1):
                image = gr.Image(type="filepath", label="输入图片")
                task = gr.Dropdown(
                    choices=list(PROMPT_LIBRARY.keys()),
                    value="structured_extraction",
                    label="任务模板",
                )
                user_question = gr.Textbox(
                    lines=5,
                    label="问题 / 指令",
                    value="请提取图中的关键信息，并以 JSON 输出。",
                )
                system_prompt = gr.Textbox(
                    lines=2,
                    label="系统提示词（可选）",
                    value="你是一个严谨的多模态文档与图表理解助手。",
                )
                submit = gr.Button("开始推理", variant="primary")
            with gr.Column(scale=1):
                answer = gr.Textbox(lines=12, label="模型原始回答")
                parsed_json = gr.Code(label="解析出的 JSON（如果有）", language="json")

        submit.click(
            fn=run_infer,
            inputs=[image, task, user_question, system_prompt],
            outputs=[answer, parsed_json],
        )

    return demo


def main() -> None:
    args = parse_args()
    demo = build_demo(args)
    demo.launch(
        share=args.share,
        server_name=args.server_name,
        server_port=args.server_port,
    )


if __name__ == "__main__":
    main()
