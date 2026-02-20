from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.models.plan import Plan


DEFAULT_PLANS = [
    {"code": "free", "name": "Free", "price_cents": 0, "interval": "month"},
    {"code": "starter", "name": "Starter", "price_cents": 1900, "interval": "month"},
    {"code": "growth", "name": "Growth", "price_cents": 7900, "interval": "month"},
]


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        for plan in DEFAULT_PLANS:
            exists = db.query(Plan).filter(Plan.code == plan["code"]).first()
            if exists:
                continue
            db.add(Plan(**plan))
        db.commit()