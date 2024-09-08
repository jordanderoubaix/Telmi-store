from fastapi import APIRouter, HTTPException, Query
from services.file_service import collect_data
from config import settings

router = APIRouter()

@router.get("/store")
def get_data(api_key: str = Query(None)):
    if api_key is None:
        raise HTTPException(status_code=400, detail="API Key is required")
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    data = collect_data()
    return data
