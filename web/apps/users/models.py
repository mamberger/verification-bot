from datetime import datetime, timedelta
from django.contrib.auth.models import Group
from django.conf import settings 
from django.contrib.auth.models import (
	AbstractBaseUser, PermissionsMixin
)
from .UserManager import UserManager
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above is
    # must manage objects of this type.

    objects = UserManager()

    def __str__(self):
        return self.username


    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_group(self):
        return self.groups.values_list('name', flat=True).first()