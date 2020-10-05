from django.db import models

# Create your models here.
class Game(models.Model):
    home = models.CharField(max_length= 200)
    away = models.CharField(max_length= 200)
    date = models.CharField(max_length= 200)
    gameLeague = models.CharField(max_length= 200)
    numberTips = models.IntegerField()
    ProbHome = models.IntegerField()
    ProbDraw = models.IntegerField()
    ProbAway = models.IntegerField()
    ToWin = models.CharField(max_length=4)
    lol = models.TextField()
    
