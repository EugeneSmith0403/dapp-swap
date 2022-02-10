from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, models.Model):
    wallet = models.CharField(max_length=60)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return "address - {wallet}".format(wallet=self.wallet)
