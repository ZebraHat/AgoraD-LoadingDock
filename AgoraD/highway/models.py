#
## models.py
## Logs session information
#

__author__ = 'chase'

from django.db import models
from loading_dock.models import Database, Table


class Session(models.Model):
    def __unicode__(self):
        return str(self.session_id)

    #TODO Layout session
    # logger is default database
    session_id = models.CharField(max_length=256, help_text="Session ID from Marketplace")
    current_block = models.ForeignKey('Block', null=True, blank=True, help_text="Current block database is on")

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