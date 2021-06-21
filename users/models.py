from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class Role(models.Model):
    """table to define the role
    of the user : owner or catsitter"""

    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class UsersManager(BaseUserManager):
    
    def get_all_by_term(self, term):
        """method for autocomplete method to search in 
        db while user is typing his query search"""

        self.users = User.objects.all()
        return self.users.filter(username__icontains=term)


class User(AbstractUser):
    """table that inherits from AbstractUser
    to establish more attributes to Django's
    User model"""
    # ajouter de nouveau champs au modèle (en supposant qu'on aime bien le USER MODEL de base)

    email = models.EmailField('user email', max_length=255, unique=True)
    location = models.CharField(max_length=30, blank=True)

    avatar = models.ImageField(upload_to="static/img/", default='avatar_profile.jpg')

    role = models.ForeignKey('users.Role',
                        on_delete=models.CASCADE,
                        related_name="role",
                        null=True, blank=True)

    host_capacity = models.IntegerField(null=True, blank=True) # NEW
    location = models.CharField(max_length=100, null=True)
    postal_code = models.IntegerField(null=True, blank=True)
    friends = models.ManyToManyField('users.User', blank=True)

    objects = UsersManager()

    def __str__(self):
        return f'{self.username}'
    