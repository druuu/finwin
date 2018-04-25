from __future__ import absolute_import, unicode_literals
import time
import pwd
from subprocess import check_call
import socket
from contextlib import closing

from celery import shared_task
from django.conf import settings
from app.models import Notebook


@shared_task
def add(x, y):
    with open('/tmp/hello', 'w') as f:
        f.write('adsi')
    return x + y


############################### notebook runner ############################
def listening(port):
    listening = False
    count = 0
    while count < 10:
        count += 1
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if sock.connect_ex(('127.0.0.1', port)) == 0:
                return True
        listening = True
        time.sleep(1)
    return listening


def port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


def notebook():
    port2 = port()
    base_url = username = uuid.uuid4().hex
    time2 = int(time.time())
    heartbeat = time2 + 60
    notebook = Notebook.objects.create(username=username, port=port2, base_url=base_url, status=0, time2=time2, heartbeat=heartbeat)
    cmd = '%s/scripts/launch_jupyter.o %d %s %s &' % (settings.BASE_DIR, port2, username, base_url)
    check_call(cmd, shell=True)
    if listening(port2):
        notebook.status = 1
    else:
        notebook.status = 2
    notebook.time3 = int(time.time())
    notebook.save()

@shared_task
def notebook2():
    pass
############################################################


####################### culling ########################
def cull2(notebook):
    print('>>>>>>>> culling ' + notebook.username)
    try:
        pwd.getpwnam(notebook.username)
        cmd = 'pkill -u %s; sleep 2 && pkill -9 -u %s; userdel -r %s' % (notebook.username, notebook.username, notebook.username)
        check_call(cmd, shell=True)
    except KeyError:
        print('User %s does not exist.' % notebook.username)


@shared_task
def cull():
    notebooks = Notebook.objects.all()
    for notebook in notebooks:
        if int(time.time()) - notebook.heartbeat > 30:
            cull2(notebook)
##########################################################
