from rest_framework.views import APIView
from web3 import Web3
from django.conf import settings
from rest_framework.response import Response

from server.api.models.web3 import SwapConstructorProps, Web3Model
from server.api.payloads.swapVendor import SwapAddTokenProps, BuyTokenProps, SellTokenProps, SwapProps

provider = Web3.HTTPProvider(
    settings.ETHEREUM_NETWORK
)

w3 = Web3(provider)


class AddedToken(APIView):
    def post(self, request):
        props = SwapAddTokenProps(**request.data)
        w3 = Web3Model(props)
        w3.set_contract(props)
        contract = Web3Model(props).get_contract()
        contract.functions.addToken(
            props.contract_address,
            props.liquidity
        ).transact()
        return Response({'result': 'ok', 'contract_address': props.owner_wallet_address})


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
