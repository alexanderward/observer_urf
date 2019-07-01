from django.http import JsonResponse
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from app.models import Game
from app.serializers import GameSerializer


class GameViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    # todo - Use each team's emblem of highest league in overlay
    # todo - Use each team's win% in overlay

    queryset = Game.objects.select_related(). \
        prefetch_related(

    )
    serializer_class = GameSerializer
    ordering_fields = '__all__'
    ordering = ('created_at',)

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
        data = serializer(self.queryset.order_by('-created_at').first()).data
        return JsonResponse(data)

