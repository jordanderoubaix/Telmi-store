from fastapi import FastAPI
from .routers import data

app = FastAPI()

app.include_router(data.router)

@app.get("/")
def read_root():
    return {"message": "Your telmi store API is running. Go to /store to get the data."}