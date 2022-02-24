from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response

from ..models.deployedContract import DeployedContract
from ..models.web3 import Web3Model, ContractProps
from ..payloads.swapVendor import SwapAddTokenProps, BuyTokenProps, SellTokenProps, SwapProps, BaseSwapProps


def convert_swap_vendor_data(props):
    queryName = 'swapVendor_{wallet}'.format(wallet=settings.CONTRACT_OWNER_WALLET_ADDRESS)

    item = DeployedContract.objects.filter(contract_name=queryName).all()

    if not item:
        raise Exception('Contract doesn\'t exist!')

    return {
        'contract_name': 'swapVendor',
        'contract_class_name': 'SwapVendor',
        'contract_address': item[0].address_contract
    }


class AddedToken(APIView):
    def post(self, request):
        props = SwapAddTokenProps(**request.data)
        w3 = Web3Model(props)

        swap_contract_props = convert_swap_vendor_data(props)

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

        token_contract.functions.approve(swap_props.contract_address, liquidity) \
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

        # add swap contract
        swap_contract_dict = convert_swap_vendor_data(props)
        swap_contract_props = ContractProps(swap_contract_dict)
        w3.set_contract(swap_contract_props)

        # add token contract
        w3.set_contract(ContractProps(request.data))
        swap_contract = w3.get_contract('swapVendor')
        token_contract = w3.get_contract('createToken')

        transactProps = {'from': props.owner_wallet_address, 'value': int(props.amount)}

        swap_contract.functions.buyToken(
            props.contract_address
        ).transact(transactProps)

        owner_balance_bought_token = token_contract.functions.balanceOf(props.owner_wallet_address).call()

        return Response({'result': 'ok', 'owner_balance_bought_token': owner_balance_bought_token})


class SellToken(APIView):
    def post(self, request):
        props = SellTokenProps(**request.data)
        w3 = Web3Model(props)
        w3.set_contract(ContractProps(request.data))

        # add swap contract
        swap_contract_dict = convert_swap_vendor_data(props)
        swap_contract_props = ContractProps(swap_contract_dict)
        w3.set_contract(swap_contract_props)

        swap_contract = w3.get_contract('swapVendor')
        token_contract = w3.get_contract('createToken')
        transactProps = {
            'from': props.owner_wallet_address,
        }

        balance = token_contract.functions.balanceOf(props.owner_wallet_address).call()

        token_contract.functions.approve(props.owner_wallet_address, balance) \
            .transact(transactProps)

        swap_contract.functions.sellToken(
            props.contract_address,
            int(props.amount)
        ).transact({'from': props.owner_wallet_address})

        return Response({'result': 'ok'})


class Swap(APIView):
    def post(self, request):
        props = SwapProps(**request.data)
        w3 = Web3Model(props)
        swap_contract_props = convert_swap_vendor_data(props)
        swap_props = ContractProps(swap_contract_props)
        w3.set_contract(swap_props)
        transactProps = {
            'from': props.owner_wallet_address,
        }

        sell_token_dict = {
            "contract_name": "createToken",
            "contract_class_name": "MyToken",
            "contract_address": props.sell_token_address
        }
        w3.set_contract(ContractProps(sell_token_dict), 'sell')

        buy_token_dict = {
            "contract_name": "createToken",
            "contract_class_name": "MyToken",
            "contract_address": props.buy_token_address
        }
        w3.set_contract(ContractProps(buy_token_dict), 'buy')

        swap_contract = w3.get_contract('swapVendor')
        buy_token = w3.get_contract('buy_createToken')
        sell_token = w3.get_contract('sell_createToken')

        sell_token.functions.approve(props.owner_wallet_address, int(props.sell_token_amount)).transact(transactProps)
        buy_token.functions.approve(swap_contract.address, int(props.sell_token_amount)).transact(transactProps)

        swap_contract.functions.swap(
            props.sell_token_address,
            int(props.sell_token_amount),
            props.buy_token_address
        ).transact({'from': props.owner_wallet_address})

        return Response({'result': 'ok'})
