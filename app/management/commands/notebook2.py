import time

from django.core.management.base import BaseCommand, CommandError
from app.models import Notebook

class Command(BaseCommand):
    def handle(self, *args, **options):
        notebooks = Notebook.objects.all()
        for i, nb in enumerate(notebooks):
            print('###########################################', i, notebooks.count())
            x = ("username: {0}\n"
            "port: {1}\n"
            "status: {2}\n"
            "started: {3}\n"
            "time started listening: {4}\n"
            "last activity: {5} {6}sec\n").format(nb.username, nb.port, nb.status, nb.time2, nb.time3, nb.heartbeat, int(time.time())-nb.heartbeat)
            print(x, '\n')
