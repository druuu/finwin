import time
from pathlib import Path
from urllib import parse

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf import settings
from app.models import *


def notebook(request):
    url = settings.STRICTREDIS.lpop('server')
    return HttpResponseRedirect(url)


def heartbeat(request):
    server = request.GET['server']
    Path(settings.HEARTBEAT_DIR + '/' + server).touch()
    return HttpResponse('ok')

def none(request):
    return HttpResponse('the servers are all occupied, please try after sometime.')
