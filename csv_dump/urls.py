from django.conf.urls import url

from .views import *

app_name = 'csv_dump'
urlpatterns = [
    url(r'^csv_data_dump/', csv_data_dump, ),
]
