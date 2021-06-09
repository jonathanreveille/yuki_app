from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    """table to define the role
    of the user"""

    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    """table that inherits from AbstractUser
    to establish more attributes to Django's
    User model"""
    # ajouter de nouveau champs au modèle (en supposant qu'on aime bien le USER MODEL de base)

    email = models.EmailField('user email', max_length=255, unique=True)
    role = models.ForeignKey('users.Role',
                            on_delete=models.CASCADE,
                            related_name="role",
                            null=True, blank=True)

    location = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars/", default='avatar_profile.jpg')

    def __str__(self):
        return f'{self.username}'