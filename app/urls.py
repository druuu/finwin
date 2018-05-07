from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    #re_path('^health', health, name='health'),
    re_path('^notebook', notebook, name='notebook'),
    re_path('^heartbeat', heartbeat, name='heartbeat'),
    re_path('^None', none, name='none'),
]
