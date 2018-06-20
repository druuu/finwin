import textwrap

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        servers = []
        server_suffixes = []
        for i in range(settings.TOTAL_VMS):
            if i < 9:
                server_suffix = '0%d' % (i+1)
            else:
                server_suffix = '%d' % (i+1)
            server_suffixes.append(server_suffix)
            servers.append('nbs'+server_suffix)
        
        config2 = '[group:nbs]\nprograms=' + ','.join(servers) + '\n'
        config = ''
        for server, server_suffix in zip(servers, server_suffixes):
            config += '''
            [program:%s]
            redirect_stderr=true
            stdout_logfile = /var/log/supervisor/%s.log
            logfile_maxbytes = 5MB
            logfile_backups = 10
            directory = /home/notebook/notebook/scripts
            command = /home/notebook/env/bin/python3 vm.py %s
            ''' % (server, server, server_suffix)

        with open('/etc/supervisor/conf.d/vm.conf', 'w') as f:
            f.write(config2+textwrap.dedent(config))
