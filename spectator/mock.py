import json
import os
from uuid import uuid4

from run import Game, LeagueAPI, start_game


def mock_insert_game(api, seed):
    path = "{}/{}".format("api_data", seed)
    if not os.path.exists(path):
        raise Exception("Seed does not exist")
    for required_file in ["game", "pregame-stats", "postgame-stats"]:
        if not os.path.exists("{}/{}.json".format(path, required_file)):
            raise Exception("Missing {}.json".format(required_file))
    with open("{}/{}".format(path, "game.json"), 'r') as f:
        game = Game(json.load(f), api.api, uuid4().hex)  # use this to get the currentAccountID & get playerHistory
    with open("{}/{}".format(path, "postgame-stats.json"), 'r') as f:
        postgame_stats = json.load(f)
    blacklist_ids = start_game(game, [], postgame_stats=postgame_stats)


if __name__ == '__main__':
    league_api = LeagueAPI("RGAPI-40125f5e-20d1-482b-878f-b85c05b91a7b")
    mock_insert_game(league_api, "fc2de72a75c64a5c9434fc151ae76884")
