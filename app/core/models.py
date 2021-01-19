from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from django.conf import settings
from pycountry import countries

COUNTRY_CHOICES = tuple((country.name, country.name) for country in countries)


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

    email = models.EmailField(_('Email'), max_length=255, unique=True)
    first_name = models.CharField(_('First Name'), max_length=255, null=True, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=255, null=True, blank=True)
    company_name = models.CharField(_('Company Name'), max_length=255, null=True, blank=True)
    country = models.CharField(_('Country'), max_length=50, choices=COUNTRY_CHOICES, null=True, blank=True)
    require_password_change = models.BooleanField(_('Require password change'), default=False)
    preferred_language = models.CharField(_('Preferred language'), max_length=50, default='English')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class PasswordPolicy(models.Model):
    """password policy model"""

    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='password_policy')
    min_number = models.IntegerField(default=0)
    min_length = models.IntegerField(default=8)
    min_lowercase = models.IntegerField(default=0)
    min_uppercase = models.IntegerField(default=0)
    min_special_char = models.IntegerField(default=0)
    min_different_char = models.IntegerField(default=0)
    max_consecutive_char = models.IntegerField(default=0)
    max_consecutive_char_type = models.IntegerField(default=0)
    exp_interval = models.IntegerField(default=90)
    warn_interval = models.IntegerField(default=10)
    pwd_history = models.IntegerField(default=7)
    contains_username = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.user, self.name)
