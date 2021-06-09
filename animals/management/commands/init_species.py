from django.core.management.base import BaseCommand

from animals.models import Specie

SPECIE_LIST = ["cat",]

class Command(BaseCommand):
    help = 'Initialise la base de données à partir des données de Openfoodfacts'

    def handle(self, *args, **options):
        """method that adds species to the in db"""

        for specie in SPECIE_LIST:
            Specie.objects.get_or_create(name=specie)

        print("Your species are in the database now!")
