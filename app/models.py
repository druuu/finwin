from django.db import models


class Notebook(models.Model):
    username = models.CharField(max_length=255, unique=True)
    base_url = models.CharField(max_length=255, unique=True)
    port = models.IntegerField()
    status = models.IntegerField()
    time2 = models.IntegerField()
    time3 = models.IntegerField(blank=True, null=True)
    heartbeat = models.IntegerField()
    lock = models.BooleanField(default=False)

    def __str__(self):
        return '%s, %s, %d, %d' % (self.username, self.base_url, self.port, self.status)
