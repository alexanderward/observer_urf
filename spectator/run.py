import json
import pprint
import subprocess
import sys
import time

import keyboard
import requests
from requests import HTTPError
from riotwatcher import RiotWatcher

from spectator.utils.enums import Region, MatchTypes, Leagues
from spectator.utils.misc_functions import get_random_item, sort_list
from spectator.utils.interval import RepeatedTimer
from spectator.utils.rest_api import send_pregame_stats, send_postgame_stats


class Game(object):
    champions = {}

    def __init__(self, game, api):
        self.version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
        champions_data = requests.get("https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json"
                                      "".format(self.version)).json()
        for key, value in champions_data['data'].items():
            self.champions[value["key"]] = value
        self.game = game
        self.api = api
        self.proc = None
        self.hud_view_toggle = RepeatedTimer(30, lambda: keyboard.send("x"))

    def spectate(self):
        from spectator.utils.enums import SpectatorGrid
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
                # self.hud_view_toggle.start()

    def kill(self, error=False):
        if self.proc:
            if self.hud_view_toggle.is_running:
                self.hud_view_toggle.stop()
                time.sleep(.5)  # A small buffer so we don't get keystrokes after proc ends
            subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.proc.pid))
        return error

    def send_postgame_stats(self, stats=None):
        while not stats:
            try:
                stats = self.api.match.by_id(self.game.get('platformId'), self.game.get('gameId'))
            except Exception as e:
                print("Stats not ready yet.  Waiting 5 seconds. Error: {}".format(str(e)))
                time.sleep(5)
        send_postgame_stats(stats)

    def send_pregame_stats(self):
        # Can use these details as a bot command since participants not in rendered order
        # team 200  = bottom loading / red team / top side
        # team 100 = top loading / blue team / bottom side

        teams = {100: dict(players=[], win_rate=None),
                 200: dict(players=[], win_rate=None)}
        highest_league = None

        leagues = Leagues.get_names()
        for participant in self.game['participants']:
            summoner = self.api.summoner.by_name(self.game.get("platformId"), participant.get("summonerName"))
            player_stats = self.api.league.by_summoner(self.game.get("platformId"), summoner.get("id"))[0]
            win_rate = (float(player_stats["wins"]) / float(player_stats["losses"] + player_stats["wins"])) * 100
            champion = self.champions[str(participant['championId'])]
            player = dict(league=player_stats["tier"],
                          summoner=summoner['name'], win_rate=win_rate,
                          champion=champion['name'],
                          hot_streak=player_stats["hotStreak"])
            teams[participant.get('teamId')]['players'].append(player)
            if teams[participant.get('teamId')]['win_rate'] is None:
                teams[participant.get('teamId')]['win_rate'] = win_rate
            else:
                tmp = [teams[participant.get('teamId')]['win_rate'], win_rate]
                teams[participant.get('teamId')]['win_rate'] = sum(tmp) / len(tmp)
            if highest_league is None:
                highest_league = Leagues[player_stats["tier"]].name
            else:
                index = leagues.index(highest_league)
                new_index = leagues.index(player_stats["tier"])
                if new_index < index:
                    highest_league = Leagues[player_stats["tier"]].name

        stats = {"league": highest_league,
                 "teams": teams,
                 "region": self.game['platformId'],
                 "game_id": self.game.get("gameId"),
                 "game_type": self.game.get("gameQueueConfigId"),
                 "version": self.version
                 }
        send_pregame_stats(stats)


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


def run(debug=False):
    api = LeagueAPI("RGAPI-c1fc6855-8e6d-40e9-92c8-2311f650f58b")

    if not debug:
        while True:
            game = api.find_game()
            game.send_pregame_stats()
            error = game.spectate()
            if not error:
                game.send_postgame_stats()
            # break
            # print("Waiting a minute")
            # time.sleep(60)
    else:
        with open("notes/game.json", 'r') as f:
            game = Game(json.load(f), api.api)  # use this to get the currentAccountID & get playerHistory
        # game.send_pregame_stats()

        with open("notes/match_stats.json", 'r') as f:
            game.send_postgame_stats(json.load(f))


if __name__ == "__main__":
    # import timeit
    # print(timeit.timeit("run()", setup="from __main__ import run", number=1))
    run(debug=False)
