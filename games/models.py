from django.db import models

# Create your models here.
class Game(models.Model):
    game = models.CharField(max_length= 200)
    date = models.CharField(max_length= 200)
    gameLeague = models.CharField(max_length= 200)
    numberTips = models.IntegerField()
    ProbHome = models.IntegerField()
    OddHome = models.DecimalField(max_digits=100, decimal_places=2)
    ProbDraw = models.IntegerField()
    OddDraw = models.DecimalField(max_digits=100, decimal_places=2)
    ProbAway = models.IntegerField()
    OddAway = models.DecimalField(max_digits=100, decimal_places=2)
    ToWin = models.CharField(max_length=4)
    
