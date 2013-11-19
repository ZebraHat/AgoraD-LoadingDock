#
## models.py
## Logs session information
#

__author__ = 'chase'

from django.db import models
from AgoraD.loading_dock.models import Database, Table


class Session(models.Model):
    def __unicode__(self):
        return str(self.session_id)

    #TODO Layout session
    # logger is default database
    session_id = models.CharField(max_length=256, help_text="Session ID from Marketplace")

    class Meta:
        app_label = 'highway'


class Block(models.Model):
    def __unicode__(self):
        return '{}: {}: {} - {}'.format(self.database, self.table, self.start_row, self.end_row)

    database = models.ForeignKey(Database)
    table = models.ForeignKey(Table)

    start_row = models.IntegerField()
    end_row = models.IntegerField()

    class Meta:
        app_label = 'highway'