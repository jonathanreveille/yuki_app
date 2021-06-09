from django.core.management.base import BaseCommand

from animals.models import Pet, Specie
from users.models import User
from schedules.models import Task, Schedule


class Command(BaseCommand):
    help = 'Deletes every single objects in the database'

    def handle(self, *args, **options):
        Pet.objects.all().delete()
        Specie.objects.all().delete()
        Task.objects.all().delete()
        Schedule.objects.all().delete()
        User.objects.all().delete()
        print('All objects are deleted from the database, done !')