from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.player_game_stats import PlayerGameStats
from app.schemas.player_game_stats import PlayerGameStatsResponse

router = APIRouter()

@router.get("/stats", response_model=list[PlayerGameStatsResponse])
def list_stats(
    player_id: int | None = Query(None),
    game_id: int | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(PlayerGameStats)
    if player_id:
        query = query.filter(PlayerGameStats.player_id == player_id)
    if game_id:
        query = query.filter(PlayerGameStats.game_id == game_id)
    return query.limit(100).all()