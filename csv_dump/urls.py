from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^csv_data_dump/', csv_data_dump, ),
]
