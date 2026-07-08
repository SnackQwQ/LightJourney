# -*- coding: utf-8 -*-
"""Trip ORM 模型"""
from sqlalchemy import Column, Integer, String, Date, Time, Text, DECIMAL, DateTime, ForeignKey, Index, func

from database import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    city = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    budget = Column(DECIMAL(10, 2), default=0.00)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    __table_args__ = (
        Index("idx_trips_user_date", "user_id", "date"),
    )
