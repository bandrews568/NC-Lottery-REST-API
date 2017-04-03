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
    powerball = request.GET.get('powerball', None)
    megaball = request.GET.get('megaball', None)

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

    if model == Pick3 or model == Pick4:
        if time:
            queryset = queryset.filter(drawing_time=time)

    if model == PowerBall and powerball:
        queryset = queryset.filter(powerball=powerball)

    if model == MegaMillions and megaball:
        queryset = queryset.filter(megaball=megaball)

    if limit is not None:
        limit = int(limit)
        queryset = queryset[:limit]

    return queryset


@api_view()
def all_games(request):
    pick3 = Pick3.objects.all().last()
    pick4 = Pick4.objects.all().last()
    cash5 = Cash5.objects.all().last()
    powerball = PowerBall.objects.all().last()
    mega_millions = MegaMillions.objects.all().last()
    lucky_for_life = LuckyForLife.objects.all().last()

    pick3_data = Pick3Serializer(pick3, many=False)
    pick4_data = Pick4Serializer(pick4, many=False)
    cash5_data = Cash5Serializer(cash5, many=False)
    powerball_data = PowerBallSerializer(powerball, many=False)
    mega_millions_data = MegaMillionsSerializer(mega_millions, many=False)
    lucky_for_life_data = LuckyForLifeSerializer(lucky_for_life, many=False)

    serialized_data = {
        "pick3": pick3_data.data,
        "pick4": pick4_data.data,
        "cash5": cash5_data.data,
        "powerball": powerball_data.data,
        "mega_millions": mega_millions_data.data,
        "lucky_for_life": lucky_for_life_data.data
    }
    return JSONResponse(serialized_data)


@api_view()
def pick3(request):
    queryset = filter_queryset(request, Pick3)
    games_serializer = Pick3Serializer(queryset, many=True)
    return JSONResponse(games_serializer.data)


@api_view()
def pick4(request):
    queryset = filter_queryset(request, Pick4)
    games_serializer = Pick4Serializer(queryset, many=True)
    return JSONResponse(games_serializer.data)


@api_view()
def cash5(request):
    queryset = filter_queryset(request, Cash5)
    games_serializer = Cash5Serializer(queryset, many=True)
    return JSONResponse(games_serializer.data)


@api_view()
def powerball(request):
    queryset = filter_queryset(request, PowerBall)
    games_serializer = PowerBallSerializer(queryset, many=True)
    return JSONResponse(games_serializer.data)


@api_view()
def mega_millions(request):
    queryset = filter_queryset(request, MegaMillions)
    games_serializer = MegaMillionsSerializer(queryset, many=True)
    return JSONResponse(games_serializer.data)


@api_view()
def lucky_for_life(request):
    queryset = filter_queryset(request, LuckyForLife)
    games_serializer = LuckyForLifeSerializer(queryset, many=True)
    return JSONResponse(games_serializer.data)
