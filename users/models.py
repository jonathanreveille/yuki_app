from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Role(models.Model):
    """table to define the role
    of the user : owner or catsitter"""

    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    """table that inherits from AbstractUser
    to establish more attributes to Django's
    User model"""
    # ajouter de nouveau champs au modèle (en supposant qu'on aime bien le USER MODEL de base)

    email = models.EmailField('user email', max_length=255, unique=True)
    location = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars/", default='avatar_profile.jpg')

    role = models.ForeignKey('users.Role',
                        on_delete=models.CASCADE,
                        related_name="role",
                        null=True, blank=True)

    host_capacity = models.IntegerField(null=True, blank=True) # NEW
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.username}'

class Relationship(models.Model):

    follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="follower")

    followed = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="followed")
                                
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.follower} added {self.followed}'
