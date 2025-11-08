import asyncio
from app.database import async_session
from app.models.provider import Provider
from sqlmodel import select

async def check():
    async with async_session() as s:
        result = await s.execute(select(Provider).limit(5))
        providers = result.scalars().all()
        print(f'Found {len(providers)} providers')
        for p in providers:
            print(f'- {p.provider_name}')

asyncio.run(check())

