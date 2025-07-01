from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from accounts.managers import AppUserManager


# Create your models here.
#Option 1
# class CustomUser(AbstractUser):
#     points = models.IntegerField(blank=True, null=True)

# Option 2
# class CustomCustonUser(CustomUser):
#     class Meta:
#         proxy = True
#
#         def get_points(self):
#             return self.points

# Option 3
class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)