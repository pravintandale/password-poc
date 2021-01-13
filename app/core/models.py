from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
                                       PermissionsMixin
from django.conf import settings

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """create and save a new user"""
        if not email:
            raise ValueError("Users must have email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """custom user model"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class PasswordPolicy(models.Model):
    """password policy model"""

    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    min_length = models.IntegerField()
    min_characters = models.IntegerField()
    min_lowercase = models.IntegerField()
    min_uppercase = models.IntegerField()
    min_special_char = models.IntegerField()
    min_different_char = models.IntegerField()
    max_consecutive_char = models.IntegerField()
    max_consecutive_char_type = models.IntegerField()
    exp_interval = models.IntegerField(default=90)
    warn_interval = models.IntegerField()
    pwd_history = models.IntegerField(default=7)
    is_alpha_numeric = models.BooleanField(default=True)
    allow_username = models.BooleanField(default=False)


    def __str__(self):
        return self.name

