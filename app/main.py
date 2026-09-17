from fastapi import FastAPI
from sqlalchemy import engine

from app import models

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}