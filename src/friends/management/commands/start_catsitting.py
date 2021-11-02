from django.core.management.base import BaseCommand

from datetime import datetime, timezone

from friends.models import Catsitter


class Command(BaseCommand):

    help = 'Allows the app to know which catsittings have starts'

    def handle(self, *args, **options):
        """method that adds species to the in db"""

        today = datetime.now(timezone.utc)
        queryset = Catsitter.objects.filter(is_active=False)
        for catsitting in queryset:
            if catsitting.start <= today < catsitting.end:
                catsitting.is_active = True
                catsitting.save()
        print("Catsitting launched for today")
