from pydantic import BaseModel, ConfigDict


class BotCreate(BaseModel):
    tenant_id: int
    name: str
    telegram_bot_token: str
    webhook_secret: str


class BotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    name: str