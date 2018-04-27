import time

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf import settings
from app.models import *


def notebook(request):
    notebook = Notebook.objects.filter(lock=False).first()
    if notebook:
        url = 'https://%s:%d/%s' % (settings.DOMAIN, notebook.port, notebook.base_url)
        notebook.lock = True
        notebook.save()
        #return HttpResponseRedirect(url)
        return render(request, 'app/notebook.html', {'url': url, 'url2': '/heartbeat?username='+notebook.username})


def heartbeat(request):
    username = request.GET['username']
    notebook = Notebook.objects.get(username=username)
    notebook.heartbeat = int(time.time())
    notebook.save()
    return HttpResponse('ok')
