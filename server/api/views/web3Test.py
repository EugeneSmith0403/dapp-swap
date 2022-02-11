from rest_framework.views import APIView
from rest_framework.response import Response
from web3 import EthereumTesterProvider, Web3

from ..services.contractService import compile_contract, deploy_contract


class Web3Test(APIView):
    def get(self, request):
        compile_contract('createToken')
        hash_contract = deploy_contract('createToken', 'MyToken', Web3.EthereumTesterProvider)
        return Response({'result': 'Ok', 'hash': hash_contract})
