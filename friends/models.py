from django.db import models
from django.conf import settings
from enum import Enum


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


# FRiend list
    # def add_friend(self,account):
    #     """method to add a friend"""
    #     if not account in self.friends.all():
    #         self.friends.add(account)
    #         self.save()

    # def remove_friend(self, account):
    #     """remove a friend from list"""
    #     if account in self.friends.all():
    #         self.friends.remove(account)
    
    # def unfriend(self, to_delete_user):
    #     """
    #     Action to unfriend a user from your
    #     friends list
    #     """
    #     remover_friends_list = self #person who terminates the friendship
    #     remover_friends_list.remove_friend(to_delete_user)
    #     friend_list = FriendList.objects.get(user=to_delete_user)
    #     friend_list.remove.friend(remover_friends_list.user)

    # def is_mutual_friend(self, friend):
    #     """Check if we are we friends 
    #     together ? """

    #     if friend in self.friends.all():
    #         return True
    #     return False


#Friend request

    # def accept(self):
    #     """accept a friend request.
    #     update Sender and Receiver friends list"""

    #     receiver_friend_list = settings.AUTH_USER_MODEL.objects.get(user=self.receiver)
    #     # if receiver_friend_list is not None
    #     if receiver_friend_list:
    #         receiver_friend_list.add_friend(self.sender)
    #         sender_friend_list = settings.AUTH_USER_MODEL.objects.get(user=self.sender)

    #         if sender_friend_list:
    #             sender_friend_list.add_friend(self.receiver)
    #             self.is_active = False
    #             self.save()

    # def decline(self):
    #     """decline a friend request
    #     from another user"""
    #     self.is_active = False
    #     self.save()
