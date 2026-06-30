import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine
from app.models import team, player, game, player_game_stats

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")