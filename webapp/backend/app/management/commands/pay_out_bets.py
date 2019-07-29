from django.core.management.base import BaseCommand
import logging
from app.models import Game

logger = logging.getLogger()
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


class Command(BaseCommand):
    help = 'Pay out bets'

    def add_arguments(self, parser):
        parser.add_argument('game_id', type=int)
        parser.add_argument('winning_team_id', type=int)
        parser.add_argument(
            '--complete_games',
            action='store_true',
            help='Completes all games',
        )

    def handle(self, *args, **kwargs):
        game_id = kwargs.get('game_id')
        game = Game.objects.get(pk=game_id)
        winner = "red" if kwargs.get("winning_team_id") == 200 else "blue"
        for bet in game.bets.all().iterator():
            logger.info("Balancing wager for: {}".format(bet.twitch_user.username))
            bet.pay_out(winner)
        if kwargs.get('complete_games'):
            for game in Game.objects.filter(complete=False).all().iterator():
                logger.info("Incomplete game found.  Refunding all wagers for game: {}".format(game.id))
                game.complete = True
                for bet in game.bets.all().iterator():
                    bet.pay_out(winning_color=None)
                game.save()
