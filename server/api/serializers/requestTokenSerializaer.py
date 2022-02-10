from rest_framework import serializers
from ..models.requestToken import RequestToken


class RequestTokenSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = RequestToken
        fields = ('id', 'name', 'liquidityAmount', 'symbol', 'partial', 'status')
