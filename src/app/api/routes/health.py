import redis
from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import settings
from app.db.session import SessionLocal

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    db_status = "down"
    redis_status = "down"

    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        db_status = "up"
    except Exception:
        db_status = "down"

    try:
        client = redis.from_url(settings.redis_url)
        client.ping()
        redis_status = "up"
    except Exception:
        redis_status = "down"

    return {"status": "ok", "database": db_status, "redis": redis_status}