from typing import Type, Union

from eth_account import Account
from web3 import Web3
from django.conf import settings
from web3.contract import Contract
from web3.middleware import construct_sign_and_send_raw_middleware

from ..payloads.swapVendor import SwapConstructorProps, BaseSwapProps
from ..services.contractService import get_contract_data


class Web3Model:
    __provider = Web3.HTTPProvider(
        settings.ETHEREUM_NETWORK
    )
    w3: Web3 = None
    __account = None
    __contract_instance: Union[Type[Contract], Contract] = None

    def __init__(self, props: BaseSwapProps):
        self.w3 = Web3(self.__provider)
        self.__account = Account.create(props.owner_wallet_address)
        self.w3.middleware_onion.add(construct_sign_and_send_raw_middleware(self.__account))
        self.w3.eth.default_account = props.owner_wallet_address

    def set_contract(self, props: SwapConstructorProps):
        abi, _ = get_contract_data(props.contract_name, props.contract_class_name)
        self.__contract_instance = self.w3.eth.contract(address=props.contract_address, abi=abi)

    def get_contract(self):
        return self.__contract_instance

    def get_account(self):
        return self.__account
