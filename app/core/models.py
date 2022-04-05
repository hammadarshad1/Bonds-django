from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from core.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using login with
    email instead of username"""
    email = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
