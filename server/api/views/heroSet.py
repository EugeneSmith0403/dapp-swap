from rest_framework import viewsets

from ..models.heroModel import Hero
from ..serializers.heroSerializer import HeroSerializer

class HeroSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer
