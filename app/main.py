from fastapi import FastAPI

from app import routers


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(routers.auth_router)
app.include_router(routers.users_router)