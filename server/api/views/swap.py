from rest_framework.views import APIView
from web3 import Web3
from django.conf import settings
from rest_framework.response import Response

from ..models.deployedContract import DeployedContract
from ..models.web3 import SwapConstructorProps, Web3Model, ContractProps
from ..payloads.swapVendor import SwapAddTokenProps, BuyTokenProps, SellTokenProps, SwapProps, BaseSwapProps

provider = Web3.HTTPProvider(
    settings.ETHEREUM_NETWORK
)

w3 = Web3(provider)


class AddedToken(APIView):
    def post(self, request):
        props = SwapAddTokenProps(**request.data)
        w3 = Web3Model(props)

        queryName = '{contract_name}_{wallet}'.format(contract_name= props.contract_name, wallet=props.owner_wallet_address)

        item = DeployedContract.objects.filter(contract_name=queryName).all()

        if not item:
            raise Exception('Contract doesn\'t exist!')

        swap_contract_props = {
            'contract_name': props.contract_name,
            'contract_class_name': props.contract_class_name,
            'contract_address': item[0].address_contract
        }

        # add swap contract
        w3.set_contract(ContractProps(swap_contract_props))

        swap_vendor_contract = w3.get_contract(props.contract_name)

        contract_data = {
            "contract_name": "createToken",
            "contract_class_name": "MyToken",
            "contract_address": props.contract_address
        }
        # add token contract
        w3.set_contract(ContractProps(contract_data))

        token_contract = w3.get_contract('createToken')

        token_contract.functions.approve(props.contract_address, props.liquidity).call()
        trx = swap_vendor_contract.functions.addToken(
            props.contract_address,
            props.liquidity
        ).transact()

        return Response({'result': 'ok', 'contract_address': props.owner_wallet_address, 'trx': trx})



class BuyToken(APIView):
    def post(self, request):
        props = BuyTokenProps(**request.data)
        w3 = Web3Model(props)
        w3.set_contract(props)
        contract = w3.get_contract()
        contract.functions.buyToken(
            props.contract_address
        ).transact({'from': props.owner_wallet_address})
        return Response({'result': 'ok'})


class SellToken(APIView):
    def post(self, request):
        props = SellTokenProps(**request.data)
        w3 = Web3Model(props)
        w3.set_contract(props)
        contract = w3.get_contract()
        contract.functions.sellToken(
            props.contract_address,
            props.amount
        ).transact({'from': props.owner_wallet_address})
        return Response({'result': 'ok'})


class Swap(APIView):
    def post(self, request):
        props = SwapProps(**request.data)
        w3 = Web3Model(props)
        w3.set_contract(props)
        contract = w3.get_contract()
        contract.functions.swap(
            props.sail_token_address,
            props.sail_token_amount,
            props.buy_token_address
        ).transact({'from': props.owner_wallet_address})
        return Response({'result': 'ok'})
