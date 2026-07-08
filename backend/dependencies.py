# -*- coding: utf-8 -*-
"""JWT 鉴权依赖"""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    从请求头解析 JWT token，返回 user_id。
    TODO: P1 实现 — 验证 token 并解析 user_id
    """
    raise NotImplementedError("P1 需要实现 JWT 验证逻辑")
