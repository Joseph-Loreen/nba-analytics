import os
import time
import requests
from dotenv import load_dotenv
from app.database import SessionLocal
from app.models.team import Team
from app.models.player import Player

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


if __name__ == "__main__":
    sync_teams()
    sync_players()