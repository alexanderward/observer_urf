from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        abstract = True


class Participant(BaseModel):
    # Will have duplicates so I can store unique matches due to summoners spells and team ids
    summoner_name = models.CharField(max_length=255)
    region = models.CharField(max_length=10)  # platformId
    champion = models.CharField(max_length=255)
    hot_streak = models.BooleanField(default=False)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name="game_participants")
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name="team_participants")
    league = models.CharField(max_length=25)
    win_rate = models.FloatField()


class Team(BaseModel):
    team_id = models.IntegerField()
    win_rate = models.FloatField()
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name="teams")


class PostgameStats(BaseModel):
    data = models.TextField()


class Game(BaseModel):
    id = models.BigIntegerField(primary_key=True, editable=False)  # gameId
    game_type = models.IntegerField()  # gameQueueConfigId
    region = models.CharField(max_length=10)  # platformId
    league = models.CharField(max_length=25)
    postgame = models.ForeignKey("PostgameStats", on_delete=models.CASCADE, related_name="game")
    version = models.CharField(max_length=255)
    seed = models.CharField(max_length=32)
    updated_at = models.DateTimeField(auto_now=True)
    close_bets_at = models.DateTimeField()
    complete = models.BooleanField(default=False)


class BotCommand(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()


class TwitchUserManager(models.Manager):
    def get_or_create(self, username=None, user_id=None):
        obj, created = super().get_or_create(
            username=username,
            user_id=user_id
        )
        return obj


class TwitchUser(BaseModel):
    username = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    balance = models.BigIntegerField(default=1000)
    free_points_game_id = models.BigIntegerField(blank=True, null=True)

    objects = TwitchUserManager()

    def bet(self, game, color, amount):
        if self.balance is None:
            self.balance = 0
        if game.close_bets_at < timezone.now():
            raise ValidationError("{} - Betting is closed for this game.".format(self.username))
        if amount > self.balance:
            raise ValidationError("{} - Insufficient balance.".format(self.username))
        vote, created = Bet.objects.get_or_create(twitch_user=self, game=game, defaults={"amount": amount,
                                                                                         "color": color})
        if not created:
            raise ValidationError("{} has already bet on this match.".format(self.username))
        self.balance -= amount
        self.save()

    def get_free_points(self, game):
        if self.free_points_game_id != game.id:
            if self.balance is None:
                self.balance = 0
            self.balance += 1000
            self.free_points_game_id = game.id
            self.save()
        else:
            raise ValidationError("{} has already earned free points this match. "
                                  " Wait until next match to earn more.".format(self.username))


class Bet(BaseModel):
    twitch_user = models.ForeignKey(TwitchUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="bets")
    color = models.CharField(max_length=255)
    amount = models.BigIntegerField()
    complete = models.BooleanField(default=False)

    def pay_out(self, winning_color):
        if winning_color is None:
            self.twitch_user.balance += self.amount
        elif not self.complete and winning_color.upper() == self.color:
            self.twitch_user.balance += (self.amount * 2)

        self.twitch_user.save()
        self.complete = True
        self.save()
        return self
