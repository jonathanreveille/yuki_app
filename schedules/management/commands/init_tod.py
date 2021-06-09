from django.core.management.base import BaseCommand

from schedules.models import TimeOfDay

TIME_OF_DAY = ["Morning", "Afternoon", "Night"]

class Command(BaseCommand):
    help = 'Initialise la base de données à partir des données de Openfoodfacts'

    def handle(self, *args, **options):
        """method that adds species to the in db"""

        for time in TIME_OF_DAY:
            TimeOfDay.objects.get_or_create(time=time)

        print("Your time of days options are in the db!")
