from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

from .models import (Pick3, Pick4, Cash5,
                     PowerBall, MegaMillions,
                     LuckyForLife)
from .serializer import (Pick3Serializer, Pick4Serializer,
                         Cash5Serializer, PowerBallSerializer,
                         MegaMillionsSerializer, LuckyForLifeSerializer)


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def filter_queryset(request, model):
    limit = request.GET.get('limit', None)
    date = request.GET.get('date', None)
    date_begin = request.GET.get('begin', None)
    date_end = request.GET.get('end', None)
    day = request.GET.get('day', None)
    month = request.GET.get('month', None)
    year = request.GET.get('year', None)
    numbers = request.GET.get('numbers', None)
    time = request.GET.get('time', None)

    queryset = model.objects.all()

    if date:
        queryset = queryset.filter(drawing_date=date)

    if date_begin and date_end:
        queryset = queryset.filter(drawing_date__range=[date_begin, date_end])

    if date_begin is None and date_end is None:
        if day:
            queryset = queryset.filter(drawing_date__day=day)

        if month:
            queryset = queryset.filter(drawing_date__month=month)

        if year:
            queryset = queryset.filter(drawing_date__year=year)

    if numbers:
        queryset = queryset.filter(drawing_numbers__contains=numbers)

    if model == Pick3 or model == Pick4 and time:
        queryset = queryset.filter(drawing_time=time)

    if limit is not None:
        limit = int(limit)
        queryset = queryset[:limit]

    return queryset


@api_view()
def pick3(request):
    queryset = filter_queryset(request, Pick3)
    games_serializer = Pick3Serializer(queryset, many=True)
    return JSONResponse(games_serializer.data)


@api_view()
def pick4(request):
    games = Pick4.objects.all()
    games_serializer = Pick4Serializer(games, many=True)
    return JSONResponse(games_serializer.data)


@api_view()
def cash5(request):
    games = Cash5.objects.all()
    games_serializer = Cash5Serializer(games, many=True)
    return JSONResponse(games_serializer.data)


@api_view()
def powerball(request):
    games = PowerBall.objects.all()
    games_serializer = PowerBallSerializer(games, many=True)
    return JSONResponse(games_serializer.data)


@api_view()
def mega_millions(request):
    games = MegaMillions.objects.all()
    games_serializer = MegaMillionsSerializer(games, many=True)
    return JSONResponse(games_serializer.data)

@api_view()
def lucky_for_life(request):
    games = LuckyForLife.objects.all()
    games_serializer = LuckyForLifeSerializer(games, many=True)
    return JSONResponse(games_serializer.data)
