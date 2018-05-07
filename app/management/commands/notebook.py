import time, uuid
import pwd
from subprocess import check_call
import socket
from contextlib import closing

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
#from app.models import Notebook


CERTFILE = settings.BASE_DIR + '/scripts/fullchain.pem' 
KEYFILE = settings.BASE_DIR + '/scripts/privkey.pem'

class Command(BaseCommand):
    def listening(self, port):
        count = 0
        while count < 10:
            count += 1
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                if sock.connect_ex(('127.0.0.1', port)) == 0:
                    return True
            time.sleep(1)
    
    def port(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(('', 0))
        addr, port = tcp.getsockname()
        tcp.close()
        return port
    
    def notebook(self):
        port2 = self.port()
        base_url = username = uuid.uuid4().hex
        print('>>>>>> running %s' % username)
        time2 = int(time.time())
        #heartbeat = time2 + 60
        heartbeat = time2
        #notebook = Notebook.objects.create(username=username, port=port2, base_url=base_url, status=0, time2=time2, heartbeat=heartbeat)
        cmd = '%s/scripts/launch_jupyter.o %d %s %s %s %s &' % (settings.BASE_DIR, port2, username, base_url, CERTFILE, KEYFILE)
        check_call(cmd, shell=True)
        if self.listening(port2):
            #notebook.status = 1
            #notebook.time3 = int(time.time())
            #notebook.save()
            settings.STRICTREDIS.lpush('server', '%s:%d' % (username, port2))
        else:
            #notebook.status = 2
            #notebook.time3 = int(time.time())
            #notebook.save()
            #TODO: kill this notebook
            pass
    
    def running_notebooks(self):
        return 10

    def handle(self, *args, **options):
        while True:
            #notebooks = Notebook.objects.filter(status=1)
            diff = settings.TOTAL_NOTEBOOKS - self.running_notebooks()
            print('>>>>>>>>> diff: %d' % diff)
            for i in range(diff):
                self.notebook()
            time.sleep(1)
