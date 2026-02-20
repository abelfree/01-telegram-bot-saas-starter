from pydantic import BaseModel


class WebhookAck(BaseModel):
    status: str
    received_update_id: int | None = None