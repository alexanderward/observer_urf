import json
import time
from functools import wraps

import requests
import pprint
from spectator.utils.constants import api_endpoint
from spectator.utils.gmail import send_email


def wakeup_rds(func):
    @wraps(func)
    def function_wrapper(x):
        status_code = None
        while status_code is not 200:
            resp = requests.get(url="{}/api/bot-commands/text-list/".format(api_endpoint))
            status_code = resp.status_code
            if status_code is not 200:
                time.sleep(1)
        return func(x)

    return function_wrapper


@wakeup_rds
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
        "game_participants": players,
        "seed": stats.get("seed")
    }
    resp = requests.post(url="{}/api/games/".format(api_endpoint), json=data)
    if resp.status_code != 201 and "Game already Exists" not in resp.text:
        send_email("Failed to send pregame stats", {
            "url": "{}/api/games/".format(api_endpoint),
            "data": data,
            "response": resp.json()
        })


@wakeup_rds
def send_postgame_stats(stats):
    resp = requests.post(url="{}/api/games/{}/postgame/".format(api_endpoint, stats.get("gameId")),
                         json={"data": json.dumps(stats)})
    if resp.status_code != 200:
        send_email("Failed to send postgame stats", {
            "url": "{}/api/games/{}/postgame/".format(api_endpoint, stats.get("gameId")),
            "data": stats,
            "response": resp.json()
        })
