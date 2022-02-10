from rest_framework import serializers
from ..models.client import Client
from ..serializers.requestTokenSerializaer import RequestTokenSerializer


class ClientSerializer(serializers.ModelSerializer):

    requests = RequestTokenSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'wallet', 'requests')
