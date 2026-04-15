from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import torch
from PIL import Image
from transformers import AutoProcessor, BitsAndBytesConfig, Qwen2_5_VLForConditionalGeneration

try:
    from qwen_vl_utils import process_vision_info
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "缺少 qwen-vl-utils，请先安装：pip install qwen-vl-utils"
    ) from exc


def load_image(image_path: str | Path) -> Image.Image:
    image = Image.open(image_path).convert("RGB")
    return image


def build_quant_config(bits: int | None) -> Optional[BitsAndBytesConfig]:
    if bits not in (4, 8):
        return None
    if bits == 4:
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )
    return BitsAndBytesConfig(load_in_8bit=True)


def load_model_and_processor(
    model_name: str,
    bits: int = 4,
    device_map: str = "auto",
    min_pixels: Optional[int] = None,
    max_pixels: Optional[int] = None,
    attn_implementation: Optional[str] = None,
) -> Tuple[Qwen2_5_VLForConditionalGeneration, AutoProcessor]:
    quant_config = build_quant_config(bits)
    model_kwargs: Dict[str, Any] = {
        "device_map": device_map,
        "torch_dtype": torch.float16 if bits in (4, 8) else "auto",
    }
    if quant_config is not None:
        model_kwargs["quantization_config"] = quant_config
    if attn_implementation:
        model_kwargs["attn_implementation"] = attn_implementation

    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        model_name,
        **model_kwargs,
    )

    processor_kwargs: Dict[str, Any] = {}
    if min_pixels is not None:
        processor_kwargs["min_pixels"] = min_pixels
    if max_pixels is not None:
        processor_kwargs["max_pixels"] = max_pixels

    processor = AutoProcessor.from_pretrained(model_name, **processor_kwargs)
    return model, processor


def build_messages(image_path: str, prompt: str, system_prompt: Optional[str] = None) -> list[dict[str, Any]]:
    messages = []
    if system_prompt:
        messages.append(
            {
                "role": "system",
                "content": [{"type": "text", "text": system_prompt}],
            }
        )
    messages.append(
        {
            "role": "user",
            "content": [
                {"type": "image", "image": str(image_path)},
                {"type": "text", "text": prompt},
            ],
        }
    )
    return messages


def move_to_model_device(inputs: Dict[str, Any], model: Qwen2_5_VLForConditionalGeneration) -> Dict[str, Any]:
    model_device = None
    try:
        model_device = model.device
    except Exception:
        model_device = None

    if model_device is None:
        return inputs

    moved: Dict[str, Any] = {}
    for key, value in inputs.items():
        if hasattr(value, "to"):
            moved[key] = value.to(model_device)
        else:
            moved[key] = value
    return moved


@torch.inference_mode()
def generate_answer(
    model: Qwen2_5_VLForConditionalGeneration,
    processor: AutoProcessor,
    image_path: str | Path,
    prompt: str,
    system_prompt: Optional[str] = None,
    max_new_tokens: int = 512,
    temperature: float = 0.1,
    top_p: float = 0.9,
) -> str:
    messages = build_messages(str(image_path), prompt, system_prompt=system_prompt)
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    model_inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    model_inputs = move_to_model_device(model_inputs, model)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,
        do_sample=temperature > 0,
        temperature=max(temperature, 1e-5),
        top_p=top_p,
    )
    generated_ids_trimmed = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(model_inputs["input_ids"], generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0]
    return output_text.strip()


def extract_first_json_block(text: str) -> Optional[dict[str, Any]]:
    text = text.strip()

    if text.startswith("```"):
        fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.S)
        if fenced:
            for candidate in fenced:
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    continue

    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

    match = re.search(r"(\{.*\})", text, flags=re.S)
    if match:
        candidate = match.group(1)
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return None
    return None


def save_prediction(
    save_path: str | Path,
    image_path: str | Path,
    prompt: str,
    answer_text: str,
    task: str,
) -> None:
    payload = {
        "image": str(image_path),
        "task": task,
        "prompt": prompt,
        "answer_text": answer_text,
        "answer_json": extract_first_json_block(answer_text),
    }
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
