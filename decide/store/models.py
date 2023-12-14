from django.db import models
from base.models import BigBigField


class Vote(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.voting_id, self.voter_id)



class VoteByPreference(models.Model):
    voting_by_preference_id = models.PositiveIntegerField()
    voter_by_preference_id = models.PositiveIntegerField()
    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)

    def __str__(self):

        return '{}: {}'.format(self.voting_by_preference_id, self.voter_by_preference_id)
    

class VoteYesNo(models.Model):
    voting_yesno_id = models.PositiveIntegerField()
    voter_yesno_id = models.PositiveIntegerField()

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)

    def __str__(self):

        return '{}: {}'.format(self.voting_yesno_id, self.voter_yesno_id) 

