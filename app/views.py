import os
import uuid
import random, string
from urllib.parse import quote_plus
import json
import nbformat

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect

from app import tasks


def demo(request):
    tasks.add.delay(2, 3)
    return HttpResponse('ok')
