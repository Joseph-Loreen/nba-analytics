from pydantic import BaseModel
from app.schemas.team import TeamBasic
from datetime import date as date_type

class GameResponse(BaseModel):
    id: int
    date: date_type
    season: int
    home_score: int | None
    away_score: int | None
    home_team: TeamBasic
    away_team: TeamBasic

    class Config:
        from_attributes = True