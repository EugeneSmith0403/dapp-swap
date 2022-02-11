from solcx import compile_files
from pickle import dump
from django.conf import settings


def make_contract_file_url(path: str, contract_name: str) -> str:
    return r'{path}{contract_name}'.format(path=path, contract_name=contract_name)


def compile_contract(contract_name: str) -> None:
    if contract_name:
        compile_file_name = '{contract_name}.sol'.format(contract_name=contract_name)
        built_file_name = '{contract_name}.txt'.format(contract_name=contract_name)
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
            base_path=settings.OPEN_ZEPPELIN_URL
        )
        print(contract_file_build)
        with open(contract_file_build, 'wb') as file:
            dump(contract, file)
    else:
        raise Exception('contract_name arguments not empty')


