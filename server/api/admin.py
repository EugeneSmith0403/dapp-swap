from django.contrib import admin
from .models.heroModel import Hero
from .models.requestToken import RequestToken
from .models.requestToken import Client
from .models.user import User



# Register your models here.

models = User, Hero, RequestToken, Client
admin.site.register(models)
