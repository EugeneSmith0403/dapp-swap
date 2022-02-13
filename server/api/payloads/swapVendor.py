class BaseSwapProps:
    owner_wallet_address: str
    contract_name: str
    contract_class_name: str


class SwapConstructorProps(BaseSwapProps):
    contract_props: dict

    def __init__(self, **props):
        self.owner_wallet_address = props.get('owner_wallet_address')
        self.contract_name = props.get('contract_name')
        self.contract_class_name = props.get('contract_class_name')
        self.contract_props = props.get('contract_props')


class SwapAddTokenProps(BaseSwapProps):
    contract_address: str
    liquidity: str

    def __init__(self, **props):
        self.owner_wallet_address = props.get('owner_wallet_address')
        self.contract_address = props.get('contract_address')
        self.liquidity = props.get('liquidity')
        self.contract_name = props.get('contract_name')
        self.contract_class_name = props.get('contract_class_name')


class BuyTokenProps(BaseSwapProps):
    contract_address: str

    def __init__(self, **props):
        self.owner_wallet_address = props.get('owner_wallet_address')
        self.contract_address = props.get('contract_address')
        self.contract_name = props.get('contract_name')
        self.contract_class_name = props.get('contract_class_name')


class SellTokenProps(BaseSwapProps):
    contract_address: str
    amount: str

    def __init__(self, **props):
        self.owner_wallet_address = props.get('owner_wallet_address')
        self.contract_address = props.get('contract_address')
        self.amount = props.get('amount')
        self.contract_name = props.get('contract_name')
        self.contract_class_name = props.get('contract_class_name')


class SwapProps(BaseSwapProps):
    buy_token_address: str
    sail_token_address: str
    sail_token_amount: int

    def __init__(self, **props):
        self.owner_wallet_address = props.get('owner_wallet_address')
        self.contract_address = props.get('buy_token_address')
        self.sail_token_address = props.get('sail_token_address')
        self.sail_token_amount = props.get('sail_token_address')
        self.contract_name = props.get('contract_name')
        self.contract_class_name = props.get('contract_class_name')