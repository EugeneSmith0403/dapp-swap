from django.db import models


class DeployedContract(models.Model):
    contract_name = models.CharField(max_length=100)
    address_contract = models.CharField(max_length=100)
    abi = models.TextField()
    address_wallet = models.CharField(max_length=100)

    def __str__(self):
        return self.contract_name