from rest_framework.views import APIView
from rest_framework.response import Response
from web3 import Web3

from ..services.contractService import compile_contract, deploy_contract


class Web3Test(APIView):
    def get(self, request):

        provider = Web3.HTTPProvider(
            'HTTP://127.0.0.1:7545'
        )

        compile_contract('createToken')

        props = {
            'name': "TS",
            'symbol': 'TS',
            '_amount': 1000000000000000000,
            'partialPrice': 1
        }

        deployProperty = {
            'contract_name': 'createToken',
            'contract_class_name': 'MyToken',
            'contract_props': props,
            'provider': provider
        }
        hash_contract = deploy_contract(**deployProperty)
        return Response({'result': 'Ok', 'hash_contract': hash_contract})
