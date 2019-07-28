import json
import os
import subprocess
import sys
import time
import traceback
from uuid import uuid4

import keyboard
import requests
from requests import HTTPError
from riotwatcher import RiotWatcher

from utils.spotify import Spotify
from utils.enums import Region, MatchTypes, Leagues
from utils.misc_functions import get_random_item, sort_list
from utils.interval import RepeatedTimer
from utils.rest_api import send_pregame_stats, send_postgame_stats, wakeup_rds
import simplejson
import logging

logger = logging.getLogger("spectator")
logger.setLevel(logging.DEBUG)
logger.propagate = False

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def format_message(seed, message):
    return "Seed:{} - {}".format(seed, message)


def save_fetched_data(name, seed, data, subfolder=None):
    folder = "{}/{}".format("api_data", seed)
    if not os.path.exists(folder):
        os.mkdir(folder)
    if subfolder:
        folder = "{}/{}".format(folder, subfolder)
        if not os.path.exists(folder):
            os.mkdir(folder)

    filename = "{}/{}.json".format(folder, name)
    logger.info(format_message(seed, "Saving data for {} to {}".format(name, filename)))
    with open(filename, 'w') as f:
        f.write(simplejson.dumps(simplejson.loads(simplejson.dumps(data)), indent=4, sort_keys=True))


class Game(object):
    champions = {}

    def __init__(self, game, api, seed):
        self.seed = seed
        logger.info(format_message(self.seed, "Game found: {}".format(game['gameId'])))
        save_fetched_data("game", seed, game)
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
        from utils.enums import SpectatorGrid
        url, port = SpectatorGrid[self.game['platformId']].value
        cmd = r'cd "C:\Riot Games\League of Legends\Game" && "League of Legends.exe" "8394" ' \
              r'"LeagueClient.exe" "" "' \
              r'spectator {}:{} {} {} {}" "-UseRads"'.format(url, port,
                                                             self.game['observers']['encryptionKey'],
                                                             self.game['gameId'], self.game['platformId'])

        logger.info(format_message(self.seed, "Starting spectator mode for game: {}".format(self.game['gameId'])))

        self.proc = subprocess.Popen(cmd,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE,
                                     shell=True)
        for line in iter(self.proc.stdout.readline, b''):
            decoded = line.decode(sys.stdout.encoding)
            # print(decoded)

            if "Failed to connect" in decoded or \
                    "Finished Play game" in decoded or \
                    "Process Force Terminating" in decoded:
                logging.info(format_message(self.seed, "Game {} terminated.  Reason: {}".format(self.game['gameId'],
                                                                                                decoded)))
                return self.kill(error=True)

            elif "SetEndOfGameVideoActive" in decoded:
                logging.info(format_message(self.seed, "Game {} ended.  Reason: {}".format(self.game['gameId'],
                                                                                           decoded)))
                return self.kill()

            elif "GAMESTATE_GAMELOOP EndRender & EndFrame" in decoded:
                logger.info(format_message(self.seed, "Game {} started.  Pausing music and setting up"
                                                      " UI".format(self.game['gameId'])))
                Spotify.pause()
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
            self.send_postgame_stats()
            logger.info(format_message(self.seed, "Game {} ended.  Exiting spectator mode".format(self.game['gameId'])))
            subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.proc.pid))
        time.sleep(1)  # small buffer needed for window to close
        logger.info(format_message(self.seed, "Starting music"))
        Spotify.next()
        return error

    def send_postgame_stats(self, stats=None):
        while not stats:
            try:
                logger.info(format_message(self.seed, "Retrieving postgame "
                                                      "stats for game: {}".format(self.game['gameId'])))
                stats = self.api.match.by_id(self.game.get('platformId'), self.game.get('gameId'))
            except Exception as e:
                logger.warning(format_message(self.seed, "Stats not ready yet.  "
                                                         "Waiting 5 seconds. Error: {}".format(str(e))))
                time.sleep(5)
        logger.info(format_message(self.seed, "Sending postgame stats for game: {}".format(self.game['gameId'])))
        save_fetched_data("postgame-stats", self.seed, stats)
        send_postgame_stats(stats)

    def send_pregame_stats(self):
        # Can use these details as a bot command since participants not in rendered order
        # team 200  = bottom loading / red team / top side
        # team 100 = top loading / blue team / bottom side

        teams = {100: dict(players=[], win_rate=None),
                 200: dict(players=[], win_rate=None)}
        highest_league = None

        leagues = Leagues.get_names()
        logger.info(format_message(self.seed, "Generating pregame stats for game: {}".format(self.game['gameId'])))
        for participant in self.game['participants']:
            logger.info(format_message(self.seed, "Participant: {}".format(participant.get("summonerName"))))
            summoner = self.api.summoner.by_name(self.game.get("platformId"), participant.get("summonerName"))
            save_fetched_data(participant.get("summonerName"), self.seed, summoner, subfolder="summoner")
            player_stats = self.api.league.by_summoner(self.game.get("platformId"), summoner.get("id"))
            save_fetched_data("{}-stats".format(participant.get("summonerName")), self.seed,
                              player_stats, subfolder="summoner")
            player_stats = player_stats[0]
            win_rate = (float(player_stats["wins"]) / float(player_stats["losses"] + player_stats["wins"])) * 100
            champion = self.champions[str(participant['championId'])]
            player = dict(league=player_stats["tier"],
                          summoner=summoner['name'], win_rate=win_rate,
                          champion=champion['id'],
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
                 "version": self.version,
                 "seed": self.seed}
        save_fetched_data("pregame-stats", self.seed, stats)
        logger.info(format_message(self.seed, "Sending pregame stats for game: {}".format(self.game['gameId'])))
        send_pregame_stats(stats)


