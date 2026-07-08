# -*- coding: utf-8 -*-
"""
环境变量配置
读取 .env 文件中的配置，提供默认值
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 数据库
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lightjourney.db")

# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# DeepSeek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
