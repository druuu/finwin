import time
import pwd
from subprocess import check_call

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from app.models import Notebook

class Command(BaseCommand):
    def cull2(self, notebook):
        try:
            pwd.getpwnam(notebook.username)
            cmd = 'pkill -u %s; sleep 2 && pkill -9 -u %s; userdel -r %s' % (notebook.username, notebook.username, notebook.username)
            check_call(cmd, shell=True)
        except KeyError:
            print('User %s does not exist.' % notebook.username)
    
    def handle(self, *args, **options):
        while True:
            notebooks = Notebook.objects.all()
            for notebook in notebooks:
                if int(time.time()) - notebook.heartbeat > 60:
                    username = notebook.username
                    self.cull2(notebook)
                    notebook.delete()
            time.sleep(2)   
