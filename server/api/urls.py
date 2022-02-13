# myapi/urls.py
from django.urls import include, path
from rest_framework import routers

from .views.heroSet import HeroSet
from .views.contractCompiler import ContractCompiler
from .views.swap import AddedToken, BuyToken, SellToken, Swap

router = routers.DefaultRouter()
router.register(r'heroes', HeroSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('deployContract/', ContractCompiler.as_view()),
    path('swapVendor/addToken', AddedToken.as_view()),
    path('swapVendor/buyToken', BuyToken.as_view()),
    path('swapVendor/sailToken', SellToken.as_view()),
    path('swapVendor/swap', Swap.as_view()),
]