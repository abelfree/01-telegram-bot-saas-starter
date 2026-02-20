from fastapi import APIRouter

from app.api.routes import admin, auth, bots, health, tenants, webhook

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(bots.router, prefix="/bots", tags=["bots"])
api_router.include_router(webhook.router, prefix="/telegram", tags=["telegram"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])