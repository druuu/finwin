import time
from pathlib import Path
from urllib import parse

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from app.models import *
from app.forms import *


def index(request):
    if request.method == "POST":
        user = authenticate(username=request.POST.get('email'), \
                password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next') or '/')
        else:
            response_data = {'message': 'The username and password are incorrect.'}
        return render(request, 'signin.html', response_data)

    elif request.user.is_authenticated:
        return render(request, 'home.html')

    else:
        return render(request, 'signin.html')


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"error": False})
        else:
            return JsonResponse({"error": True, "errors": form.errors})
    form = UserForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def notebook(request):
    nb_url = request.GET['url']
    try:
        vm = VM.objects.get(user=request.user)
    except ObjectDoesNotExist:
        pass
    else:
        if (vm.is_active):
            yid = slugify(nb_url) + vm.base_url
            url = 'http://%s:%d/%s/notebooks/template.ipynb?url=%s&id=%s' \
                    % (settings.DOMAIN, vm.port, vm.base_url, nb_url, yid)
            print(url, '22222222222222222222')
            return HttpResponseRedirect(url)

    url = settings.STRICTREDIS.lpop('server')
    if url:
        url = url.decode()
        parsed_url = parse.urlparse(url)
        base_url = parsed_url.path.split('/')[1]
        vm = VM.objects.create(base_url=base_url, \
                user=request.user, port=parsed_url.port, last_modified=datetime.datetime.now())
        print(vm)
        yid = slugify(nb_url) + base_url
        url = '%s/notebooks/template.ipynb?url=%s&id=%s' \
                % (url, nb_url, yid)
        print(url, '1111111111111111111')
    return HttpResponseRedirect(url)


@csrf_exempt
@login_required
def save(request):
    print(request.POST.keys())
    notebook = request.POST['nb']
    nb_url = request.POST['nb_url']
    port = request.POST['port']
    settings.DB.user_data.update({'id': request.user.id, 'nb_url': nb_url}, \
            {'$set': {'notebook': notebook}}, upsert=True)

    response = HttpResponse('ok')
    response["Access-Control-Allow-Origin"] = "http://%s:%s" % (settings.DOMAIN, port)
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    response['Access-Control-Allow-Credentials'] = 'true'
    return response


def heartbeat(request):
    base_url = request.GET['base_url']
    share_url = request.GET['share_url']
    port = int(request.GET['port'])
    last_modified = datetime.datetime.now()

    if request.user.is_authenticated:
        try:
            vm = VM.objects.get(port=port)
            print(vm)
            vm.last_modified = last_modified
            vm.save()
            response = HttpResponse('ok')
        except ObjectDoesNotExist:
            response = HttpResponse('expired')
    else:
        url = 'https://' + settings.DOMAIN + '/?next=' + parse.quote_plus(share_url)
        response = HttpResponse(url, status=401)

    response["Access-Control-Allow-Origin"] = "http://%s:%s" % (settings.DOMAIN, port)
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    response['Access-Control-Allow-Credentials'] = 'true'
    return response


def none(request):
    return HttpResponse('the servers are all occupied, please try after sometime.')
