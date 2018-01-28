from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^search_keyword/', search_keyword, ),
]
