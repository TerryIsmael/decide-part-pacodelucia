from django.db import models


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)

class CensusPreference(models.Model):
    voting_preference_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    class Meta:
        unique_together = (('voting_preference_id', 'voter_id'),)
