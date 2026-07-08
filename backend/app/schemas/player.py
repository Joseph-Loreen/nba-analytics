from pydantic import BaseModel

class TeamBasic(BaseModel):
    id: int
    name: str
    abbreviation: str

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