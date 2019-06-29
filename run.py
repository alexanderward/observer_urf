import pprint
import subprocess
import sys
import time

import keyboard
from requests import HTTPError
from riotwatcher import RiotWatcher

from utils.enums import Region, MatchTypes, Leagues
from utils.misc_functions import get_random_item, sort_list
from utils.threading import RepeatedTimer


class Game(object):
    def __init__(self, game, api):
        self.game = game
        self.api = api
        self.proc = None
        self.hud_view_toggle = RepeatedTimer(30, lambda: keyboard.send("x"))

    def spectate(self):
        from utils.enums import SpectatorGrid
        url, port = SpectatorGrid[self.game['platformId']].value
        cmd = r'cd "C:\Riot Games\League of Legends\Game" && "League of Legends.exe" "8394" ' \
              r'"LeagueClient.exe" "" "' \
              r'spectator {}:{} {} {} {}" "-UseRads"'.format(url, port,
                                                             self.game['observers']['encryptionKey'],
                                                             self.game['gameId'], self.game['platformId'])

        self.proc = subprocess.Popen(cmd,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE,
                                     shell=True)
        for line in iter(self.proc.stdout.readline, b''):
            decoded = line.decode(sys.stdout.encoding)
            print(decoded)

            if "Failed to connect" in decoded or \
                    "Finished Play game" in decoded or \
                    "Process Force Terminating" in decoded:
                return self.kill(error=True)

            elif "SetEndOfGameVideoActive" in decoded:
                return self.kill()

            elif "GAMESTATE_GAMELOOP EndRender & EndFrame" in decoded:
                # Sets up UI
                keyboard.send('o')
                keyboard.send('n')
                keyboard.send('u')
                keyboard.send('d')
                self.hud_view_toggle.start()

    def kill(self, error=False):
        if self.proc:
            if self.hud_view_toggle.is_running:
                self.hud_view_toggle.stop()
                time.sleep(.5)  # A small buffer so we don't get keystrokes after proc ends
            subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.proc.pid))
        return error

    def get_stats(self):
        stats = None
        while not stats:
            try:
                stats = self.api.match.by_id(self.game.get('platformId'), self.game.get('gameId'))
            except Exception as e:
                print("Stats not ready yet.  Waiting 5 seconds. Error: {}".format(str(e)))
                time.sleep(5)
        pprint.pprint(stats)


class LeagueAPI(object):
    regions = Region.get_names()
    leagues = Leagues.get_names()
    match_types = MatchTypes.get_names()
    featured_games = {}

    def __init__(self, key):
        self.api = RiotWatcher(key)

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
        for match_type in MatchTypes.get_names():
            self.featured_games[match_type] = {region: [] for region in self.regions}
        self.get_featured_games()

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
                    return Game(game_rankings[league][0], self.api)
        for region in self.regions:
            for match_type in [x for x in [MatchTypes.NORMAL_3V3_BLIND_PICK.name,
                                           MatchTypes.RANKED_3V3_FLEX.name,
                                           MatchTypes.ARAM.name]]:
                if self.featured_games[match_type][region]:
                    return Game(get_random_item(self.featured_games[match_type][region]), self.api)


def run():
    api = LeagueAPI("RGAPI-c68037fc-1718-4186-a60b-5b7b897ac757")
    # while True:
    game = api.find_game()
    pprint.pprint(game.game)

    error = game.spectate()
    if not error:
        game.get_stats()
    # print("Waiting a minute")
    # time.sleep(60)


if __name__ == "__main__":
    # import timeit
    # print(timeit.timeit("run()", setup="from __main__ import run", number=1))
    run()
