from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from accounts.managers import AppUserManager


# Create your models here.
class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    is_staff = models.BooleanField(('staff status'),
                default=False,
                help_text=('Designates whether the user can log into this admin site.'),)
    is_active = models.BooleanField(('active'),
                default=True,
                help_text=('Designates whether this user should be treated as active.'
                           'Unselect this instead of deleting accounts.')
                )
    objects = AppUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
    )

    age = models.IntegerField()

    first_name = models.CharField(
        max_length=30,
    )

    last_name = models.CharField(
        max_length=30,
    )

    points = models.IntegerField(
        default=0
    )


