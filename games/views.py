from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import AcademiaGame
from django.core import serializers
from django.http import JsonResponse
# Create your views here.


def UpdateDatabase_xhr(request, *args, **kwargs):
    allGames = AcademiaGame.objects.all()  # list of objects
    # leagues = Game.objects.values('gameLeague').distinct()
    # context={
    #     # "object_list":allGames,
    #     'leagues': leagues
    # }
    data = serializers.serialize('json', allGames)

    return HttpResponse(data)


def allgames_view(request, *args, **kwargs):
    allGames = AcademiaGame.objects.all().order_by('-numberTips')  # list of objects
    leagues = AcademiaGame.objects.values_list(
        'gameLeague', flat=True).distinct()
    context = {
        "object_list": allGames,
        'leagues': leagues
    }
    return render(request, "games/allgames.html", context)
