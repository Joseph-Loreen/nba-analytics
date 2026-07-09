from pydantic import BaseModel

class TeamBasic(BaseModel):
    id: int
    name: str
    abbreviation: str

    class Config:
        from_attributes = True
        
class TeamResponse(BaseModel):
    id: int
    name: str
    abbreviation: str
    city: str
    full_name: str
    conference: str | None
    division: str | None

    class Config:
        from_attributes = True
