import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


class VM(models.Model):
    user = models.OneToOneField(User, on_delete='CASCADE')
    base_url = models.CharField(max_length=255, unique=True)
    port = models.IntegerField(unique=True)
    last_modified = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'base_url', 'port')

    def __str__(self):
        return '%s: %s' % (self.user.username, self.base_url)

    def is_active(self):
        if (self.last_modified - datetime.datetime.now()).seconds < settings.TIMEOUT:
            return True

