from fastapi import APIRouter
from app.routes import providers, web, admin

api_router = APIRouter()
api_router.include_router(providers.router, prefix="/api/v1", tags=["providers"])
api_router.include_router(web.router, tags=["web"])
api_router.include_router(admin.router, tags=["admin"])

