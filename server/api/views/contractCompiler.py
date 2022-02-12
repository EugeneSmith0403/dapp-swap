import web3
from django.db import InternalError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from web3 import Web3

from ..models.deployedContract import DeployedContract

from ..services.contractService import compile_contract, deploy_contract, get_contract_data

provider = Web3.HTTPProvider(
    settings.ETHEREUM_NETWORK
)

w3 = web3.Web3(provider)

class ContractCompiler(APIView):
    def get(self, request):
        address = '0x9d3cB05047280bD8De204917D0AE7E79091f70C1'
        abi, _ = get_contract_data('createToken', 'MyToken')
        contract_instance = w3.eth.contract(address=address, abi=abi)
        result = contract_instance.functions.getPrice().call()
        return Response({'result': result, 'status': 'Ok'})

    # Create smart contract
    # @param contract_name,
    # @param contract_class_name,
    # @param props: { name, symbol, _amount, partialPrice }
    # @param owner_wallet_address
    # @return
    def post(self, request):
        contract_name = request.data['contract_name']
        item = DeployedContract.objects.all().filter(contract_name=contract_name)
        if not item:
            try:
                compile_contract(contract_name)
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
                address_contract = deploy_contract(**deployProperty)
                try:
                    DeployedContract(
                        contract_name=contract_name,
                        address_contract=address_contract,
                        address_wallet=owner_wallet_address,
                    ).save()
                except InternalError:
                    raise InternalError('Something wen\'t wrong with saving model to database!')
                return Response({'status': 'ok', 'result': {'hash_contract': address_contract}})
            except InternalError:
                raise InternalError('Check you arguments!')
        return {'result': 'contract Existed', 'status': 'ok'}
