import time
import os
import pwd
from subprocess import check_call
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    def cull2(self, username):
        try:
            pwd.getpwnam(username)
            cmd = 'pkill -u %s; sleep 2 && pkill -9 -u %s; userdel -r %s' % (username, username, username)
            check_call(cmd, shell=True)
        except KeyError:
            print('User %s does not exist.' % username)
    
    def handle(self, *args, **options):
        while True:
            usernames = os.listdir('/home')
            values = settings.STRICTREDIS.lrange('server', 0, -1)
            for username in usernames:
                username2 = username.encode()
                if not any([username2 in i for i in values]):
                    path2 = settings.HEARTBEAT_DIR + '/' + username
                    if not os.path.isfile(path2):
                        Path(path2).touch()
                    elif int(time.time()) - int(os.path.getmtime(path2)) > 60:
                        os.remove(path2)
                        self.cull2(username)
            time.sleep(2)
