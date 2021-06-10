from django.db import models
from django.conf import settings
from enum import Enum


class YesOrNoChoice(Enum):
    """choice for user when creating animal"""
    YES = "Yes"
    NO = "No"

class Specie(models.Model):
    """table that defines the type
    of the animal"""

    name = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.name}"

class Pet(models.Model):
    """table that will store pets"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner")
    specie = models.ForeignKey('animals.Specie', on_delete=models.CASCADE, related_name='specie')
    name = models.CharField(max_length=100)
    age =  models.BigIntegerField(null=True, blank=True)
    weight = models.FloatField(max_length=6, null=True, blank=True)


    def __str__(self):
        return f"{self.name}"

