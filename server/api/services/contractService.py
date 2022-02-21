import json
import os

from eth_account import Account
from solcx import compile_files
from django.conf import settings
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware


def make_contract_file_url(path: str, contract_name: str) -> str:
    return r'{path}{contract_name}'.format(path=path, contract_name=contract_name)


def make_parent_property_for_contract(contract_file_path: str, contract_class_name: str) -> str:
    return '{path}:{class_name}'.format(path=contract_file_path, class_name=contract_class_name)


def get_contract_data(contract_name: str, contract_class_name: str) -> tuple:
    if contract_name:
        built_file_name = '{contract_name}.json'.format(contract_name=contract_name)
        compile_file_name = '{contract_name}.sol'.format(contract_name=contract_name)
        contract_file_build = make_contract_file_url(
            path=settings.BUILT_CONTRACTS_DIR,
            contract_name=built_file_name
        )
        contract_file_path = make_contract_file_url(
            path=settings.CONTRACTS_URL,
            contract_name=compile_file_name
        )

        jsonProp = make_parent_property_for_contract(contract_file_path, contract_class_name)

        with open(contract_file_build, 'r') as file:
            str = file.read()
            compiled_sol = json.loads(str)
            contr = compiled_sol[jsonProp]
            abi = contr['abi']
            bin = contr['bin']
        return abi, bin


def compile_contract(contract_name: str) -> None:
    if contract_name:
        compile_file_name = '{contract_name}.sol'.format(contract_name=contract_name)
        built_file_name = '{contract_name}.json'.format(contract_name=contract_name)
        contract_file_path = make_contract_file_url(
            path=settings.CONTRACTS_URL,
            contract_name=compile_file_name
        )
        contract_file_build = make_contract_file_url(
            path=settings.BUILT_CONTRACTS_DIR,
            contract_name=built_file_name
        )

        if os.path.exists(contract_file_build):
            os.remove(contract_file_build)

        with open(contract_file_build, 'a+') as file:
            if not file.read():
                contract: dict = compile_files(
                    contract_file_path,
                    import_remappings={
                        '@baseOpenzeppelin': settings.OPEN_ZEPPELIN_URL,
                    },
                    output_values=['abi', 'bin']
                )
                contractJson = json.dumps(contract)
                print(contractJson, file=file)
    else:
        raise Exception('contract_name arguments not empty')


def _deploy_contract(
        contract_name: str,
        contract_class_name: str,
        contract_props: dict,
        provider,
        owner_wallet_address: str
) -> str:
    abi, bin = get_contract_data(contract_name, contract_class_name)
    if abi and bin:
        w3 = Web3(provider)
        acct = Account.create(owner_wallet_address)
        w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
        w3.eth.default_account = owner_wallet_address

        contract = w3.eth.contract(abi=abi, bytecode=bin)

        transaction = {
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.getTransactionCount(owner_wallet_address),
        }

        contract_data = contract.constructor(**contract_props).buildTransaction(transaction)
        tx_hash = w3.eth.send_transaction(contract_data)
        return w3.eth.get_transaction_receipt(tx_hash)['contractAddress']
    else:
        raise Exception('some problem with abi and bin for contract!')


def deploy_contract(
        contract_name: str,
        contract_class_name: str,
        contract_props: dict,
        provider,
        owner_wallet_address: str
) -> str:
    try:
        return _deploy_contract(
            contract_name,
            contract_class_name,
            contract_props,
            provider,
            owner_wallet_address
        )
    except Exception:
        raise Exception('deploy contract error!')
