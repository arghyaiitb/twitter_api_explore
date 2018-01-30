from django.conf.urls import url

from .views import *

app_name='custom_search'
urlpatterns = [
    url(r'^filtered_search/', filtered_search, ),
    url(r'^group_search/', group_search, ),
    url(r'^plain_search/', plain_search, ),
]
