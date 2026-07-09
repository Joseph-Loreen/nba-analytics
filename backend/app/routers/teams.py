from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.team import Team
from app.schemas.team import TeamResponse

router = APIRouter()

@router.get("/teams", response_model=list[TeamResponse])
def list_teams(search: str | None = Query(None), db: Session = Depends(get_db)):
    query = db.query(Team)
    if search:
        query = query.filter((Team.name.ilike(f"%{search}%")) | (Team.full_name.ilike(f"%{search}%")))
    return query.limit(50).all()

@router.get("/teams/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team