# -*- coding: utf-8 -*-
"""AI 路由 — Skill1 行程规划 / Skill2 文案生成"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/ai", tags=["AI"])


@router.post("/plan")
async def plan_trip():
    """TODO: P2 实现 — Skill1 行程智能规划"""
    raise NotImplementedError("P2 需要实现 AI 行程规划逻辑")


@router.post("/copywriting")
async def generate_copywriting():
    """TODO: P2 实现 — Skill2 行程文案生成"""
    raise NotImplementedError("P2 需要实现 AI 文案生成逻辑")
