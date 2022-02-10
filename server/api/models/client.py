from django.db import models


class Client(models.Model):
    wallet = models.CharField(max_length=60)

    def __str__(self):
        return self.wallet