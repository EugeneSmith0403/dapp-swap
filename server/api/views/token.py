from rest_framework.views import APIView
from web3 import Web3

from server.server import settings

provider = Web3.HTTPProvider(
    settings.ETHEREUM_NETWORK
)

w3 = Web3(provider)


class BuyToken(APIView):
    def post(self, request):
        pass


class SailToken(APIView):
    def post(self, request):
        pass


class Swap(APIView):
    def post(self, request):
        pass
