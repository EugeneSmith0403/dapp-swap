from typing import Type, Union

import web3
from eth_account import Account
from django.conf import settings
from web3.middleware import construct_sign_and_send_raw_middleware

from ..payloads.swapVendor import SwapConstructorProps, BaseSwapProps, SwapAddTokenProps
from ..services.contractService import get_contract_data


class ContractProps:
    contract_name = ''
    contract_class_name = ''
    contract_address = ''
    owner_wallet_address = ''

    def __init__(self, params: dict):
        self.contract_name = params.get('contract_name')
        self.contract_address = params.get('contract_address')
        self.contract_class_name = params.get('contract_class_name')
        self.owner_wallet_address = params.get('owner_wallet_address')


class Web3Model:
    __provider = web3.Web3.HTTPProvider(
        settings.ETHEREUM_NETWORK
    )
    w3: web3.Web3 = None
    __account = None
    __contract_instance: dict = {}

    def __init__(self, props: BaseSwapProps):
        self.w3 = web3.Web3(self.__provider)
        # self.__account = Account.create(props.owner_wallet_address)
        # self.w3.middleware_onion.add(construct_sign_and_send_raw_middleware(self.__account))
        # self.w3.eth.default_account = props.owner_wallet_address

    def set_contract(self, props: ContractProps, prefix: str = ''):
        abi, _ = get_contract_data(props.contract_name, props.contract_class_name)
        pr = prefix + '_' if prefix else ''
        prop = '{prefix}{name}'.format(prefix=prefix + '_', name=props.contract_name)
        self.__contract_instance[prop] = self.w3.eth.contract(address=props.contract_address, abi=abi)

    def get_contract(self, name: str):
        return self.__contract_instance[name]

    def get_account(self):
        return self.__account
