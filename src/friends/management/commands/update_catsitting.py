from django.core.management.base import BaseCommand

from datetime import datetime, timezone

from friends.models import Catsitter


class Command(BaseCommand):

    help = 'Allows the app to know which catsittings have ended'

    def handle(self, *args, **options):
        """method that adds species to the in db"""

        today = datetime.now(timezone.utc)
        queryset = Catsitter.objects.filter(is_active=True)

        for catsitting in queryset:
            if catsitting.end <= today:
                catsitting.is_active = False
                catsitting.save()
        print("Ok, all catsittings that have ended, were stopped")
