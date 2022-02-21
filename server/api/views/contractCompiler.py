import web3
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
        address = '0x5ECc7200A4f12217A8e7B26799d69563d610FEaE'
        try:
            abi, _ = get_contract_data('createToken', 'MyToken')

        except Exception:
            return Response({'result': 'contract file not found!'})

        contract_instance = w3.eth.contract(address=address, abi=abi)
        result = contract_instance.functions.getPrice().call()

        tx_hash = contract_instance.functions \
            .transfer('0x4CD7b1cB371c0Ba761e3e0dC8887bE3F4a99C35A', 100) \
            .transact({'from': settings.CONTRACT_OWNER_WALLET_ADDRESS})

        balance = contract_instance.functions.balanceOf('0x4CD7b1cB371c0Ba761e3e0dC8887bE3F4a99C35A').call()
        balance_owner = contract_instance.functions.balanceOf(settings.CONTRACT_OWNER_WALLET_ADDRESS).call()

        return Response(
            {'result': {'balance': balance, 'balance_owner': balance_owner, 'tx_hash': tx_hash.hex()}, 'status': 'Ok'})

    # @example params: {
    #   "contract_name": "",
    #   "contract_class_name": "",
    #   "props": {},
    #   "owner_wallet_address": ""
    #  }
    # Create smart contract
    # @param contract_name,
    # @param contract_class_name,
    # @param props: { name, symbol, _amount, partialPrice }
    # @param owner_wallet_address
    # @return

    def post(self, request):
        contract_name = request.data['contract_name']
        owner_wallet_address = request.data['owner_wallet_address']
        contract = '{contract_name}_{wallet}'.format(contract_name=contract_name, wallet=owner_wallet_address)
        item = DeployedContract.objects.all().filter(contract_name=contract)
        if not item:
            compile_contract(contract_name)
            contract_class_name = request.data['contract_class_name']
            props = request.data['props']

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
                    contract_name=contract,
                    address_contract=address_contract,
                    address_wallet=owner_wallet_address,
                ).save()
            except Exception:
                return Exception('Something wen\'t wrong with saving model to database!')
            return Response({'status': 'ok', 'result': {'hash_contract': address_contract}})
        return Response({'result': 'contract Existed', 'status': 'ok'})
