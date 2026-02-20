from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user
from app.db.session import get_db
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.tenant import TenantCreate, TenantRead

router = APIRouter()


@router.post("", response_model=TenantRead, status_code=status.HTTP_201_CREATED)
def create_tenant(
    payload: TenantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    duplicate = db.query(Tenant).filter((Tenant.name == payload.name) | (Tenant.slug == payload.slug)).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Tenant with name or slug already exists")

    tenant = Tenant(name=payload.name, slug=payload.slug, owner_id=current_user.id)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


@router.get("", response_model=list[TenantRead])
def list_tenants(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Tenant).filter(Tenant.owner_id == current_user.id).all()