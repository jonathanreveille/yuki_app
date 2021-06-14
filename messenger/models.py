from django.db import models
from django.conf import settings

# Create your models here.
class Messenger(models.Model):
    """this table represents the messages
    inside the application"""

    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="from_user",
                                verbose_name="from_user")

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="for_user",
                                verbose_name="for_user")

    subject = models.CharField(max_length=300, null=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}"

    class Meta:
        ordering = ['-timestamp']
