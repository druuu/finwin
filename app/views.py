import time
from pathlib import Path

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf import settings
from app.models import *


def notebook(request):
    url = settings.STRICTREDIS.lpop('server')
    print(url)
    return HttpResponseRedirect(url)


def heartbeat(request):
    username = request.GET['username']
    Path(settings.HEARTBEAT_DIR + '/' + username, exist_ok=True).touch()
    return HttpResponse('ok')

def none(request):
    return HttpResponse('the servers are all occupied, please try after sometime.')
