import os
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.conf import settings


class Command(BaseCommand):
    def clone(self, server, mac, img_path, base_server):
        path3 = Path(img_path)
        if path3.exists():
            path3.unlink()
        cmd = 'virt-clone --name %s --mac %s --original %s --file %s' % (server, mac, base_server, img_path)
        subprocess.check_call(cmd, shell=True)

    def destroy(self, server):
        cmd = 'virsh destroy ' + server
        subprocess.call(cmd, shell=True)

    def undefine(self, server):
        cmd = 'virsh undefine ' + server
        subprocess.call(cmd, shell=True)

    def handle(self, *args, **options):
        servers = []
        macs = []
        img_paths = []
        for i in range(settings.TOTAL_VMS):
            if i < 9:
                server_suffix = '0%d' % (i+1)
            else:
                server_suffix = '%d' % (i+1)
            servers.append('bnbs'+server_suffix)
            macs.append('52:54:00:6c:3b:'+server_suffix)
            img_paths.append('/home/kvm/base_images/bnbs'+server_suffix+'.img')
        
        base_server = 'bnbs'
        for server, mac, img_path in zip(servers, macs, img_paths):
            self.destroy(server)
            self.undefine(server)
            self.clone(server, mac, img_path, base_server)
