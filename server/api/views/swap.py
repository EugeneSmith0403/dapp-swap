import web3.eth
from rest_framework.views import APIView
from web3 import Web3
import web3
from django.conf import settings
from rest_framework.response import Response

from ..models.deployedContract import DeployedContract
from ..models.web3 import SwapConstructorProps, Web3Model, ContractProps
from ..payloads.swapVendor import SwapAddTokenProps, BuyTokenProps, SellTokenProps, SwapProps, BaseSwapProps
from ..services.contractService import get_contract_data

# provider = Web3.HTTPProvider(
#     settings.ETHEREUM_NETWORK
# )
#
# w3 = Web3(provider)


class AddedToken(APIView):
    def post(self, request):
        props = SwapAddTokenProps(**request.data)
        w3 = Web3Model(props)

        queryName = '{contract_name}_{wallet}'.format(contract_name=props.contract_name,
                                                      wallet=props.owner_wallet_address)

        item = DeployedContract.objects.filter(contract_name=queryName).all()

        if not item:
            raise Exception('Contract doesn\'t exist!')

        swap_contract_props = {
            'contract_name': props.contract_name,
            'contract_class_name': props.contract_class_name,
            'contract_address': item[0].address_contract
        }

        swap_props = ContractProps(swap_contract_props)

        # add swap contract
        w3.set_contract(swap_props)

        contract_data = {
            "contract_name": "createToken",
            "contract_class_name": "MyToken",
            "contract_address": props.contract_address
        }
        # add token contract
        w3.set_contract(ContractProps(contract_data))

        token_contract = w3.get_contract('createToken')
        swap_vendor_contract = w3.get_contract(props.contract_name)
        liquidity = int(props.liquidity)

        transactProps = {
            'from': settings.CONTRACT_OWNER_WALLET_ADDRESS,
        }

        token_contract.functions.approve(swap_props.contract_address, liquidity)\
            .transact(transactProps)
        
        swap_vendor_contract.functions.addToken(props.contract_address, liquidity).transact(transactProps)

        balance_token_owner = token_contract.functions.balanceOf(settings.CONTRACT_OWNER_WALLET_ADDRESS).call()
        balance_swap_vendor_contract = token_contract.functions.balanceOf(swap_props.contract_address).call()

        return Response({
            'result': 'ok', 'contract_address': props.owner_wallet_address,
            'balance_swap_vendor_contract': balance_swap_vendor_contract,
            'balance_token_owner': balance_token_owner
        })


class BuyToken(APIView):
    def post(self, request):
        props = BuyTokenProps(**request.data)
        w3 = Web3Model(props)
        w3.set_contract(ContractProps(request.data))

        contract = w3.get_contract('swapVendor')

        tk = contract.functions.tokens(props.contract_address).call()

        contract.functions.buyToken(
            props.contract_address
        ).transact({'from': props.owner_wallet_address, 'value': 100})

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
