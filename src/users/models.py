from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


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

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """table that inherits from AbstractUser
    to establish more attributes to Django's
    User model"""

    email = models.EmailField('user email', max_length=255, unique=True)
    location = models.CharField(max_length=30, blank=True)
    avatar = models.FileField(default='avatar_profile.jpg')
    role = models.ForeignKey('users.Role',
                             on_delete=models.CASCADE,
                             related_name="role",
                             null=True,
                             blank=True)

    host_capacity = models.IntegerField(null=True, blank=True)  # NEW
    location = models.CharField(max_length=100, null=True)
    postal_code = models.IntegerField(null=True, blank=True)
    friends = models.ManyToManyField('users.User', blank=True)

    objects = UsersManager()

    def __str__(self):
        return f'{self.username}'
