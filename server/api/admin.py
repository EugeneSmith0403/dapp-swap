from django.contrib import admin

from .models.deployedContract import DeployedContract
from .models.heroModel import Hero
from .models.requestToken import RequestToken
from .models.requestToken import Client
from .models.user import User



# Register your models here.

models = User, Hero, RequestToken, Client, DeployedContract
admin.site.register(models)
