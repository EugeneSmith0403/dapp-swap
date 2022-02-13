from rest_framework.views import APIView
from web3 import Web3
from django.conf import settings
from rest_framework.response import Response

provider = Web3.HTTPProvider(
    settings.ETHEREUM_NETWORK
)

w3 = Web3(provider)


class addToken(APIView):
    def post(self, request):
        return Response({ 'result': 'ok' })

class BuyToken(APIView):
    def post(self, request):
        return Response({ 'result': 'ok' })


class SailToken(APIView):
    def post(self, request):
        return Response({ 'result': 'ok' })


class Swap(APIView):
    def post(self, request):
        return Response({ 'result': 'ok' })
