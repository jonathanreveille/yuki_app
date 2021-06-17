from django.db import models
from django.conf import settings
from enum import Enum

from .managers import ScheduleManager

class CategoryChoice(Enum):
    """category of tasks, it determines
    what is the action of the task"""

    CLEANING = "Cleaning"
    FOOD = "Food"
    MEDICATION = "Medication"

# Create your models here.
class Task(models.Model):
    """"table that will store one task"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    category = models.CharField(max_length=40,
                                verbose_name="category of task",
                                choices=[(tag.name, tag.value) for tag in CategoryChoice],
                                null=True, blank=True
                                )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['complete']


class Schedule(models.Model):
    pet = models.ManyToManyField('animals.Pet')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    time = models.ForeignKey('schedules.TimeOfDay', on_delete=models.CASCADE, null=True,blank=True)

    objects = ScheduleManager()

    def __str__(self):
        return f"{self.pet.all()}"

    class Meta:
        ordering = ["id"]


class TimeOfDay(models.Model):
    time = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.time}"
