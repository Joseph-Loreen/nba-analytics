from fastapi import FastAPI
from app.routers import players

app = FastAPI(title="NBA Analytics API")

app.include_router(players.router)

@app.get("/")
def read_root():
    return {"message": "NBA Analytics API is running"}