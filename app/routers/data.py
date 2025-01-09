from fastapi import APIRouter, HTTPException, Query, Request
from services.file_service import collect_data
from config import settings

router = APIRouter()

@router.get("/store", name="get_data")
def get_data(request: Request, api_key: str = Query(None)):
    if api_key is None:
        raise HTTPException(status_code=400, detail="API Key is required")
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    scheme = settings.REQUEST_SCHEME
    host = request.headers.get("host")
    base_url = f"{scheme}://{host}"
    
    data = collect_data(base_url)
    return data
