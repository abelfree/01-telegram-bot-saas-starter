from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user
from app.db.session import get_db
from app.models.bot import Bot
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.bot import BotCreate, BotRead

router = APIRouter()


@router.post("", response_model=BotRead, status_code=status.HTTP_201_CREATED)
def create_bot(
    payload: BotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tenant = db.query(Tenant).filter(Tenant.id == payload.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    if tenant.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden for this tenant")

    existing = db.query(Bot).filter(Bot.telegram_bot_token == payload.telegram_bot_token).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bot token already exists")

    bot = Bot(**payload.model_dump())
    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot


@router.get("", response_model=list[BotRead])
def list_bots(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(Bot)
        .join(Tenant, Tenant.id == Bot.tenant_id)
        .filter((Tenant.owner_id == current_user.id) | (current_user.is_superuser))
        .all()
    )