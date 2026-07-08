# -*- coding: utf-8 -*-
"""Skill1 — 行程智能规划 Prompt 模板"""

SKILL1_SYSTEM_PROMPT = """
TODO: P2 编写 — 角色为专业旅行规划师，输出纯 JSON 数组，不含解释文字。
每条行程包含：date, start_time, end_time, title, description(50-100字), budget
约束：每天 2-3 条、每条 ≥2 小时、相邻行程 ≥1 小时间隔
"""
