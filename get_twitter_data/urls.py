from django.conf.urls import url

from .views import *

app_name = 'get_twitter_data'
urlpatterns = [
    url(r'^search_keyword/', search_keyword, ),
]
