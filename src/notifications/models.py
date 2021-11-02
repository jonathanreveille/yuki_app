from django.db import models
from django.conf import settings


class Notification(models.Model):
    # 1 = is friend request
    # 2 = is incoming message
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='notification_to',
                                blank=True,
                                null=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='notification_from',
                                  blank=True,
                                  null=True)
    friend_request = models.ForeignKey('friends.FriendRequest',
                                       on_delete=models.CASCADE,
                                       related_name='+',
                                       blank=True,
                                       null=True)
    message =  models.ForeignKey('messenger.Messenger',
                                 on_delete=models.CASCADE,
                                 related_name='+',
                                 blank=True,
                                 null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_has_seen = models.BooleanField(default=False)
