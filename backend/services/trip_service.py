# -*- coding: utf-8 -*-
"""行程服务 — CRUD / 冲突检测 / 预算统计"""


def check_conflict(user_id: int, date: str, start_time: str, end_time: str, exclude_trip_id: int = None) -> list:
    """
    时段冲突检测。
    算法：A和B重叠 ⟺ A.start < B.end AND A.end > B.start
    注意：12:00 结束 vs 12:00 开始 → 不冲突（等于不算重叠）
    TODO: P2 实现
    """
    raise NotImplementedError("P2 需要实现冲突检测逻辑")


def create_trip(user_id: int, data: dict) -> dict:
    """TODO: P2 实现 — 创建行程"""
    raise NotImplementedError("P2 需要实现创建行程逻辑")


def get_trips(user_id: int, city: str = None, date_from: str = None, date_to: str = None) -> dict:
    """TODO: P2 实现 — 行程列表（含筛选 + 预算统计）"""
    raise NotImplementedError("P2 需要实现行程列表逻辑")


def update_trip(trip_id: int, user_id: int, data: dict) -> dict:
    """TODO: P2 实现 — 更新行程"""
    raise NotImplementedError("P2 需要实现更新行程逻辑")


def delete_trip(trip_id: int, user_id: int) -> None:
    """TODO: P2 实现 — 删除行程"""
    raise NotImplementedError("P2 需要实现删除行程逻辑")
