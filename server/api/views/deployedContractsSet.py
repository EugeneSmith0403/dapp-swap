from rest_framework import viewsets
from ..models.deployedContract import DeployedContract
from ..serializers.deployedContractSerializer import DeployedContractSerializer


class DeployContractSet(viewsets.ModelViewSet):
    queryset = DeployedContract.objects.all().order_by('contract_name')
    serializer_class = DeployedContractSerializer
