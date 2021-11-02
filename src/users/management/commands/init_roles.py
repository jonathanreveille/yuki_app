from django.core.management.base import BaseCommand

from users.models import Role


USER_ROLES = ["Owner", "Catsitter"]


class Command(BaseCommand):
    help = 'Adds roles for users in the app'

    def handle(self, *args, **options):

        for role_name in USER_ROLES:
            Role.objects.get_or_create(name=role_name)

        print("Your roles for users are in the database now!")
