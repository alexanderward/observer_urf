import json
import os
from uuid import uuid4

from run import Game, LeagueAPI, start_game


def mock_insert_game(api, seed):
    path = "{}/{}".format("api_data", seed)
    if not os.path.exists(path):
        raise Exception("Seed does not exist")
    for required_file in ["game", "pregame-stats"]:#, "postgame-stats"]:
        if not os.path.exists("{}/{}.json".format(path, required_file)):
            raise Exception("Missing {}.json".format(required_file))
    with open("{}/{}".format(path, "game.json"), 'r') as f:
        game = Game(json.load(f), api.api, uuid4().hex)  # use this to get the currentAccountID & get playerHistory
    blacklist_ids = start_game(game, [], mock=True)


if __name__ == '__main__':
    league_api = LeagueAPI("RGAPI-40125f5e-20d1-482b-878f-b85c05b91a7b")
    mock_insert_game(league_api, "230c436756aa4d57846bb8b72b90351d")
