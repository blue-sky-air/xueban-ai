import os
from dotenv import load_dotenv

load_dotenv()

AI_API_KEY=os.getenv("AI_API_KEY", "")
AI_BASE_URL=os.getenv("AI_BASE_URL", "https://token-plan-cn.xiaomimimo.com")
AI_MODEL=os.getenv("AI_MODEL", "mimo-v2.5-pro")

JWT_SECRET=os.getenv("JWT_SECRET", "xueban-ai-secret-key-2026-very-long")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 72

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./xueban_ai.db")

PORT = int(os.getenv("PORT", "8000"))
