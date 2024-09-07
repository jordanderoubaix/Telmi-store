from fastapi import APIRouter
from ..services.file_service import collect_data

router = APIRouter()

@router.get("/store")
def get_data():
    data = collect_data()
    return data