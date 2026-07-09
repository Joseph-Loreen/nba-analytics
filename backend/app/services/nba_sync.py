import os
import time
from urllib import response
import requests
from dotenv import load_dotenv
from datetime import datetime
from app.models.game import Game
from app.database import SessionLocal
from app.models.team import Team
from app.models.player import Player
from app.models.player_game_stats import PlayerGameStats

load_dotenv()

API_KEY = os.getenv("BALLDONTLIE_API_KEY")
BASE_URL = "https://api.balldontlie.io/nba/v1"

headers = {
    "Authorization": API_KEY
}


def sync_teams():
    db = SessionLocal()
    response = requests.get(f"{BASE_URL}/teams", headers=headers)
    data = response.json()["data"]

    created_count = 0
    updated_count = 0

    for team_data in data:
        conference = (team_data.get("conference") or "").strip()
        division = (team_data.get("division") or "").strip()

        existing = db.query(Team).filter(Team.id == team_data["id"]).first()

        if existing:
            existing.name = team_data["name"]
            existing.full_name = team_data["full_name"]
            existing.city = team_data["city"]
            existing.abbreviation = team_data["abbreviation"]
            existing.conference = conference
            existing.division = division
            updated_count += 1
        else:
            team = Team(
                id=team_data["id"],
                name=team_data["name"],
                full_name=team_data["full_name"],
                city=team_data["city"],
                abbreviation=team_data["abbreviation"],
                conference=conference,
                division=division,
            )
            db.add(team)
            created_count += 1

    db.commit()
    db.close()
    print(f"Teams: {created_count} created, {updated_count} updated.")


def sync_players():
    db = SessionLocal()
    page_cursor = None
    created_count = 0
    updated_count = 0

    while True:
        params = {"per_page": 100}
        if page_cursor:
            params["cursor"] = page_cursor

        response = requests.get(f"{BASE_URL}/players", headers=headers, params=params)

        if response.status_code == 429:
            print("Rate limited. Waiting 15 seconds...")
            time.sleep(15)
            continue

        result = response.json()
        players_data = result["data"]

        for p in players_data:
            team_id = p["team"]["id"] if p.get("team") else None

            existing = db.query(Player).filter(Player.id == p["id"]).first()

            if existing:
                existing.first_name = p["first_name"]
                existing.last_name = p["last_name"]
                existing.position = p.get("position")
                existing.height = p.get("height")
                existing.weight = p.get("weight")
                existing.college = p.get("college")
                existing.country = p.get("country")
                existing.team_id = team_id
                updated_count += 1
            else:
                player = Player(
                    id=p["id"],
                    first_name=p["first_name"],
                    last_name=p["last_name"],
                    position=p.get("position"),
                    height=p.get("height"),
                    weight=p.get("weight"),
                    college=p.get("college"),
                    country=p.get("country"),
                    team_id=team_id,
                )
                db.add(player)
                created_count += 1

        db.commit()

        page_cursor = result.get("meta", {}).get("next_cursor")
        if not page_cursor:
            break

        time.sleep(13)

    db.close()
    print(f"Players: {created_count} created, {updated_count} updated.")

def sync_games(season: int = 2025):
    db = SessionLocal()
    page_cursor = None
    created_count = 0
    updated_count = 0

    while True:
        params = {"seasons[]": season, "per_page": 100}
        if page_cursor:
            params["cursor"] = page_cursor

        response = requests.get(f"{BASE_URL}/games", headers=headers, params=params)

        if response.status_code == 429:
            print("Rate limited. Waiting 15 seconds...")
            time.sleep(15)
            continue

        result = response.json()
        games_data = result["data"]

        for g in games_data:
            game_date = datetime.strptime(g["date"][:10], "%Y-%m-%d").date()

            existing = db.query(Game).filter(Game.id == g["id"]).first()

            if existing:
                existing.date = game_date
                existing.season = g["season"]
                existing.home_score = g["home_team_score"]
                existing.away_score = g["visitor_team_score"]
                existing.home_team_id = g["home_team"]["id"]
                existing.away_team_id = g["visitor_team"]["id"]
                updated_count += 1
            else:
                game = Game(
                    id=g["id"],
                    date=game_date,
                    season=g["season"],
                    home_score=g["home_team_score"],
                    away_score=g["visitor_team_score"],
                    home_team_id=g["home_team"]["id"],
                    away_team_id=g["visitor_team"]["id"],
                )
                db.add(game)
                created_count += 1

        db.commit()

        page_cursor = result.get("meta", {}).get("next_cursor")
        if not page_cursor:
            break

        time.sleep(13)

    db.close()
    print(f"Games ({season} season): {created_count} created, {updated_count} updated.")

