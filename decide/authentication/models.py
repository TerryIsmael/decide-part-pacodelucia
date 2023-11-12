from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email=models.EmailField()
    password = models.CharField(max_length=100)

    #to save the data
    def save(self):
        self.save()
