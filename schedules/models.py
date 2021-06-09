from django.db import models
from django.conf import settings


# Create your models here.
class Task(models.Model):
    """"table that will store one task"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['complete']


class Schedule(models.Model):
    cat = models.ManyToManyField('animals.Pet')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    time = models.ForeignKey('schedules.TimeOfDay', on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return f"{self.cat.all()}"


class TimeOfDay(models.Model):
    time = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.time}"

