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

class CensusYesNo(models.Model):
    voting_yesno_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    class Meta:
        unique_together = (('voting_yesno_id', 'voter_id'),)

class UserData(models.Model):

    GENDER = [
        ("MA", "Male"),
        ("FE", "Female"),
        ("NB", "Non binary"),
        ("NP", "No response")
    ]

    CIVIL_STATE = [
        ("SI","Single"),
        ("MA", "Married"),
        ("DI", "Divorced"),
        ("WI", "Widower")
    ]

    WORKS = [
        ("ST", "Student"),
        ("WO", "Worker"),
        ("UN", "Unemployed")
    ]

    RELIGION = [
        ("CH", "Christianity"),
        ("IS", "Islamism"),
        ("HI", "Hinduism"),
        ("BU", "Buddhism"),
        ("AG", "Agnosticism"),
        ("AT", "Atheism"),
        ("OT", "Other")
    ]

    voter_id = models.PositiveIntegerField()
    born_year = models.PositiveIntegerField(null=True)
    country = models.CharField(max_length=50, null= True)
    religion = models.CharField(max_length=2, choices=RELIGION, null=True)
    gender = models.CharField(max_length=2, choices=GENDER, null=True)
    civil_state = models.CharField(max_length=2, choices=CIVIL_STATE, null=True)
    works = models.CharField(max_length=2, choices=WORKS, null=True)
    class Meta:
        unique_together = (('voter_id'),)
