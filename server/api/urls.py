# myapi/urls.py
from django.urls import include, path
from requests import Response
from rest_framework import routers
from rest_framework.decorators import api_view

from .views.heroSet import HeroSet
from .views.web3 import Web3Test

router = routers.DefaultRouter()
router.register(r'heroes', HeroSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('web3/', Web3Test.as_view())
]