class LeagueAPI(object):
    regions = Region.get_names()
    leagues = Leagues.get_names()
    match_types = MatchTypes.get_names()
    featured_games = {}

    def __init__(self, key):
        self.api = RiotWatcher(key)
        self.seed = None

    def update_seed(self):
        self.seed = uuid4().hex

    def get_featured_games(self, blacklist_ids):
        logger.info(format_message(self.seed, "Generating featured games list"))
        for region in self.regions:
            games = self.api.spectator.featured_games(region)
            for game_ in games['gameList']:
                if game_['gameId'] not in blacklist_ids:
                    self.featured_games[MatchTypes.get_name_by_value(game_.
                                                                     get("gameQueueConfigId"))][region].append(game_)

        # Sort by timestamp descending
        for region in self.regions:
            for match_type in MatchTypes.get_names():
                self.featured_games[match_type][region] = sort_list(self.featured_games[match_type][region],
                                                                    'gameStartTime',
                                                                    descending=True)

    def find_game(self, blacklist_ids=None):
        self.update_seed()
        logger.info(format_message(self.seed, "Searching for game."))
        if blacklist_ids is None:
            blacklist_ids = []
        for match_type in MatchTypes.get_names():
            self.featured_games[match_type] = {region: [] for region in self.regions}
        self.get_featured_games(blacklist_ids)

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
                    return Game(game_rankings[league][0], self.api, self.seed)
        for region in self.regions:
            for match_type in [x for x in [MatchTypes.NORMAL_3V3_BLIND_PICK.name,
                                           MatchTypes.RANKED_3V3_FLEX.name,
                                           MatchTypes.ARAM.name]]:
                if self.featured_games[match_type][region]:
                    return Game(get_random_item(self.featured_games[match_type][region]), self.api, self.seed)


def start_game(game, blacklist_ids, mock=False):
    try:
        game.send_pregame_stats()
        if not mock:
            error = game.spectate()
            logger.info("Intermission - Waiting ~2 minutes")
            time.sleep(180)
        else:
            game.send_postgame_stats()
        blacklist_ids = []
    except:
        logger.error(format_message(game.seed, "Something went wrong.  Blacklisting ID for game"
                                               ": {}.".format(game.game['gameId'])))
        logger.error(format_message(game.seed, traceback.format_exc()))
        blacklist_ids.append(game.game['gameId'])
    return blacklist_ids


def run():
    api = LeagueAPI("RGAPI-40125f5e-20d1-482b-878f-b85c05b91a7b")
    blacklist_ids = []
    while True:
        game = api.find_game(blacklist_ids)
        blacklist_ids = start_game(game, blacklist_ids)


if __name__ == "__main__":
    run()
