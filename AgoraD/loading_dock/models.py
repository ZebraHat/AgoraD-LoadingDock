from django.db import models
import json

#TODO: less arbitrary name length

#### LOGGER DB ####

def toJSON(dbname, tablenames, destdb = None):
    """
    Creates a JSON representation of a table schema. 
    Doesn't include the database name, because that's not guaranteed
    to be the same on the destination server anyway.
    """

    db = Database.objects.get(name=dbname)
    
    schema = {'tables':{}}

    for tablename in tablenames:
        table = Table.objects.get(db=db, name=tablename)
        schema['tables'][tablename] = []

        for column in Column.objects.filter(table=table):
            schema[tablename].append((column.name, column.type))

    if destdb:
        schema['database'] = destdb

    return json.dumps(schema, sort_keys=True)

def fromJSON(dbname, schema_json):
    """
    Creates Database, Table, and Column objects as needed to satisfy the incoming schema.
    If the table is already present, assume we are updating: delete all columns and recreate from the schema.
    """
    
    schema = json.loads(schema_json)
    try:
        db = Database.objects.get(name=dbname)
    except Database.DoesNotExist:
        db = Database(name=dbname)
        db.save()

    for (tablename, columns) in schema.iteritems():
        try:
            table = Table.objects.get(db=db, name=tablename)
            for column in Columns.objects.filter(table=table):
                column.delete()
        except Table.DoesNotExist:
            table = Table(db=db, name=tablename)
            table.save()

        for columninfo in columns:
            column = Column(table=table, name=columninfo[0], type=columninfo[1])
            column.save()

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
