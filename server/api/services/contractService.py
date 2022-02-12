import json
from eth_account import Account
from solcx import compile_files
from django.conf import settings
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
from django.apps import apps


def make_contract_file_url(path: str, contract_name: str) -> str:
    return r'{path}{contract_name}'.format(path=path, contract_name=contract_name)


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
        with open(contract_file_build, 'r+') as file:
            if not file.read():
                contract: dict = compile_files(
                    contract_file_path,
                    base_path=settings.OPEN_ZEPPELIN_URL,
                    output_values=['abi', 'bin']
                )
                contractJson = json.dumps(contract)
                print(contractJson, file=file)
    else:
        raise Exception('contract_name arguments not empty')


def deploy_contract(
        contract_name: str,
        contract_class_name: str,
        contract_props: dict,
        provider
) -> str:
    built_file_name = '{contract_name}.json'.format(contract_name=contract_name)
    compile_file_name = '{contract_name}.sol'.format(contract_name=contract_name)
    contract_file_path = make_contract_file_url(
        path=settings.CONTRACTS_URL,
        contract_name=compile_file_name
    )
    jsonProp = '{path}:{class_name}'.format(path=contract_file_path, class_name=contract_class_name)
    contract_file_build = make_contract_file_url(
        path=settings.BUILT_CONTRACTS_DIR,
        contract_name=built_file_name,
    )

    w3 = Web3(provider)
    acct = Account.create(settings.CONTRACT_OWNER_WALLET_ADDRESS)
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
    w3.eth.default_account = settings.CONTRACT_OWNER_WALLET_ADDRESS

    with open(contract_file_build, 'r') as file:
        str = file.read()
        compiled_sol = json.loads(str)
        contr = compiled_sol[jsonProp]
        abi = contr['abi']
        bin = contr['bin']
        contract = w3.eth.contract(abi=abi, bytecode=bin)

    transaction = {
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.getTransactionCount(settings.CONTRACT_OWNER_WALLET_ADDRESS),
    }

    contract_data = contract.constructor(**contract_props).buildTransaction(transaction)
    return w3.eth.send_transaction(contract_data).hex()
