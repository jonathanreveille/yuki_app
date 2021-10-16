from django.db import models
from django.conf import settings
from django.db.models.fields import related

from enum import Enum
from datetime import datetime, timedelta, timezone


class FriendList(models.Model):
    """table that will represent the friends
    of a user within the application"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="user_friend_list")

    friend = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name="friend",
                                    on_delete=models.CASCADE,
                                    null=True)


    def __str__(self):
        return f"{self.friend.username}"


class FriendRequest(models.Model):
    """Friend request,
    1. sender : user who initiates the friend request
    2. receiver : user who receives the friend request
    """

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender_request")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver_request")
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"from {self.sender.username} to {self.receiver.username}"

    class Meta:

        ordering = ["-timestamp"]


class FriendRequestStatus(Enum):
    NO_FRIEND_REQUEST = 0
    THEM_SENT_YOU = 1
    YOU_SENT_THEM = 2



class Catsitter(models.Model):
    """class that will allow two friends
    to share their cat's schedule, medication
    and healthbook"""

    is_owned = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="is_cat_owner",
                                verbose_name="cat's owner")

    is_catsitter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="is_catsitter",
                                verbose_name="catsitter")

    pet = models.ForeignKey('animals.Pet',
                                on_delete=models.CASCADE,
                                related_name="catsitted",
                                verbose_name="catsitted",
                                )

    start = models.DateTimeField(null=True, verbose_name="catsitting starts")
    end = models.DateTimeField(null=True, verbose_name="catsitting ends")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Owner {self.is_owned} : {self.is_catsitter} for {self.pet}"

    def is_catsitting(self):
        today = datetime.now(timezone.utc)
        if self.start < today < self.end:
            return True
        return False

    def end_catsitting(self):
        if self.end < datetime.now(timezone.utc) :
            self.is_active = False
            return True
        return False

    # Comment faire de l'expiration date quand on arrive^-
    # Comment on peut faire appel ?
    # comment ça s'active ?
    # suis-je obligé de passer par une tâche CRON ou avec par Celery ?

    # différent status : end_date qui sont prévu pour aujourd'hui
    # Une tache automatisé quotidien

    # est-ce que c'est dans mes vues que je l'appelle ?
    # prendre la date du jour aujourd'hui
    # 23H59 : comme ça on a tout les object d'aujourd'hui
    # une fois pris, on change l'attribut à False
    # le end à aujourd'hui et is_actif à True

    # Serveur de  test de production (tâche cron de 5/10 min)
    # Préparer dans mon admin, choisir les entrées et créer des objets pour la journée


    # Comment faire pour avoir plusieurs bases de données ? Une pour l'application et une pour les photos ?
    # Comment préparer les fichiers de settings pour les photos uniquement sur notre serveur Linux ?
# ce n'est pas une base de onnée amazon s3
# pour pouvoir récupérer sur s3, on peut définir des règles
# on fait le controle des permissions
