import logging
from fastapi import FastAPI
from routers import data
from config import settings

app = FastAPI()

app.include_router(data.router)

@app.get("/")
def read_root():
    return {"message": "Your telmi store API is running. Go to /store to get the data."}


@app.on_event("startup")
async def on_startup():
    logging.info(f"A new API Key has been generated: {settings.API_KEY}")
