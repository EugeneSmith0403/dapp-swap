import json

from solcx import compile_files
from pickle import dump, load
from django.conf import settings
from web3 import Web3


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
        contract: dict = compile_files(
            contract_file_path,
            base_path=settings.OPEN_ZEPPELIN_URL,
            output_values=['abi', 'bin']
        )
        contractJson = json.dumps(contract)
        with open(contract_file_build, 'w') as file:
            print(contractJson, file=file)
    else:
        raise Exception('contract_name arguments not empty')


def deploy_contract(contract_name: str, contract_class_name, provider):
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

    with open(contract_file_build, 'r') as file:
        str = file.read()
        compiled_sol = json.loads(str)
        contr = compiled_sol[jsonProp]
        abi = contr['abi']
        bin = contr['bin']
    w3 = Web3(provider())
    contract = w3.eth.contract(abi=abi, bytecode=bin)
    props = {
        'name': "TS",
        'symbol': 'TS',
        '_amount': 1000000000000000000,
        'partialPrice': 1
    }
    print(contract.constructor(**props).transact({'from': w3.eth.account[0]}))
