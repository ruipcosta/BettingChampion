from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Game
import  scripts.betchampWeb as betchamp
from django.core import serializers
from django.http import JsonResponse
# Create your views here.



def UpdateDatabase_xhr(request,*args, **kwargs):
    data=betchamp.run(0)
    for match in data['Games']:
        try:
            obj = Game.objects.get(home=match['home'], away=match['away'], date=match['date'])
            if match['numberTips'] > obj.numberTips:
                obj.numberTips = match['numberTips']
                obj.ProbAway = match['ProbAway']
                obj.ProbHome = match['ProbHome']
                obj.ProbDraw = match['ProbDraw']
                obj.ToWin = match['ToWin']
                obj.save()
        except ObjectDoesNotExist:
            Game.objects.create(**match)
    
    allGames = Game.objects.all() # list of objects
    # leagues = Game.objects.values('gameLeague').distinct()
    # context={
    #     # "object_list":allGames,
    #     'leagues': leagues
    # }
    data = serializers.serialize('json', allGames)

    return HttpResponse(data, mimetype='application/javascript')

def allgames_view(request,*args, **kwargs):
    allGames = Game.objects.all().order_by('-numberTips') # list of objects
    leagues = Game.objects.values_list('gameLeague', flat=True).distinct()
    context={
        "object_list": allGames,
        'leagues': leagues
    }
    return render(request, "games/allgames.html",context)