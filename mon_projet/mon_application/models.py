from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Activity(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) 
    date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=100)
    marche = models.FloatField(default=0)
    jogging = models.FloatField(default=0)
    velo = models.FloatField(default=0)
    total = models.FloatField(default=0, editable=False)
    calories = models.FloatField(default=0, editable=False)
    vitesse = models.FloatField() 
    

    def save(self, *args, **kwargs):
        self.total = self.marche + self.jogging + self.velo
        self.calories = (self.marche * 50) + (self.jogging * 70) + (self.velo * 35)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.date} - Total: {self.total} km, Calories: {self.calories} kcal"


class UserObjective(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objectif_marche = models.FloatField(default=0)  # Défaut à zéro
    objectif_jogging = models.FloatField(default=0)  # Défaut à zéro
    objectif_velo = models.FloatField(default=0)  # Défaut à zéro

    def __str__(self):
        return f"Objectifs de {self.user.username}"