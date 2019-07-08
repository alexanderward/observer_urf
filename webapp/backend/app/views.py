import json
from urllib.parse import quote_plus

from django.http import JsonResponse
from django.http.response import Http404
from django.utils import timezone
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet

from app.models import Game, BotCommand, TwitchUser
from app.serializers import GameSerializer, PostGameSerializer, BotCommandSerializer


class GameViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):

    queryset = Game.objects.select_related('postgame'). \
        prefetch_related('bets')
    serializer_class = GameSerializer
    ordering_fields = '__all__'
    ordering = ('updated_at',)

    def get_latest_game(self):
        return self.queryset.order_by('-updated_at').first()

    # todo - abstract creates and put all behind auth
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['GET'], url_path='latest')
    def most_recent(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        game = self.get_latest_game()
        data = serializer(game).data
        return JsonResponse(data)

    @action(detail=False, methods=['GET'], url_path='odds')
    def odds(self, request, *args, **kwargs):
        game = self.get_latest_game()
        data = dict(total=dict(blue=0, red=0), percentage=dict(blue=50, red=50))
        for bet in game.bets.all().iterator():
            data['total'][bet.color.lower()] += bet.amount
        total = data['total']['red'] + data['total']['blue']
        if total:
            data['percentage']['red'] = (data['total']['red']/ total) * 100
            data['percentage']['blue'] = (data['total']['blue']/ total) * 100
        return JsonResponse(data)

    @action(detail=True, methods=['POST'], url_path='postgame')
    def postgame_stats_create(self, request, *args, **kwargs):
        PostGameSerializer(data=request.data).is_valid(raise_exception=True)

        game = self.get_object()
        game.postgame.data = request.data['data']
        game.postgame.complete = True
        game.postgame.save()
        game.save()
        data = json.loads(request.data['data'])
        [x.pay_out("red" if [x for x in data['teams'] if x['win'] == 'Win'][0]['teamId'] == 200 else "blue") for x in
         game.bets.all()]
        serializer = self.get_serializer_class()
        return JsonResponse(serializer(game).data)


class BotCommandsViewSet(mixins.ListModelMixin,
                         GenericViewSet):
    queryset = BotCommand.objects.all()
    serializer_class = BotCommandSerializer
    ordering_fields = '__all__'
    ordering = ('created_at',)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['GET'], url_path='text-list')
    def text_list(self, request, *args, **kwargs):
        commands = []
        for command in self.queryset.all().iterator():
            commands.append("[ {} - {} ]".format(command.name, command.description))
        data = {"commands": ",".join(commands)}
        return JsonResponse(data)

    @action(detail=False, methods=['GET'], url_path='free')
    def free(self, request, *args, **kwargs):
        user = TwitchUser.objects.get_or_create(user_id=request.GET.get("user_id"),
                                                username=request.GET.get("username"))
        game = Game.objects.order_by('-updated_at').first()
        try:
            user.get_free_points(game)
            message = "{} has successfully earned free points.  New balance is {}".format(user.username, user.balance)
        except Exception as e:
            message = "{}".format(e.detail[0].__str__())

        return JsonResponse({"message": message})

    @action(detail=False, methods=['GET'], url_path='bet')
    def bet(self, request, *args, **kwargs):
        color = request.GET.get("color")
        color = color.upper()
        if color not in ["RED", "BLUE"]:
            message = "{} is not a valid team. Use: !red <amount> or !blue <amount>".format(color.title())
        else:
            try:
                username = request.GET.get("username")
                user_id = request.GET.get("user_id")
                amount = request.GET.get("amount", "").split()[0]
                try:
                    amount = int(amount)
                except ValueError:
                    raise ValidationError("Amount must be a number")
                game = Game.objects.order_by('-updated_at').first()
                user = TwitchUser.objects.get_or_create(user_id=user_id, username=username)
                user.bet(game, color, amount)
                message = "{} has successfully wagered {} on the {} team. Current balance: {}".format(username,
                                                                                                      amount,
                                                                                                      color.title(),
                                                                                                      user.balance)
            except Exception as e:
                message = "{}".format(e.detail[0].__str__())
        return JsonResponse({"message": message})

    @action(detail=False, methods=['GET'], url_path='balance')
    def get_stats(self, request, *args, **kwargs):
        user = TwitchUser.objects.get_or_create(user_id=request.GET.get("user_id"),
                                                username=request.GET.get("username"))
        return JsonResponse({"message": "{}'s balance: {}".format(user.username, user.balance)})

    @action(detail=False, methods=['GET'], url_path='game-info')
    def get_game_info(self, request, *args, **kwargs):
        game = Game.objects.order_by('-updated_at').first()
        if not game:
            raise Http404
        participant = game.game_participants.first()
        regions = {
            "NA1": "na",
            "EUN1": "eune",
            "EUW1": "euw",
            "KR": "kr",
            "LA1": "lan",
            "LA2": "las",
            "BR1": "br",
            "OC1": "oce",
            "JP1": "jp",
            "RU": "ru",
            "TR1": "tr"
        }
        url = "https://ezre.al/live/{}/{}?utm_source=observerurf".format(regions[participant.region],
                                                                         quote_plus(participant.summoner_name))
        return JsonResponse({"url": url})
