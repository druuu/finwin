from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf import settings
from app.models import *


def notebook(request):
    notebook = Notebook.objects.filter(lock=False).first()
    if notebook:
        url = 'http://%s:%d/%s' % (settings.DOMAIN, notebook.port, notebook.base_url)
        notebook.lock = True
        notebook.save()
        return HttpResponseRedirect(url)
