from django.db import models
from .client import Client
from ..enum.statusRequest import StatusRequest


class RequestToken(models.Model):
    name = models.CharField(max_length=70)
    liquidityAmount = models.IntegerField()
    symbol = models.CharField(max_length=10)
    partial = models.IntegerField(default=1)
    client = models.ForeignKey(Client, related_name='requests', on_delete=models.CASCADE)
    status = models.IntegerField(default=StatusRequest.pending)

    def __str__(self):
        return self.name