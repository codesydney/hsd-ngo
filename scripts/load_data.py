"""
Script to load CSV data into the database.
"""
import asyncio
import csv
import sys
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.provider import Provider
from app.database import DATABASE_URL

async def load_csv_data(csv_path: str):
    """Load CSV data into the database."""
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    # Read and insert data
    async with async_session() as session:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                provider = Provider(
                    provider_name=row.get('Provider Name', '').strip() or None,
                    provider_identifier_abn=row.get('Provider Identifier (ABN)', '').strip() or None,
                    delivery_area=row.get('Delivery Area', '').strip() or None,
                    local_government_area=row.get('Local Government Area Name Multi Value Description', '').strip() or None,
                    local_health_district=row.get('Local Health District Multi Value Description', '').strip() or None,
                    target_group=row.get('Target Group Multi Value Description', '').strip() or None,
                    classification=row.get('Classification Multi Value Description', '').strip() or None,
                    gender=row.get('Gender', '').strip() or None,
                    indigenous_status=row.get('Indigenous status', '').strip() or None,
                    commissioning_agency=row.get('Commissioning Agency', '').strip() or None,
                    program_name=row.get('Program Name', '').strip() or None,
                    agreement_identifier=row.get('Agreement Identifier', '').strip() or None,
                    agreement_start_date=row.get('Agreement Start Date', '').strip() or None,
                    agreement_end_date=row.get('Agreement End Date', '').strip() or None,
                )
                session.add(provider)
                count += 1
                
                if count % 1000 == 0:
                    await session.commit()
                    print(f"Loaded {count} records...")
            
            await session.commit()
            print(f"Successfully loaded {count} records")
    
    await engine.dispose()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python load_data.py <path_to_csv_file>")
        print("Example: python load_data.py data.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    if not Path(csv_path).exists():
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)
    
    asyncio.run(load_csv_data(csv_path))

