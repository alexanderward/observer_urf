import json

import requests
import pprint
from spectator.utils.constants import api_endpoint
from spectator.utils.notify import notify_me


def send_pregame_stats(stats):
    teams = []
    players = []
    for team, item in stats.get("teams").items():
        teams.append({"team_id": int(team), "win_rate": item.get("win_rate")})
        for player in item.get("players"):
            players.append({
                "summoner_name": player.get("summoner"),
                "region": stats.get('region'),
                "champion": player.get("champion"),
                "champion_url": player.get("champion"),
                "hot_streak": player.get("hot_streak"),
                "team_id": int(team),
                "league": player.get("league"),
                "win_rate": player.get("win_rate"),
            })
    data = {
        "id": stats.get('game_id'),
        "game_type": stats.get('game_type'),
        "region": stats.get('region'),
        "league": stats.get('league'),
        "teams": teams,
        "version": stats.get("version"),
        "game_participants": players
    }
    # pprint.pprint(data)
    resp = requests.post(url="{}/api/games/".format(api_endpoint), json=data)
    if resp.status_code != 201:
        notify_me("Unable to create pregame stats")


def send_postgame_stats(stats):
    resp = requests.post(url="{}/api/games/{}/postgame/".format(api_endpoint, stats.get("gameId")),
                         json={"data": json.dumps(stats)})
    print(resp.json())
    if resp.status_code != 200:
        notify_me("Unable to create postagme stats")
