# -*- coding: utf-8 -*-
"""鉴权路由 — 注册 / 登录"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["鉴权"])


@router.post("/register")
async def register():
    """TODO: P1 实现 — 用户注册"""
    raise NotImplementedError("P1 需要实现注册逻辑")


@router.post("/login")
async def login():
    """TODO: P1 实现 — 用户登录"""
    raise NotImplementedError("P1 需要实现登录逻辑")
