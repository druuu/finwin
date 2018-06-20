import time
import os
import sys
import subprocess
from pathlib import Path
from shutil import copyfile

server_suffix = sys.argv[1]
server = 'nbs' + sys.argv[1]
mac = '52:54:00:6c:3c:' + server_suffix
base_img_path = '/home/kvm/base_images/b' + server + '.img'
img_path = '/home/kvm/images/' + server + '.img'
heartbeat_path = '/home/notebook/heartbeat'

path2 = heartbeat_path + '/' + server
Path(path2).touch()

def running(server):
    try:
        output = subprocess.check_output('virsh domstate '+server, shell=True)
    except subprocess.CalledProcessError:
        return False
    else:
        if b'running' in output:
            return True

def install_vm(server, base_img_path, img_path, mac):
    path3 = Path(img_path)
    if path3.exists():
        path3.unlink()
    copyfile(base_img_path, img_path)        
    cmd = 'virt-install --name %s --os-variant=ubuntu16.04 --ram 2048 --vcpus 2 --disk path=%s --import --noautoconsole --network network=default,mac=%s' % (server, img_path, mac)
    subprocess.check_call(cmd, shell=True)

def reset(server):
    subprocess.check_call('virsh destroy '+server, shell=True)
    subprocess.check_call('virsh undefine '+server, shell=True)
    install_vm(server, base_img_path, img_path, mac)

def run(server):
    try:
        subprocess.check_call('virsh domstate '+server, shell=True)
    except subprocess.CalledProcessError:
        pass
    else:
        subprocess.check_call('virsh undefine '+server, shell=True)
    install_vm(server, base_img_path, img_path, mac)

def server_off(server):
    for i in range(10):
        if running(server):
            return False
        time.sleep(1)
    return False


while True:
    print('\n############################################################')
    if running(server):
        diff = time.time() - os.path.getmtime(path2)
        print('time diff', diff)
        if diff > 30:
            print('resetting server...')
            reset(server)
            Path(path2).touch()
    else:
        print('creating server...')
        run(server)
        Path(path2).touch()

    if server_off(server):
        print('ERROR: server not running')
        sys.exit(1)
    print('############################################################\n')
    time.sleep(3)
