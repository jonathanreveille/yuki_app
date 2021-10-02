from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Role(models.Model):
    """table to define the role
    of the user : owner or catsitter"""

    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class UsersManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password=None):
        """creates a super user with the given email, date of
        birth, and email"""

        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


    def get_all_by_term(self, term):
        """method for autocomplete method to search in
        db while user is typing his query search"""

        self.users = User.objects.all()
        return self.users.filter(username__icontains=term)


class User(AbstractUser):
    """table that inherits from AbstractUser
    to establish more attributes to Django's
    User model"""

    email = models.EmailField('user email', max_length=255, unique=True)
    location = models.CharField(max_length=30, blank=True)

    avatar = models.ImageField(blank=True, default='avatar_profile.jpg')

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


