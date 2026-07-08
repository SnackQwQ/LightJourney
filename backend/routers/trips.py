# -*- coding: utf-8 -*-
"""行程路由 — CRUD"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/trips", tags=["行程"])


@router.get("")
async def get_trips():
    """TODO: P2 实现 — 行程列表（含筛选 + 预算统计）"""
    raise NotImplementedError("P2 需要实现行程列表逻辑")


@router.post("")
async def create_trip():
    """TODO: P2 实现 — 创建行程"""
    raise NotImplementedError("P2 需要实现创建行程逻辑")


@router.put("/{trip_id}")
async def update_trip(trip_id: int):
    """TODO: P2 实现 — 更新行程"""
    raise NotImplementedError("P2 需要实现更新行程逻辑")


@router.delete("/{trip_id}")
async def delete_trip(trip_id: int):
    """TODO: P2 实现 — 删除行程"""
    raise NotImplementedError("P2 需要实现删除行程逻辑")
