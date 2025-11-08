from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.controllers.provider_controller import get_providers, get_filters

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: AsyncSession = Depends(get_db)):
    """Home page with provider explorer."""
    providers, total = await get_providers(db=db, skip=0, limit=50)
    filters = await get_filters(db)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "providers": providers,
            "total": total,
            "filters": filters,
        },
    )


@router.get("/providers", response_class=HTMLResponse)
async def providers_page(
    request: Request,
    skip: int = 0,
    limit: int = 50,
    local_health_district: str = None,
    commissioning_agency: str = None,
    search: str = None,
    db: AsyncSession = Depends(get_db),
):
    """Providers listing page."""
    providers, total = await get_providers(
        db=db,
        skip=skip,
        limit=limit,
        local_health_district=local_health_district,
        commissioning_agency=commissioning_agency,
        search=search,
    )
    filters = await get_filters(db)
    
    return templates.TemplateResponse(
        "providers.html",
        {
            "request": request,
            "providers": providers,
            "total": total,
            "skip": skip,
            "limit": limit,
            "local_health_district": local_health_district,
            "commissioning_agency": commissioning_agency,
            "search": search,
            "filters": filters,
        },
    )

