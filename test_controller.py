import asyncio
from app.controllers.provider_controller import get_providers, get_filters
from app.database import async_session

async def test():
    async with async_session() as db:
        providers, total = await get_providers(db, skip=0, limit=50)
        filters = await get_filters(db)
        print(f'Total: {total}')
        print(f'Providers returned: {len(providers)}')
        print(f'Filters - LHDs: {len(filters["local_health_districts"])}')
        print(f'Filters - Agencies: {len(filters["commissioning_agencies"])}')
        if providers:
            print(f'First provider: {providers[0].provider_name}')

asyncio.run(test())

