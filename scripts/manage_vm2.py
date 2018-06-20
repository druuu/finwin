import time
import os
import sys
import subprocess
from pathlib import Path
from shutil import copyfile
import textwrap

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('server_suffix', type=str)

    def running(self, server):
        try:
            output = subprocess.check_output('virsh domstate '+server, shell=True)
        except subprocess.CalledProcessError:
            return False
        else:
            if b'running' in output:
                return True
    
    def install_vm(self, server, base_img_path, img_path, mac):
        path3 = Path(img_path)
        if path3.exists():
            path3.unlink()
        copyfile(base_img_path, img_path)        
        cmd = 'virt-install --name %s --os-variant=ubuntu16.04 --ram 2048 --vcpus 2 --disk path=%s --import --noautoconsole --network network=default,mac=%s' % (server, img_path, mac)
        subprocess.check_call(cmd, shell=True)
    
    def reset(self, server, base_img_path, img_path, mac):
        subprocess.check_call('virsh destroy '+server, shell=True)
        subprocess.check_call('virsh undefine '+server, shell=True)
        self.install_vm(server, base_img_path, img_path, mac)
    
    def run(self, server, base_img_path, img_path, mac):
        try:
            subprocess.check_call('virsh domstate '+server, shell=True)
        except subprocess.CalledProcessError:
            pass
        else:
            subprocess.check_call('virsh undefine '+server, shell=True)
        self.install_vm(server, base_img_path, img_path, mac)
    
    def server_off(self, server):
        for i in range(10):
            if self.running(server):
                return False
            time.sleep(1)
        return False
    
    def handle(self, *args, **options):
        server_suffix = options['server_suffix']
        server = 'nbs' + server_suffix
        mac = '52:54:00:6c:3c:' + server_suffix
        base_img_path = '/home/kvm/base_images/b' + server + '.img'
        img_path = '/home/kvm/images/' + server + '.img'
        heartbeat_path = '/home/notebook/heartbeat'
        path2 = heartbeat_path + '/' + server
        Path(path2).touch()
        while True:
            if self.running(server):
                diff = time.time() - os.path.getmtime(path2)
                if diff > 30:
                    self.reset(server, base_img_path, img_path, mac)
                    Path(path2).touch()
            else:
                self.run(server, base_img_path, img_path, mac)
                Path(path2).touch()
        
            if self.server_off(server):
                print('ERROR: server not running')
                sys.exit(1)
            time.sleep(3)
