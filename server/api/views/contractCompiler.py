from django.db import InternalError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from web3 import Web3

from ..models.deployedContract import DeployedContract

from ..services.contractService import compile_contract, deploy_contract

provider = Web3.HTTPProvider(
    settings.ETHEREUM_NETWORK
)


class ContractCompiler(APIView):
    def get(self, request):

        return Response({'result': 'Ok'})

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
                address_contract, abi = deploy_contract(**deployProperty)
                try:
                    DeployedContract(
                        contract_name=contract_name,
                        address_contract=address_contract,
                        abi=abi,
                        address_wallet=owner_wallet_address,
                    ).save()
                except InternalError:
                    raise InternalError('Something wen\'t wrong with saving model to database!')
                return Response({'status': 'ok', 'result': {'hash_contract': address_contract}})
            except InternalError:
                raise InternalError('Check you arguments!')
        return {'result': 'contract Existed', 'status': 'ok'}
