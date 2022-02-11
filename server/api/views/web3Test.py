from rest_framework.views import APIView
from rest_framework.response import Response


from ..services.contractCompiler import compile_contract


class Web3Test(APIView):
    def get(self, request):
        compile_contract('createToken')
        return Response({'result': 'Ok'})
