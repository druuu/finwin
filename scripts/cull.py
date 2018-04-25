import os
import time
import subprocess

#from django.conf import settings


HEARTBEAT_DIR = '/home/filtered/heartbeat'
LOGS_DIR = '/home/filtered/logs'
def cull():
    now = time.time()
    files = os.listdir(HEARTBEAT_DIR)
    for path2 in files:
        path3 = HEARTBEAT_DIR + '/' + path2
        if (now - os.stat(path3).st_mtime) > 120:
            cmd = 'pkill -u %s; sleep 5 && pkill -9 -u %s; userdel -r %s && rm %s' % (path2, path2, path2, path3)
            try:
                subprocess.check_call(cmd, shell=True)
            except Exception as e:
                print(str(e))


while True:
    print('################################')
    cull()
    time.sleep(10)
