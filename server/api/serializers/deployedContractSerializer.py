from rest_framework import serializers
from ..models.deployedContract import DeployedContract


class DeployedContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeployedContract
        fields = ('id', 'contract_name', 'address_contract', 'abi', 'address_wallet')
