from django.db import models
from .client import Client
from ..enum.statusRequest import StatusRequest


class RequestToken(models.Model):
    name = models.CharField(max_length=70)
    project_link = models.CharField(max_length=70)
    contract_address = models.CharField(max_length=100)
    client = models.ForeignKey(Client, related_name='requests', on_delete=models.CASCADE)
    status = models.IntegerField(default=StatusRequest.pending)

    def __str__(self):
        return self.name