from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.routes import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    await init_db()
    yield
    # Shutdown

app = FastAPI(
    title="NSW Human Services Data Hub - NGO Providers Explorer",
    description="Explore NGO providers and services across New South Wales",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(api_router)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

