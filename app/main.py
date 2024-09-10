import logging
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import FileResponse
from routers import data
from config import settings
from pathlib import Path

app = FastAPI()

# Inclure les routers
app.include_router(data.router)

@app.get("/")
def read_root():
    return {"message": "Your telmi store API is running. Go to /store to get the data."}

@app.on_event("startup")
async def on_startup():
    logging.info(f"A new API Key has been generated: {settings.API_KEY}")

@app.get("/file/download")
def download_file(filename: str, api_key: str = Query(None)):
    if api_key is None:
        raise HTTPException(status_code=400, detail="API Key is required")
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    if filename is None:
        raise HTTPException(status_code=400, detail="Filename is required")

    logging.info(f"Downloading file: {filename}")
    shared_path = Path(settings.SHARED_DIRECTORY_PATH)
    file_path = shared_path / filename

    logging.info("file_path : ", file_path)

    return FileResponse(path=file_path, filename=filename, media_type="multipart/form-data")