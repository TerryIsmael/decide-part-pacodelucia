from django.db import models


class Census(models.Model):

    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

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

    born_date = models.DateField()
    gender = models.CharField(max_length=2, choices=GENDER, null=true)
    civil_state = models.CharField(max_length=2, choices=CIVIL_STATE, null=true)
    works = models.CharField(max_length=2, choices=WORKS, null=true)
    
    class Meta:
        unique_together = (('voting_id','voter_id','born_date','gender','civil_state','works'),)
