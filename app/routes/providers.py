from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.controllers.provider_controller import (
    get_providers,
    get_provider_by_id,
    get_filters,
)

router = APIRouter()


@router.get("/providers")
async def list_providers(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    local_health_district: Optional[str] = None,
    commissioning_agency: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List providers with pagination and filters."""
    providers, total = await get_providers(
        db=db,
        skip=skip,
        limit=limit,
        local_health_district=local_health_district,
        commissioning_agency=commissioning_agency,
        search=search,
    )
    return {
        "items": providers,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/providers/{provider_id}")
async def get_provider(
    provider_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific provider by ID."""
    provider = await get_provider_by_id(db, provider_id)
    if not provider:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


@router.get("/filters")
async def list_filters(db: AsyncSession = Depends(get_db)):
    """Get available filter values."""
    return await get_filters(db)

