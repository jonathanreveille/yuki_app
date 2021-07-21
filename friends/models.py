from django.db import models
from django.conf import settings
from enum import Enum

from django.db.models.fields import related


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
                                related_name="cat_owner",
                                verbose_name="cat's owner")

    catsitter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="catsitter",
                                verbose_name="catsitter")

    cat = models.ForeignKey('animals.Pet',
                                on_delete=models.CASCADE,
                                related_name="catsitted",
                                verbose_name="catsitted",
                                )
