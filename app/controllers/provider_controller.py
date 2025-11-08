from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func, or_
from typing import Optional, Dict, List
from app.models.provider import Provider


async def get_providers(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
    local_health_district: Optional[str] = None,
    commissioning_agency: Optional[str] = None,
    search: Optional[str] = None,
) -> tuple[List[Provider], int]:
    """Get providers with pagination and filters."""
    query = select(Provider)
    count_query = select(func.count(Provider.id))
    
    # Apply filters
    if local_health_district:
        query = query.where(Provider.local_health_district == local_health_district)
        count_query = count_query.where(Provider.local_health_district == local_health_district)
    
    if commissioning_agency:
        query = query.where(Provider.commissioning_agency == commissioning_agency)
        count_query = count_query.where(Provider.commissioning_agency == commissioning_agency)
    
    if search:
        search_filter = or_(
            Provider.provider_name.ilike(f"%{search}%"),
            Provider.program_name.ilike(f"%{search}%"),
            Provider.local_government_area.ilike(f"%{search}%"),
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)
    
    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()
    
    # Apply pagination and ordering
    query = query.order_by(Provider.provider_name).offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    providers = result.scalars().all()
    
    return list(providers), total


async def get_provider_by_id(db: AsyncSession, provider_id: int) -> Optional[Provider]:
    """Get a specific provider by ID."""
    result = await db.execute(select(Provider).where(Provider.id == provider_id))
    return result.scalar_one_or_none()


async def search_providers(
    db: AsyncSession,
    search_term: str,
    skip: int = 0,
    limit: int = 50,
) -> tuple[List[Provider], int]:
    """Search providers by name, program, or location."""
    return await get_providers(db, skip=skip, limit=limit, search=search_term)


async def get_filters(db: AsyncSession) -> Dict[str, List[str]]:
    """Get available filter values."""
    # Get unique local health districts
    lhd_result = await db.execute(
        select(Provider.local_health_district)
        .where(Provider.local_health_district.isnot(None))
        .distinct()
        .order_by(Provider.local_health_district)
    )
    local_health_districts = [row[0] for row in lhd_result.all() if row[0]]
    
    # Get unique commissioning agencies
    agency_result = await db.execute(
        select(Provider.commissioning_agency)
        .where(Provider.commissioning_agency.isnot(None))
        .distinct()
        .order_by(Provider.commissioning_agency)
    )
    commissioning_agencies = [row[0] for row in agency_result.all() if row[0]]
    
    return {
        "local_health_districts": local_health_districts,
        "commissioning_agencies": commissioning_agencies,
    }

