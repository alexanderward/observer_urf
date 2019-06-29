import subprocess

from requests import HTTPError
from riotwatcher import RiotWatcher, ApiError
import pprint
from utils.enums import Region, MatchTypes, Leagues
from utils.misc_functions import get_random_item, sort_list


class LeagueAPI(object):
    regions = Region.get_names()
    leagues = Leagues.get_names()
    match_types = MatchTypes.get_names()
    featured_games = {}

    def __init__(self, key):
        self.api = RiotWatcher(key)
        for match_type in MatchTypes.get_names():
            self.featured_games[match_type] = {region: [] for region in self.regions}
        self.get_featured_games()

    def get_featured_games(self):
        for region in self.regions:
            games = self.api.spectator.featured_games(region)
            for game_ in games['gameList']:
                self.featured_games[MatchTypes.get_name_by_value(game_.get("gameQueueConfigId"))][region].append(game_)

        # Sort by timestamp descending
        for region in self.regions:
            for match_type in MatchTypes.get_names():
                self.featured_games[match_type][region] = sort_list(self.featured_games[match_type][region],
                                                                    'gameStartTime',
                                                                    descending=True)

    def find_game(self):
        game_rankings = {league: [] for league in self.leagues}

        for region in self.regions:
            for match_type in [x for x in [MatchTypes.RANKED_5V5_SOLO.name,
                                           MatchTypes.RANKED_5V5_FLEX.name,
                                           MatchTypes.NORMAL_5V5_BLIND_PICK.name]]:
                if self.featured_games[match_type][region]:
                    for game_ in self.featured_games[match_type][region]:
                        try:
                            summoner = self.api.summoner.by_name(region, game_['participants'][0]['summonerName'])
                            if not summoner:
                                continue
                            resp = self.api.league.by_summoner(region, summoner['id'])
                            if not resp:
                                continue
                            game_rankings[resp[0]['tier']].append(game_)
                        except HTTPError:
                            continue
            for league in self.leagues:
                if game_rankings[league]:
                    return game_rankings[league][0]
        for region in self.regions:
            for match_type in [x for x in [MatchTypes.NORMAL_3V3_BLIND_PICK.name,
                                           MatchTypes.RANKED_3V3_FLEX.name,
                                           MatchTypes.ARAM.name]]:
                if self.featured_games[match_type][region]:
                    return get_random_item(self.featured_games[match_type][region])

    def spectate(self, game):
        from utils.enums import SpectatorGrid
        url, port = SpectatorGrid[game['platformId']].value
        subprocess.run(r'cd "C:\Riot Games\League of Legends\Game" && "League of Legends.exe" "8394" '
                       r'"LeagueClient.exe" "" "' \
                       r'spectator {}:{} {} {} {}" "-UseRads"'.format(url, port,
                                                                      game['observers']['encryptionKey'],
                                                                      game['gameId'], game['platformId']),
                       shell=True)


def run():
    api = LeagueAPI("RGAPI-c68037fc-1718-4186-a60b-5b7b897ac757")
    game = api.find_game()
    pprint.pprint(game)
    api.spectate(game)


if __name__ == "__main__":
    # import timeit
    # print(timeit.timeit("run()", setup="from __main__ import run", number=1))
    run()
