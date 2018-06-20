import time
import os
import sys
import subprocess
from pathlib import Path

server_suffix = sys.argv[1]
server = 'nbs' + sys.argv[1]
mac = '52:54:00:6c:3c:' + server_suffix
base_server = 'bnbs'
img_path = '/home/kvm/' + server + '.img'
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

def clone(server):
    path3 = Path(img_path)
    if path3.exists():
        path3.unlink()
    cmd = 'virt-clone --name %s --mac %s --original %s --file %s' % (server, mac, base_server, img_path)
    subprocess.check_call(cmd, shell=True)

def reset(server):
    subprocess.check_call('virsh destroy '+server, shell=True)
    subprocess.check_call('virsh undefine '+server, shell=True)
    clone(server)
    subprocess.check_call('virsh start '+server, shell=True)

def run(server):
    try:
        subprocess.check_call('virsh domstate '+server, shell=True)
    except subprocess.CalledProcessError:
        pass
    else:
        subprocess.check_call('virsh undefine '+server, shell=True)
    clone(server)
    subprocess.check_call('virsh start '+server, shell=True)

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
