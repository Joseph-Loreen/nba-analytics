from pydantic import BaseModel
from app.schemas.team import TeamBasic

class PlayerBasic(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class PlayerResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str | None
    height: str | None
    weight: str | None
    team: TeamBasic | None

    class Config:
        from_attributes = True