from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    instruction: str
    description: str


PROMPT_LIBRARY: Dict[str, PromptTemplate] = {
    "structured_extraction": PromptTemplate(
        name="structured_extraction",
        instruction=(
            "请阅读这张图片中的关键信息。"
            "如果图中存在表单、票据、报表、界面字段或表格，请提取最重要的字段，"
            "并严格以 JSON 输出，不要输出多余解释。"
        ),
        description="结构化字段抽取，适合票据、表单、文档、截图。",
    ),
    "doc_qa": PromptTemplate(
        name="doc_qa",
        instruction=(
            "请基于图片内容回答问题。"
            "如果答案无法从图中直接获得，请明确说明无法确定。"
        ),
        description="文档问答。",
    ),
    "chart_qa": PromptTemplate(
        name="chart_qa",
        instruction=(
            "请仔细阅读图表，包括标题、图例、坐标轴、标注和数据趋势，"
            "然后回答问题。除非明确要求解释，否则优先给出简洁答案。"
        ),
        description="图表问答。",
    ),
    "ui_understanding": PromptTemplate(
        name="ui_understanding",
        instruction=(
            "请分析这个界面截图的主要功能、关键模块和可交互区域。"
            "如果用户要求结构化结果，请使用 JSON 输出。"
        ),
        description="界面理解。",
    ),
    "grounding_like_json": PromptTemplate(
        name="grounding_like_json",
        instruction=(
            "如果用户要求定位，请在回答中给出一个 JSON。"
            "JSON 至少包含 target 和 bbox 字段，bbox 格式为 [x1, y1, x2, y2]。"
            "如果无法定位，请返回 {\"target\": \"unknown\", \"bbox\": null}。"
        ),
        description="通过提示词要求输出类似 grounding 的 JSON。",
    ),
}


def build_task_prompt(task: str, question: str) -> str:
    template = PROMPT_LIBRARY.get(task)
    if template is None:
        return question.strip()

    question = question.strip()
    if not question:
        return template.instruction
    return f"{template.instruction}\n\n用户问题：{question}"


def list_prompt_names() -> list[str]:
    return list(PROMPT_LIBRARY.keys())
