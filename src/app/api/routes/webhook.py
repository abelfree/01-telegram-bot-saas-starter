from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.bot import Bot
from app.models.telegram_update import TelegramUpdate
from app.schemas.webhook import WebhookAck

router = APIRouter()


@router.post("/{bot_token}/webhook", response_model=WebhookAck)
def ingest_update(
    bot_token: str,
    payload: dict,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    bot = db.query(Bot).filter(Bot.telegram_bot_token == bot_token).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if bot.webhook_secret != x_telegram_bot_api_secret_token:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    update = TelegramUpdate(bot_id=bot.id, update_id=payload.get("update_id"), payload=payload)
    db.add(update)
    db.commit()

    return WebhookAck(status="accepted", received_update_id=payload.get("update_id"))