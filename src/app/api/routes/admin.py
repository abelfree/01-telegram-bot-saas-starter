from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user
from app.db.session import get_db
from app.models.bot import Bot
from app.models.tenant import Tenant
from app.models.telegram_update import TelegramUpdate
from app.models.user import User

router = APIRouter()


@router.get("/overview")
def overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Superuser required")

    return {
        "users": db.query(func.count(User.id)).scalar() or 0,
        "tenants": db.query(func.count(Tenant.id)).scalar() or 0,
        "bots": db.query(func.count(Bot.id)).scalar() or 0,
        "updates": db.query(func.count(TelegramUpdate.id)).scalar() or 0,
    }