"""
.. module:: shweb.accounts
   :platform: Unix, Windows
   :synopsis: Module with database user model and custom objects manager.

"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Custom objects manager for user model, which is adapted to use email
       as a username field.
    """

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Low level method for user creating.

        Args:
            email: User email (username)
            password: User password
            is_staff: Boolean which indicates whether user belongs to staff
            is_superuser: Boolean which indicates whether user has admin privileges

        Returs:
            user object
        """
        now = timezone.now()
        if not email:
            raise ValueError('You have to provide your email address')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        High level method for user creating.

        Args:
            email: User email (username)
            password: User password

        Returs:
            user object
        """
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        High level method for user with admin privileges creating.

        Args:
            email: User email (username)
            password: User password

        Returs:
            user object
        """
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email set as username.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=False)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    confirmation_code = models.CharField(max_length=50)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name
