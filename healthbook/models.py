from django.db import models

from animals.models import YesOrNoChoice


class HealthBook(models.Model):
    """this table stores the general health
    informations of the pet"""

    pet = models.ForeignKey('animals.Pet', on_delete=models.CASCADE, related_name="pet_healthbook")

    sterilize = models.CharField(
                max_length=20, verbose_name="sterilized",
                choices=[(tag.name, tag.value) for tag in YesOrNoChoice],
                blank=True, null=True
                )

    vaccine = models.CharField(
                max_length=20, verbose_name="vaccinated",
                choices=[(tag.name, tag.value) for tag in YesOrNoChoice],
                blank=True, null=True
                )

    last_vaccine = models.DateField(
                verbose_name="last vaccination",
                null=True, blank=True
                )

    next_vaccine = models.DateField(
                verbose_name="next vaccination",
                null=True, blank=True
                )

    veterinary_name = models.CharField(max_length=100, null=True, blank=True)

    veterinary_phone = models.CharField(max_length=100, null=True, blank=True)


class Medication(models.Model):
    """table that will store information
    about the pet's medication treatment"""
    
    pet = models.ForeignKey('animals.Pet', on_delete=models.CASCADE, related_name="pet_medication")
    med_name = models.CharField(max_length=100)
    med_start = models.DateField(null=True, default="Everyday")
    med_end = models.DateField(null=True)
    time = models.ForeignKey('schedules.TimeOfDay',
                            on_delete=models.CASCADE,
                            related_name="time_medication",
                            verbose_name="time of day for medication")