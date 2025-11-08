from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import os

router = APIRouter(prefix="/admin", tags=["admin"])

# Simple auth check (you can improve this)
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change-me-in-production")


@router.post("/upload-db")
async def upload_database(
    file: UploadFile = File(...),
    token: str = Query(None),
):
    """Upload database file to /data directory."""
    # Verify token
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized - invalid token")
    
    if not file.filename or not file.filename.endswith('.db'):
        raise HTTPException(status_code=400, detail="File must be a .db file")
    
    # Determine data directory
    if os.path.exists("/data"):
        db_path = Path("/data/hsd_ngo.db")
    else:
        db_path = Path("./hsd_ngo.db")
    
    # Ensure directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save uploaded file
    try:
        with open(db_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = db_path.stat().st_size
        return JSONResponse({
            "status": "success",
            "message": "Database uploaded successfully",
            "file_size": file_size,
            "file_size_mb": round(file_size / 1024 / 1024, 2),
            "path": str(db_path)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

