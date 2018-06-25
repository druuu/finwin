import time
import os
import sys
import subprocess
from pathlib import Path
from multiprocessing import Process
import socket
from contextlib import closing
import uuid
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from app.models import VM



def notebook_server_started(vm_host, vm_port, url):
    count = 0
    while count < 10:
        count += 1
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            print('notebookkkkkkkkkkkkkk', count)
            if sock.connect_ex((vm_host, int(vm_port))) == 0:
                return True
        time.sleep(1)
    print('errrrrrrrrrrrrrrrrrrrrrrrr', url)
    return False

def push_to_redis_on_listening(vm_host, vm_port, url, base_url):
    count = 0
    while count < 10:
        count += 1
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            print('sshhhhhhhhhhhhhhhhhhhhh', count)
            if sock.connect_ex((vm_host, 22)) == 0:
                cmd = """ssh -o StrictHostKeyChecking=no %s 'echo c.NotebookApp.base_url=\\"%s\\" \
                        >> ~/.jupyter/jupyter_notebook_config.py && supervisorctl start \
                        notebook'""" % (vm_host, base_url)
                print(cmd)
                subprocess.check_call(cmd, shell=True)
                if notebook_server_started(vm_host, vm_port, url):
                    print(url, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                    settings.STRICTREDIS.lpush('server', url)
                return
        time.sleep(1)

class Command(BaseCommand):
    def running(self, server):
        try:
            output = subprocess.check_output('virsh domstate '+server, shell=True)
        except subprocess.CalledProcessError:
            return False
        else:
            if b'running' in output:
                return True
    
    def reset(self, server):
        if self.running(server):
            cmd = 'virsh destroy %s && virsh start %s' % (server, server)
        else:
            cmd = 'virsh start %s' % (server)
        subprocess.check_call(cmd, shell=True)

    def handle(self, *args, **options):
        ports = {'01': '8888', '02': '8889', '03': '8890', '04': '8891', '05': '8892', '06': '8893', \
                '07': '8894', '08': '8895', '09': '8896', '10': '8897', '11': '8898', '12': '8899', \
                '13': '8900', '14': '8901', '15': '8902', '16': '8903', '17': '8904', '18': '8905', \
                '19': '8906', '20': '8907', '21': '8908', '22': '8909', '23': '8910', '24': '8911', \
                '25': '8912', '26': '8913', '27': '8914', '28': '8915', '29': '8916', '30': '8917'}
        vm_port = '8888'
        death_note = {}
        while True:
            print('--------------------------------------------')
            urls = settings.STRICTREDIS.lrange('server', 0, -1)
            urls = [b'/'.join(i.split(b'/')[:-1]) for i in urls]
            for i in range(settings.TOTAL_VMS):
                if i < 9:
                    server_suffix = '0%d' % (i+1)
                else:
                    server_suffix = '%d' % (i+1)
                server = 'nbs' + server_suffix
                vm_host = settings.PARTIAL_IP + server_suffix
                port = ports[server_suffix]
                base_url = uuid.uuid4().hex
                url = ('http://' + settings.DOMAIN + ':' + port + '/' + base_url).encode()
                url2 = ('http://' + settings.DOMAIN + ':' + port).encode()
                path2 = settings.HEARTBEAT_DIR + '/' + server
                if not url2 in urls:
                    try:
                        print(VM.objects.all())
                        print('#################################')
                        vm = VM.objects.get(port=port)
                        print('ininininininini')
                    except ObjectDoesNotExist:
                        if server in death_note:
                            if death_note.get(server) > 5:
                                self.reset(server)
                                del death_note[server]
                                Process(target=push_to_redis_on_listening, \
                                        args=(vm_host, vm_port, url, base_url)).start()
                            else:
                                death_note[server] += 1
                        else:
                            death_note[server] = 1
                    else:
                        if (datetime.datetime.now()-vm.last_modified).total_seconds() > settings.TIMEOUT:
                            self.reset(server)
                            vm.delete()
                            if server in death_note:
                                del death_note[server]
                            Process(target=push_to_redis_on_listening, \
                                    args=(vm_host, vm_port, url, base_url)).start()
            time.sleep(3)
