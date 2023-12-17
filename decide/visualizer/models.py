from django.db import models
from voting.models import Voting

# Create your models here.
class Stats(models.Model):
    voting=models.ForeignKey(Voting, on_delete=models.CASCADE,default=0)
    votes= models.IntegerField(default=0)
    census= models.FloatField

class StatsPreference(models.Model):
    voting_preference_id = models.PositiveIntegerField()
    votes= models.IntegerField(default=0)
    census= models.FloatField


class CensusYesNo(models.Model):
    voting_yesno_id = models.PositiveIntegerField()
    votes= models.IntegerField(default=0)
    census= models.FloatField