def sync_player_stats(season: int = 2025):
    db = SessionLocal()
    page_cursor = None
    created_count = 0
    updated_count = 0

    while True:
        params = {"seasons[]": season, "per_page": 100}
        if page_cursor:
            params["cursor"] = page_cursor

        response = requests.get(f"{BASE_URL}/stats", headers=headers, params=params)

        if response.status_code == 429:
            print("Rate limited. Waiting 15 seconds...")
            time.sleep(15)
            continue
        result = response.json()
        stats_data = result["data"]

        for s in stats_data:
            player_id = s["player"]["id"]
            game_id = s["game"]["id"]

            # skip if the player or game doesn't exist locally
            player_exists = db.query(Player).filter(Player.id == player_id).first()
            game_exists = db.query(Game).filter(Game.id == game_id).first()
            if not player_exists or not game_exists:
                continue

            existing = db.query(PlayerGameStats).filter(
                PlayerGameStats.player_id == player_id,
                PlayerGameStats.game_id == game_id
            ).first()

            if existing:
                existing.points = s.get("pts", 0)
                existing.rebounds = s.get("reb", 0)
                existing.assists = s.get("ast", 0)
                existing.steals = s.get("stl", 0)
                existing.blocks = s.get("blk", 0)
                existing.turnovers = s.get("turnover", 0)
                existing.minutes_played = _parse_minutes(s.get("min"))
                updated_count += 1
            else:
                stat = PlayerGameStats(
                    player_id=player_id,
                    game_id=game_id,
                    points=s.get("pts", 0),
                    rebounds=s.get("reb", 0),
                    assists=s.get("ast", 0),
                    steals=s.get("stl", 0),
                    blocks=s.get("blk", 0),
                    turnovers=s.get("turnover", 0),
                    minutes_played=_parse_minutes(s.get("min")),
                )
                db.add(stat)
                created_count += 1

        db.commit()

        page_cursor = result.get("meta", {}).get("next_cursor")
        if not page_cursor:
            break

        time.sleep(13)

    db.close()
    print(f"Player stats ({season} season): {created_count} created, {updated_count} updated.")


def _parse_minutes(min_str):
    """Convert balldontlie's 'MM:SS' minutes string into a float, e.g. '34:12' -> 34.2"""
    if not min_str or ":" not in min_str:
        return None
    try:
        minutes, seconds = min_str.split(":")
        return round(int(minutes) + int(seconds) / 60, 2)
    except (ValueError, AttributeError):
        return None

if __name__ == "__main__":
    import sys

    # In the command lien you can specify which data to sync: teams, players, or games. 
    # If no argument is provided it will sync all three.
    # If theres another command line argument with games so games 2025 it will sync games for that season.
    if len(sys.argv) > 1:
        target = sys.argv[1]

        if target == "teams":
            sync_teams()
        elif target == "players":
            sync_players()
        elif target == "games":
            season = int(sys.argv[2]) if len(sys.argv) > 2 else 2025
            sync_games(season=season)
        elif target == "stats":
            season = int(sys.argv[2]) if len(sys.argv) > 2 else 2025
            sync_player_stats(season=season)
        else:
            print(f"Unknown target: {target}")
    else:
        sync_teams()
        sync_players()
        sync_games(season=2025)
        sync_player_stats(season=2025)