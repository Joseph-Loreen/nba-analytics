from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.player import Player
from app.schemas.player import PlayerResponse

router = APIRouter()

@router.get("/players", response_model=list[PlayerResponse])
def list_players(search: str | None = Query(None), db: Session = Depends(get_db)):
    query = db.query(Player)
    if search:
        query = query.filter((Player.first_name.ilike(f"%{search}%")) |(Player.last_name.ilike(f"%{search}%")))
    return query.limit(50).all()


@router.get("/players/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player