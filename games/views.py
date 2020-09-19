from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Game
import  scripts.betchamp as betchamp
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime

# Create your views here.



def UpdateDatabase_xhr(request,*args, **kwargs):
    print("updating")
    timestart = datetime.now()
    data = betchamp.main()
    print("main done", datetime.now()-timestart)
    for match in data['Games']:
        try:
            obj = Game.objects.get(game=match['game'], date=match['date'])
            if match['numberTips'] > obj.numberTips:
                obj.numberTips = match['numberTips']
                obj.ProbAway = match['ProbAway']
                obj.ProbHome = match['ProbHome']
                obj.ProbDraw = match['ProbDraw']
                obj.ToWin = match['ToWin']
                obj.save()
        except ObjectDoesNotExist:
            Game.objects.create(**match)

    context={"object_list":Game.objects.all()}
    print("DatabaseUpdated", datetime.now()-timestart)

    return render(request, "games/allgames.html",context)

def allgames_view(request,*args, **kwargs):
    allGames = Game.objects.all().order_by('-numberTips') # list of objects
    context={
        "object_list": allGames
    }

    return render(request, "games/allgames.html",context)