from django.db import models
from pynamodb.models import Model as DynamoModel
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, JSONAttribute


# class TwitchUser(DynamoModel):
#     class Meta:
#         table_name = "observer-urf-users"
#
#     twitch_id = UnicodeAttribute(hash_key=True)
#     twitch_username = UnicodeAttribute()
#     points = NumberAttribute()
#
#
# class CurrentStats(DynamoModel):
#     # spectator sets stats
#     # overlay -> page queries every x seconds??
#
#     class Meta:
#         table_name = "observer-urf-current-stats"
#
#     name = UnicodeAttribute(hash_key=True)  # match-stats, players, banned-champs
#     value = JSONAttribute()

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


class BannedChampions(BaseModel):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name="banned_champions")
    champion = models.CharField(max_length=255)
    order = models.IntegerField()
    team = models.ForeignKey("Team", on_delete=models.CASCADE)


class PostgameStats(BaseModel):
    data = models.TextField()
    complete = models.BooleanField(default=False)


class Game(BaseModel):
    id = models.IntegerField(primary_key=True, editable=False)  # gameId
    game_type = models.IntegerField()  # gameQueueConfigId
    region = models.CharField(max_length=10)  # platformId
    league = models.CharField(max_length=25)
    post_game = models.ForeignKey("PostgameStats", on_delete=models.CASCADE, related_name="game")
