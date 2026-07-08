# -*- coding: utf-8 -*-
"""User ORM 模型"""
from sqlalchemy import Column, Integer, String, DateTime, func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
