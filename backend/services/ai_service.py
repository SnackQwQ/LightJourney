# -*- coding: utf-8 -*-
"""AI 服务 — DeepSeek API 调用封装"""
import json
import re

from openai import OpenAI

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)


def call_deepseek(system_prompt: str, user_message: str) -> str:
    """
    调用 DeepSeek API，返回原始文本。
    TODO: P2 实现 — 含超时 + 重试 + JSON 解析容错
    """
    raise NotImplementedError("P2 需要实现 DeepSeek 调用逻辑")
