from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from app.models import Game, BannedChampions, Team, Participant, PostgameStats


class BaseSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class TeamSerializer(BaseSerializer):
    team_id = serializers.IntegerField()
    win_rate = serializers.FloatField()

    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ('created_at', 'game')


class ParticipantSerializer(BaseSerializer):
    def create(self, validated_data):
        validated_data['team_id'] = validated_data.get('game').teams.get(team_id=validated_data.get("team_id")).id
        return super().create(validated_data)

    summoner_name = serializers.CharField(max_length=255)
    region = serializers.CharField(max_length=10)  # platformId
    champion = serializers.CharField(max_length=255)
    hot_streak = serializers.BooleanField(default=False)

    team = TeamSerializer(read_only=True)
    team_id = serializers.CharField(write_only=True)

    league = serializers.CharField(max_length=25)
    win_rate = serializers.FloatField()

    class Meta:
        model = Participant
        fields = '__all__'
        read_only_fields = ('created_at', 'game')


class BannedChampionSerializer(BaseSerializer):
    def create(self, validated_data):
        validated_data['team_id'] = validated_data.get('game').teams.get(team_id=validated_data.get("team_id")).id
        return super().create(validated_data)

    champion = serializers.CharField(max_length=255)
    order = serializers.IntegerField()

    team = TeamSerializer(read_only=True)
    team_id = serializers.CharField(write_only=True)

    class Meta:
        model = BannedChampions
        fields = '__all__'
        read_only_fields = ('created_at', 'game')


class PostGameSerializer(BaseSerializer):
    data = serializers.CharField()

    class Meta:
        model = PostgameStats
        fields = '__all__'


class GameSerializer(BaseSerializer):

    def create(self, validated_data):
        validated_data['post_game'] = PostgameStats.objects.create(data={})
        return super().create(validated_data)

    id = serializers.IntegerField()
    game_type = serializers.IntegerField()
    region = serializers.CharField(max_length=10)
    league = serializers.CharField(max_length=25)

    teams = TeamSerializer(many=True)
    banned_champions = BannedChampionSerializer(many=True)
    game_participants = ParticipantSerializer(many=True)
    post_game = PostGameSerializer(read_only=True)

    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ('created_at', 'post_game')
