from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email=models.EmailField()
    password = models.CharField(max_length=100)
    clave = models.CharField(default='', max_length=6)
    isEmailAuthenticated=models.BooleanField(default=False, help_text='¿Está autenticado su email?')
    #to save the data
    def save(self):
        self.save()
