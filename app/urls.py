from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    #re_path('^health', health, name='health'),
    re_path('^demo', demo, name='demo'),
]
