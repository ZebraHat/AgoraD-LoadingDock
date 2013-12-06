#
## models.py
## Models for storing information about the databases that have been introspected
#

from django.db import models

#TODO: less arbitrary name length

#### LOGGER DB ####

class Database(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name

class Table(models.Model):
# multi-column uniqueness
    class Meta:
        unique_together = ('db', 'name')

    db = models.ForeignKey(Database)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Column(models.Model):
# multi-column uniqueness
    class Meta:
        unique_together = ('table', 'name')

    table = models.ForeignKey(Table)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

#### END LOGGER DB ####
