from pydantic import BaseModel
from app.schemas.player import PlayerBasic
from app.schemas.game import GameResponse

class PlayerGameStatsResponse(BaseModel):
    id: int
    player_id: int
    game_id: int
    points: int
    rebounds: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    minutes_played: float | None

    class Config:
        from_attributes = True