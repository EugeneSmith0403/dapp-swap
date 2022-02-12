from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from web3 import Web3
from ..models.deployedContract import DeployedContract

from ..services.contractService import compile_contract, deploy_contract

provider = Web3.HTTPProvider(
    settings.ETHEREUM_NETWORK
)


class Web3Test(APIView):
    def get(self, request):

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

    # contract_name,
    # contract_class_name,
    # props: { name, symbol, _amount, partialPrice }
    # owner_wallet_address
    def post(self, request):
        try:
            contract_name = request.data['contract_name']
            contract_class_name = request.data['contract_class_name']
            props = request.data['props']
            owner_wallet_address = request.data['owner_wallet_address']

            deployProperty = {
                'contract_name': contract_name,
                'contract_class_name': contract_class_name,
                'contract_props': props,
                'provider': provider,
                'owner_wallet_address': owner_wallet_address
            }
            address_contract, abi = deploy_contract(**deployProperty)
            try:
                DeployedContract(
                    contract_name=contract_name,
                    address_contract=address_contract,
                    abi=abi,
                    address_wallet=owner_wallet_address,
                ).save()
            except Exception:
                raise Exception('Something wen\'t wrong with saving model to database!')

            return Response({'result': 'Ok', 'hash_contract': address_contract})
        except Exception:
            raise Exception('Check you arguments!')
