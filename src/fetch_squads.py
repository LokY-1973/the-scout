import requests
import json
import time
import os

API_KEY = os.getenv("FOOTBALL_API_KEY") or open(".env").read().split("=")[1].strip()

HEADERS = {"X-Auth-Token": API_KEY}

LEAGUES = {
    "Premier League":    "PL",
    "La Liga":           "PD",
    "Bundesliga":        "BL1",
    "Serie A":           "SA",
    "Ligue 1":           "FL1",
}

def fetch_teams(league_code):
    url = f"https://api.football-data.org/v4/competitions/{league_code}/teams"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(f"  Error {r.status_code}: {r.text}")
        return []
    return r.json().get("teams", [])

def fetch_squad(team_id):
    url = f"https://api.football-data.org/v4/teams/{team_id}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return []
    return r.json().get("squad", [])

def build_database():
    database = {}

    for league_name, code in LEAGUES.items():
        print(f"\n── {league_name} ──")
        teams = fetch_teams(code)
        print(f"  {len(teams)} teams found")
        time.sleep(7)

        for team in teams:
            team_name = team["name"]
            team_id   = team["id"]
            print(f"  Fetching squad: {team_name}")

            squad = fetch_squad(team_id)
            time.sleep(7)

            database[team_name] = {
                "league":     league_name,
                "team_id":    team_id,
                "crest":      team.get("crest", ""),
                "formation":  None,
                "squad": [
                    {
                        "name":        p.get("name"),
                        "position":    p.get("position"),
                        "nationality": p.get("nationality"),
                        "age":         2026 - int(p["dateOfBirth"][:4]) if p.get("dateOfBirth") else None,
                    }
                    for p in squad
                ]
            }

    with open("data/squads.json", "w") as f:
        json.dump(database, f, indent=2)

    print(f"\n✅ Done! {len(database)} teams saved to data/squads.json")

if __name__ == "__main__":
    build_database()