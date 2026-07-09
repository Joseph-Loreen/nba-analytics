from fastapi import FastAPI
from app.routers import players, teams, games, player_game_stats

app = FastAPI(title="NBA Analytics API")

app.include_router(players.router)
app.include_router(teams.router)
app.include_router(games.router)
app.include_router(player_game_stats.router)

@app.get("/")
def read_root():
    return {"message": "NBA Analytics API is running"}