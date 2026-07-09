from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.game import Game
from app.schemas.game import GameResponse

router = APIRouter()

@router.get("/games", response_model=list[GameResponse])
def list_games(
    team_id: int | None = Query(None),
    season: int | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Game)
    if team_id:
        query = query.filter(
            (Game.home_team_id == team_id) | (Game.away_team_id == team_id)
        )
    if season:
        query = query.filter(Game.season == season)
    return query.limit(50).all()


@router.get("/games/{game_id}", response_model=GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game