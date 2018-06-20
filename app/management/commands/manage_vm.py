import time
import os
import sys
import subprocess
from pathlib import Path
from shutil import copyfile
import textwrap
import socket
from contextlib import closing

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    #def add_arguments(self, parser):
    #    parser.add_argument('server_suffix', type=str)

    def running(self, server):
        try:
            output = subprocess.check_output('virsh domstate '+server, shell=True)
        except subprocess.CalledProcessError:
            return False
        else:
            if b'running' in output:
                return True
    
    def install_vm(self, server, img_path, mac, url, host, port):
        #path3 = Path(img_path)
        #if path3.exists():
        #    path3.unlink()
        #copyfile(base_img_path, img_path)        
        #cmd = 'virt-install --name %s --os-variant=ubuntu16.04 --ram 2048 --vcpus 2 --disk path=%s --import --noautoconsole --network network=default,mac=%s' % (server, img_path, mac)
        #cmd = 'virt-clone --name %s --mac %s --original bnbs --file %s' % (server, mac, img_path)
        #if self.running(server):
        #    cmd = 'virsh reboot ' + server
        #else:
        #    cmd = 'virsh start ' + server
        cmd = 'virsh reboot ' + server
        subprocess.check_call(cmd, shell=True)
        #if self.listening(host, port): 
        settings.STRICTREDIS.lpush('server', url)
    
    def reset(self, server, img_path, mac, url, host, port):
        values = settings.STRICTREDIS.lrange('server', 0, -1)
        print(values)
        print(url.encode())
        if not url.encode() in values:
            #subprocess.check_call('virsh destroy '+server, shell=True)
            #subprocess.check_call('virsh undefine '+server, shell=True)
            self.install_vm(server, img_path, mac, url, host, port)
            #subprocess.check_call('virsh start '+server, shell=True)
    
    def run(self, server, img_path, mac, url, host, port):
        #try:
        #    subprocess.check_call('virsh domstate '+server, shell=True)
        #except subprocess.CalledProcessError:
        #    pass
        #else:
        #    subprocess.check_call('virsh undefine '+server, shell=True)
        self.install_vm(server, img_path, mac, url, host, port)
        #subprocess.check_call('virsh start '+server, shell=True)
    
    def server_off(self, server):
        for i in range(10):
            if self.running(server):
                return False
            time.sleep(1)
        return False

    def listening(self, host, port):
        port = int(port)
        count = 0
        while count < 10:
            count += 1
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                if sock.connect_ex((host, port)) == 0:
                    return True
            time.sleep(1)
    
    def handle(self, *args, **options):
        heartbeat_path = '/home/notebook/heartbeat'
        server_suffixes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
        ports = {'01': '8888', '02': '8889', '03': '8890', '04': '8891', '05': '8892', '06': '8893', '07': '8894', '08': '8895', '09': '8896', '10': '8897'}
        while True:
            print('-------------------------------------------------------')
            for server_suffix in server_suffixes:
                server = 'nbs' + server_suffix
                print('######### '+server+' ############')
                mac = '52:54:00:6c:3c:' + server_suffix
                base_img_path = '/home/kvm/base_images/b' + server + '.img'
                img_path = '/home/kvm/images/' + server + '.img'
                host = 'finplane.com'
                port = ports[server_suffix]
                url = 'http://' + host + ':' + port
                path2 = heartbeat_path + '/' + server
                if self.running(server):
                    if Path(path2).exists():
                        diff = time.time() - os.path.getmtime(path2)
                        print(diff)
                        if diff > 60:
                            self.reset(server, img_path, mac, url, host, port)
                            Path(path2).touch()
                    else:
                        self.reset(server, img_path, mac, url, host, port)
                        Path(path2).touch()
                else:
                    self.run(server, img_path, mac, url, host, port)
                    Path(path2).touch()
            
                if self.server_off(server):
                    print('ERROR: server not running')
                    sys.exit(1)

            print('-------------------------------------------------------')
            time.sleep(1)
