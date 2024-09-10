from fastapi import APIRouter, HTTPException, Query, Request
from services.file_service import collect_data
from config import settings

router = APIRouter()

@router.get("/store")
def get_data(request: Request, api_key: str = Query(None)):
    if api_key is None:
        raise HTTPException(status_code=400, detail="API Key is required")
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    base_url = str(request.url_for("get_data")).replace("/store", "")
    data = collect_data(base_url)
    return data